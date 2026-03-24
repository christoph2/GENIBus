#include <array>
#include <cstdlib>
#include <iostream>

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

    // This frame is self-consistent for the current LinkLayer_VerifyCRC behavior
    // (CRC is checked over LEN..CRC_HI, i.e. without CRC_LO).
    constexpr std::array<uint8, 6> valid_frame = {
        GB_SD_REPLY, 0x02, 0x00, 0x04, 0x7A, 0xB1,
    };
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

    std::cout << "Datalink feed smoke test passed.\n";
    return EXIT_SUCCESS;
}

