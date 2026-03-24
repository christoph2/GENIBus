#include <array>
#include <cstdlib>
#include <iostream>

#include "datalink_smoke_vectors.h"

extern "C" {
#include "genibus/datalink.h"
}

namespace {

std::array<uint8, 300> g_rx_buffer{};
uint16 g_rx_size = 0;
uint16 g_rx_index = 0;

uint16 g_data_calls = 0;
uint16 g_error_calls = 0;
Gb_Error g_last_error = ERR_INVALID_CRC;

std::array<uint8, 300> g_callback_bytes{};
uint8 g_callback_len = 0;

uint8 write_frame_stub(uint8 const * const, uint16) {
    return 1;
}

uint16 available_stub(void) {
    return static_cast<uint16>(g_rx_size - g_rx_index);
}

uint8 read_byte_stub(void) {
    return g_rx_buffer[g_rx_index++];
}

void on_data_callout(uint8 * buffer, uint8 len) {
    ++g_data_calls;
    g_callback_len = len;
    for (uint16 idx = 0; idx < len; ++idx) {
        g_callback_bytes[idx] = buffer[idx];
    }
}

void on_error_callout(Gb_Error error, uint8 * buffer, uint8 len) {
    ++g_error_calls;
    g_last_error = error;
    g_callback_len = len;
    for (uint16 idx = 0; idx < len; ++idx) {
        g_callback_bytes[idx] = buffer[idx];
    }
}

void reset_callout_capture(void) {
    g_data_calls = 0;
    g_error_calls = 0;
    g_callback_len = 0;
}

template <size_t N>
void load_rx_frame(const std::array<uint8, N> & frame, uint16 frame_len) {
    g_rx_size = frame_len;
    g_rx_index = 0;
    for (uint16 idx = 0; idx < frame_len; ++idx) {
        g_rx_buffer[idx] = frame[idx];
    }
}

bool expect_true(bool value, const char * message) {
    if (!value) {
        std::cerr << "FAILED: " << message << "\n";
        return false;
    }
    return true;
}

} // namespace

