#include <array>
#include <cstdlib>
#include <iostream>

#include "datalink_smoke_vectors.h"

extern "C" {
#include "genibus/datalink.h"
}

namespace {

std::array<uint8, 16> g_rx_buffer{};
uint16 g_rx_size = 0;
uint16 g_rx_index = 0;

std::array<uint8, 300> g_last_tx{};
uint16 g_last_tx_len = 0;
uint16 g_write_calls = 0;

uint8 write_frame_stub(uint8 const * const buf, uint16 len) {
    ++g_write_calls;
    g_last_tx_len = len;
    for (uint16 i = 0; i < len && i < g_last_tx.size(); ++i) {
        g_last_tx[i] = buf[i];
    }
    return 1;
}

uint16 available_stub(void) {
    return static_cast<uint16>(g_rx_size - g_rx_index);
}

uint8 read_byte_stub(void) {
    return g_rx_buffer[g_rx_index++];
}

bool expect_true(bool value, const char *message) {
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

    LinkLayer_Init(&link);
    if (!expect_true(LinkLayer_GetState(&link) == DL_IDLE, "LinkLayer_Init should set DL_IDLE")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(link.frameLength == 0, "frameLength should be reset to 0")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(link.frameIdx == 0, "frameIdx should be reset to 0")) {
        return EXIT_FAILURE;
    }

    LinkLayer_SetState(&link, DL_SENDING);
    if (!expect_true(LinkLayer_GetState(&link) == DL_SENDING, "state transition DL_SENDING failed")) {
        return EXIT_FAILURE;
    }

    // Send must be ignored when not idle.
    g_write_calls = 0;
    LinkLayer_SetState(&link, DL_RECEIVING);
    LinkLayer_SendPDU(
        &link,
        GB_SD_REQUEST,
        0x20,
        datalink_smoke_vectors::kConnectRequestSa,
        datalink_smoke_vectors::kSendPduPayload.data(),
        static_cast<uint8>(datalink_smoke_vectors::kSendPduPayload.size())
    );
    if (!expect_true(g_write_calls == 0, "LinkLayer_SendPDU should not write when state is not DL_IDLE")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_RECEIVING, "state should remain unchanged when send is rejected")) {
        return EXIT_FAILURE;
    }

    // Connect request also goes through send path and must be ignored when not idle.
    g_write_calls = 0;
    LinkLayer_SetState(&link, DL_SENDING);
    LinkLayer_ConnectRequest(&link, datalink_smoke_vectors::kConnectRequestSa);
    if (!expect_true(g_write_calls == 0, "LinkLayer_ConnectRequest should not write when state is not DL_IDLE")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_SENDING, "state should remain unchanged when connect request is rejected")) {
        return EXIT_FAILURE;
    }

    // Sending API requires idle state.
    LinkLayer_SetState(&link, DL_IDLE);

    g_write_calls = 0;
    g_last_tx_len = 0;
    LinkLayer_SendPDU(
        &link,
        GB_SD_REQUEST,
        0x20,
        datalink_smoke_vectors::kConnectRequestSa,
        datalink_smoke_vectors::kSendPduPayload.data(),
        static_cast<uint8>(datalink_smoke_vectors::kSendPduPayload.size())
    );

    if (!expect_true(g_write_calls == 1, "LinkLayer_SendPDU should call writeFrame once")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_IDLE, "state should return to DL_IDLE after send")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_last_tx[0] == GB_SD_REQUEST, "SD byte should be written")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(
        g_last_tx[1] == static_cast<uint8>(datalink_smoke_vectors::kSendPduPayload.size() + 2),
        "LEN byte should be payload+2"
    )) {
        return EXIT_FAILURE;
    }
    if (!expect_true(
        g_last_tx_len == static_cast<uint16>(datalink_smoke_vectors::kSendPduPayload.size()),
        "writeFrame length should match current implementation"
    )) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_last_tx[2] == 0x20, "DA byte should match input")) {
        return EXIT_FAILURE;
    }

    LinkLayer_ConnectRequest(&link, datalink_smoke_vectors::kConnectRequestSa);
    if (!expect_true(g_write_calls == 2, "LinkLayer_ConnectRequest should trigger a second writeFrame call")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_last_tx[0] == GB_SD_REQUEST, "connect request should use request delimiter")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(
        g_last_tx[2] == 0xFE && g_last_tx[3] == datalink_smoke_vectors::kConnectRequestSa,
        "connect request should target DA=0xFE, SA=0x01"
    )) {
        return EXIT_FAILURE;
    }

    std::cout << "Datalink smoke test passed.\n";
    return EXIT_SUCCESS;
}