int main() {
    Interface iface{};
    iface.writeFrame = write_frame_stub;
    iface.available = available_stub;
    iface.readByte = read_byte_stub;

    DatalinkLayerType link{};
    link.port = &iface;
    link.dataLinkCallout = on_data_callout;
    link.errorCallout = on_error_callout;

    LinkLayer_Init(&link);

    constexpr std::array<uint8, 6> valid_frame = datalink_smoke_vectors::kFeedValidFrame;
    const uint16 valid_frame_len = static_cast<uint16>(valid_frame.size());

    reset_callout_capture();
    load_rx_frame(valid_frame, valid_frame_len);
    LinkLayer_Feed(&link);

    if (!expect_true(g_data_calls == 1, "valid frame should call dataLinkCallout once")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_error_calls == 0, "valid frame should not call errorCallout")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_callback_len == static_cast<uint8>(valid_frame_len), "callback frame length should match received frame")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_callback_bytes[0] == GB_SD_REPLY, "callback should receive original SD byte")) {
        return EXIT_FAILURE;
    }
    for (uint16 idx = 0; idx < valid_frame_len; ++idx) {
        if (!expect_true(g_callback_bytes[idx] == valid_frame[idx], "callback should match full valid frame content")) {
            return EXIT_FAILURE;
        }
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_IDLE, "state should return to DL_IDLE after valid frame")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(link.frameIdx == 0, "frameIdx should be reset after valid frame")) {
        return EXIT_FAILURE;
    }

    std::array<uint8, 6> invalid_frame = valid_frame;
    invalid_frame[valid_frame_len - 1] ^= 0x01;

    reset_callout_capture();
    load_rx_frame(invalid_frame, valid_frame_len);
    LinkLayer_Feed(&link);

    if (!expect_true(g_data_calls == 0, "invalid CRC frame should not call dataLinkCallout")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_error_calls == 1, "invalid CRC frame should call errorCallout once")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_last_error == ERR_INVALID_CRC, "error callback should report ERR_INVALID_CRC")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_IDLE, "state should return to DL_IDLE after CRC error")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(link.frameIdx == 0, "frameIdx should reset after CRC error")) {
        return EXIT_FAILURE;
    }

    // Truncated frame must not fire callbacks and should stay in receive state.
    constexpr std::array<uint8, 4> truncated_frame = {
        datalink_smoke_vectors::kFeedValidFrame[0],
        datalink_smoke_vectors::kFeedValidFrame[1],
        datalink_smoke_vectors::kFeedValidFrame[2],
        datalink_smoke_vectors::kFeedValidFrame[3],
    };

    reset_callout_capture();
    load_rx_frame(truncated_frame, static_cast<uint16>(truncated_frame.size()));
    LinkLayer_Feed(&link);

    if (!expect_true(g_data_calls == 0, "truncated frame should not call dataLinkCallout")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_error_calls == 0, "truncated frame should not call errorCallout yet")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_RECEIVING, "truncated frame should keep DL_RECEIVING state")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(link.frameIdx == static_cast<uint8>(truncated_frame.size()), "frameIdx should reflect buffered bytes")) {
        return EXIT_FAILURE;
    }

    // A no-data feed call must keep current receive progress unchanged.
    g_rx_size = 0;
    g_rx_index = 0;
    LinkLayer_Feed(&link);

    if (!expect_true(LinkLayer_GetState(&link) == DL_RECEIVING, "no-data feed should keep DL_RECEIVING state")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(link.frameIdx == static_cast<uint8>(truncated_frame.size()), "no-data feed should not modify frameIdx")) {
        return EXIT_FAILURE;
    }

    // Feeding the remaining bytes afterwards should complete the frame.
    constexpr std::array<uint8, 2> trailing_frame = {
        datalink_smoke_vectors::kFeedValidFrame[4],
        datalink_smoke_vectors::kFeedValidFrame[5],
    };

    reset_callout_capture();
    load_rx_frame(trailing_frame, static_cast<uint16>(trailing_frame.size()));
    LinkLayer_Feed(&link);

    if (!expect_true(g_data_calls == 1, "trailing bytes should complete and call dataLinkCallout once")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_error_calls == 0, "trailing bytes should not call errorCallout")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_callback_len == static_cast<uint8>(valid_frame_len), "completed callback should report full frame length")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_callback_bytes[0] == GB_SD_REPLY, "completed callback should preserve SD byte")) {
        return EXIT_FAILURE;
    }
    for (uint16 idx = 0; idx < valid_frame_len; ++idx) {
        if (!expect_true(g_callback_bytes[idx] == valid_frame[idx], "completed callback should match full frame content")) {
            return EXIT_FAILURE;
        }
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_IDLE, "state should return to DL_IDLE after frame completion")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(link.frameIdx == 0, "frameIdx should reset after completed frame")) {
        return EXIT_FAILURE;
    }

    // Segmentierter Frame mit fehlerhaftem Rest muss als CRC-Fehler enden.
    reset_callout_capture();
    load_rx_frame(truncated_frame, static_cast<uint16>(truncated_frame.size()));
    LinkLayer_Feed(&link);

    constexpr std::array<uint8, 2> invalid_trailing_frame = {
        datalink_smoke_vectors::kFeedValidFrame[4],
        static_cast<uint8>(datalink_smoke_vectors::kFeedValidFrame[5] ^ 0x01),
    };

    load_rx_frame(invalid_trailing_frame, static_cast<uint16>(invalid_trailing_frame.size()));
    LinkLayer_Feed(&link);

    if (!expect_true(g_data_calls == 0, "invalid segmented frame should not call dataLinkCallout")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_error_calls == 1, "invalid segmented frame should call errorCallout once")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_last_error == ERR_INVALID_CRC, "invalid segmented frame should report ERR_INVALID_CRC")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_IDLE, "state should return to DL_IDLE after segmented CRC error")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(link.frameIdx == 0, "frameIdx should reset after segmented CRC error")) {
        return EXIT_FAILURE;
    }

    // Reassembly should also work when the same frame arrives in three segments.
    constexpr std::array<uint8, 2> segment_1 = {
        datalink_smoke_vectors::kFeedValidFrame[0],
        datalink_smoke_vectors::kFeedValidFrame[1],
    };
    constexpr std::array<uint8, 2> segment_2 = {
        datalink_smoke_vectors::kFeedValidFrame[2],
        datalink_smoke_vectors::kFeedValidFrame[3],
    };
    constexpr std::array<uint8, 2> segment_3 = {
        datalink_smoke_vectors::kFeedValidFrame[4],
        datalink_smoke_vectors::kFeedValidFrame[5],
    };

    reset_callout_capture();
    load_rx_frame(segment_1, static_cast<uint16>(segment_1.size()));
    LinkLayer_Feed(&link);
    if (!expect_true(g_data_calls == 0 && g_error_calls == 0, "segment 1 should not trigger callbacks")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_RECEIVING, "segment 1 should keep DL_RECEIVING state")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(link.frameIdx == static_cast<uint8>(segment_1.size()), "segment 1 should advance frameIdx")) {
        return EXIT_FAILURE;
    }

    load_rx_frame(segment_2, static_cast<uint16>(segment_2.size()));
    LinkLayer_Feed(&link);
    if (!expect_true(g_data_calls == 0 && g_error_calls == 0, "segment 2 should not trigger callbacks")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_RECEIVING, "segment 2 should keep DL_RECEIVING state")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(link.frameIdx == static_cast<uint8>(segment_1.size() + segment_2.size()), "segment 2 should advance frameIdx")) {
        return EXIT_FAILURE;
    }

    load_rx_frame(segment_3, static_cast<uint16>(segment_3.size()));
    LinkLayer_Feed(&link);
    if (!expect_true(g_data_calls == 1, "segment 3 should complete frame and call dataLinkCallout")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_error_calls == 0, "three-segment valid frame should not call errorCallout")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_IDLE, "three-segment completion should return to DL_IDLE")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(link.frameIdx == 0, "three-segment completion should reset frameIdx")) {
        return EXIT_FAILURE;
    }
    for (uint16 idx = 0; idx < valid_frame_len; ++idx) {
        if (!expect_true(g_callback_bytes[idx] == valid_frame[idx], "three-segment callback should match full frame content")) {
            return EXIT_FAILURE;
        }
    }

    // If two valid frames are buffered, one feed call handles only one frame.
    constexpr std::array<uint8, 12> two_frame_stream = {
        datalink_smoke_vectors::kFeedValidFrame[0],
        datalink_smoke_vectors::kFeedValidFrame[1],
        datalink_smoke_vectors::kFeedValidFrame[2],
        datalink_smoke_vectors::kFeedValidFrame[3],
        datalink_smoke_vectors::kFeedValidFrame[4],
        datalink_smoke_vectors::kFeedValidFrame[5],
        datalink_smoke_vectors::kFeedValidFrame[0],
        datalink_smoke_vectors::kFeedValidFrame[1],
        datalink_smoke_vectors::kFeedValidFrame[2],
        datalink_smoke_vectors::kFeedValidFrame[3],
        datalink_smoke_vectors::kFeedValidFrame[4],
        datalink_smoke_vectors::kFeedValidFrame[5],
    };

    reset_callout_capture();
    load_rx_frame(two_frame_stream, static_cast<uint16>(two_frame_stream.size()));
    LinkLayer_Feed(&link);

    if (!expect_true(g_data_calls == 1, "first feed on two-frame stream should process one frame")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_error_calls == 0, "first feed on two-frame stream should not call errorCallout")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_rx_index == valid_frame_len, "first feed should consume exactly one frame")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_IDLE, "state should be DL_IDLE after first frame completion")) {
        return EXIT_FAILURE;
    }

    LinkLayer_Feed(&link);

    if (!expect_true(g_data_calls == 2, "second feed on two-frame stream should process remaining frame")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_error_calls == 0, "second feed on two-frame stream should not call errorCallout")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_rx_index == static_cast<uint16>(two_frame_stream.size()), "second feed should consume the full stream")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_IDLE, "state should stay DL_IDLE after second frame completion")) {
        return EXIT_FAILURE;
    }

    // Mixed backlog: first frame valid, second frame CRC-invalid.
    constexpr std::array<uint8, 12> mixed_two_frame_stream = {
        datalink_smoke_vectors::kFeedValidFrame[0],
        datalink_smoke_vectors::kFeedValidFrame[1],
        datalink_smoke_vectors::kFeedValidFrame[2],
        datalink_smoke_vectors::kFeedValidFrame[3],
        datalink_smoke_vectors::kFeedValidFrame[4],
        datalink_smoke_vectors::kFeedValidFrame[5],
        datalink_smoke_vectors::kFeedValidFrame[0],
        datalink_smoke_vectors::kFeedValidFrame[1],
        datalink_smoke_vectors::kFeedValidFrame[2],
        datalink_smoke_vectors::kFeedValidFrame[3],
        datalink_smoke_vectors::kFeedValidFrame[4],
        static_cast<uint8>(datalink_smoke_vectors::kFeedValidFrame[5] ^ 0x01),
    };

    reset_callout_capture();
    load_rx_frame(mixed_two_frame_stream, static_cast<uint16>(mixed_two_frame_stream.size()));
    LinkLayer_Feed(&link);

    if (!expect_true(g_data_calls == 1, "mixed backlog first feed should process valid frame")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_error_calls == 0, "mixed backlog first feed should not call errorCallout")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_rx_index == valid_frame_len, "mixed backlog first feed should consume first frame")) {
        return EXIT_FAILURE;
    }

    LinkLayer_Feed(&link);

    if (!expect_true(g_data_calls == 1, "mixed backlog second feed should not increment data callbacks")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_error_calls == 1, "mixed backlog second feed should report one CRC error")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_last_error == ERR_INVALID_CRC, "mixed backlog second feed should report ERR_INVALID_CRC")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_rx_index == static_cast<uint16>(mixed_two_frame_stream.size()), "mixed backlog should consume full stream after second feed")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_IDLE, "mixed backlog second feed should return DL_IDLE")) {
        return EXIT_FAILURE;
    }

    // Mixed backlog (inverse): first frame CRC-invalid, second frame valid.
    constexpr std::array<uint8, 12> mixed_two_frame_stream_inverse = {
        datalink_smoke_vectors::kFeedValidFrame[0],
        datalink_smoke_vectors::kFeedValidFrame[1],
        datalink_smoke_vectors::kFeedValidFrame[2],
        datalink_smoke_vectors::kFeedValidFrame[3],
        datalink_smoke_vectors::kFeedValidFrame[4],
        static_cast<uint8>(datalink_smoke_vectors::kFeedValidFrame[5] ^ 0x01),
        datalink_smoke_vectors::kFeedValidFrame[0],
        datalink_smoke_vectors::kFeedValidFrame[1],
        datalink_smoke_vectors::kFeedValidFrame[2],
        datalink_smoke_vectors::kFeedValidFrame[3],
        datalink_smoke_vectors::kFeedValidFrame[4],
        datalink_smoke_vectors::kFeedValidFrame[5],
    };

    reset_callout_capture();
    load_rx_frame(mixed_two_frame_stream_inverse, static_cast<uint16>(mixed_two_frame_stream_inverse.size()));
    LinkLayer_Feed(&link);

    if (!expect_true(g_data_calls == 0, "inverse mixed backlog first feed should not call dataLinkCallout")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_error_calls == 1, "inverse mixed backlog first feed should report one CRC error")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_last_error == ERR_INVALID_CRC, "inverse mixed backlog first feed should report ERR_INVALID_CRC")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_rx_index == valid_frame_len, "inverse mixed backlog first feed should consume first frame")) {
        return EXIT_FAILURE;
    }

    LinkLayer_Feed(&link);

    if (!expect_true(g_data_calls == 1, "inverse mixed backlog second feed should process valid frame")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_error_calls == 1, "inverse mixed backlog second feed should not add errors")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_rx_index == static_cast<uint16>(mixed_two_frame_stream_inverse.size()), "inverse mixed backlog should consume full stream after second feed")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_IDLE, "inverse mixed backlog second feed should return DL_IDLE")) {
        return EXIT_FAILURE;
    }
    for (uint16 idx = 0; idx < valid_frame_len; ++idx) {
        if (!expect_true(g_callback_bytes[idx] == valid_frame[idx], "inverse mixed backlog callback should match valid frame")) {
            return EXIT_FAILURE;
        }
    }

    std::cout << "Datalink feed smoke test passed.\n";
    return EXIT_SUCCESS;
}

