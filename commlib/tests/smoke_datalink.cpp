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

    // Reset should recover from an arbitrary in-progress state.
    LinkLayer_SetState(&link, DL_RECEIVING);
    link.frameLength = 0x55;
    link.frameIdx = 0x44;
    LinkLayer_Reset(&link);
    if (!expect_true(LinkLayer_GetState(&link) == DL_IDLE, "LinkLayer_Reset should set DL_IDLE")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(link.frameLength == 0, "LinkLayer_Reset should clear frameLength")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(link.frameIdx == 0, "LinkLayer_Reset should clear frameIdx")) {
        return EXIT_FAILURE;
    }

    LinkLayer_SetState(&link, DL_SENDING);
    if (!expect_true(LinkLayer_GetState(&link) == DL_SENDING, "state transition DL_SENDING failed")) {
        return EXIT_FAILURE;
    }

    // Send must be ignored when not idle.
    g_write_calls = 0;
    g_last_tx_len = 0xFFFF;
    g_last_tx.fill(0xEE);
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
    if (!expect_true(g_last_tx_len == 0xFFFF, "rejected send should not change last TX length")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_last_tx[0] == 0xEE, "rejected send should not change TX buffer")) {
        return EXIT_FAILURE;
    }

    // Connect request also goes through send path and must be ignored when not idle.
    g_write_calls = 0;
    g_last_tx_len = 0xFFFF;
    g_last_tx.fill(0xEE);
    LinkLayer_SetState(&link, DL_SENDING);
    LinkLayer_ConnectRequest(&link, datalink_smoke_vectors::kConnectRequestSa);
    if (!expect_true(g_write_calls == 0, "LinkLayer_ConnectRequest should not write when state is not DL_IDLE")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_SENDING, "state should remain unchanged when connect request is rejected")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_last_tx_len == 0xFFFF, "rejected connect request should not change last TX length")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_last_tx[0] == 0xEE, "rejected connect request should not change TX buffer")) {
        return EXIT_FAILURE;
    }

    // Sending API requires idle state.
    LinkLayer_SetState(&link, DL_IDLE);

    // Edge-case: minimal payload length (2) should still go through send path safely.
    g_write_calls = 0;
    g_last_tx_len = 0xFFFF;
    g_last_tx.fill(0xEE);
    LinkLayer_SendPDU(
        &link,
        GB_SD_REQUEST,
        0x20,
        datalink_smoke_vectors::kConnectRequestSa,
        datalink_smoke_vectors::kSendPduPayload.data(),
        2
    );
    if (!expect_true(g_write_calls == 1, "minimal-length send should call writeFrame once")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_last_tx_len == 2, "minimal-length send should write two bytes")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_last_tx[0] == GB_SD_REQUEST, "minimal-length send should write SD byte")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_last_tx[1] == 0x04, "minimal-length send should write LEN=4")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_last_tx[2] == 0xEE, "minimal-length send should not touch bytes beyond transmitted length")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_IDLE, "minimal-length send should return to DL_IDLE")) {
        return EXIT_FAILURE;
    }

    g_write_calls = 0;
    g_last_tx_len = 0;
    g_last_tx.fill(0xCC);
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
    if (!expect_true(
        g_last_tx[3] == 0xCC,
        "current implementation writes only the first payload_len bytes (bytes beyond len stay untouched)"
    )) {
        return EXIT_FAILURE;
    }
    if (!expect_true(
        g_last_tx[4] == 0xCC,
        "send path must not modify bytes beyond transmitted length"
    )) {
        return EXIT_FAILURE;
    }

    g_last_tx.fill(0xCC);
    LinkLayer_ConnectRequest(&link, datalink_smoke_vectors::kConnectRequestSa);
    if (!expect_true(g_write_calls == 2, "LinkLayer_ConnectRequest should trigger a second writeFrame call")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_IDLE, "state should return to DL_IDLE after connect request")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(g_last_tx[0] == GB_SD_REQUEST, "connect request should use request delimiter")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(
        g_last_tx[1] == static_cast<uint8>(datalink_smoke_vectors::kConnectRequestPayloadLen + 2),
        "connect request LEN byte should be payload+2"
    )) {
        return EXIT_FAILURE;
    }
    if (!expect_true(
        g_last_tx[2] == datalink_smoke_vectors::kConnectRequestDa && g_last_tx[3] == datalink_smoke_vectors::kConnectRequestSa,
        "connect request should target DA=0xFE, SA=0x01"
    )) {
        return EXIT_FAILURE;
    }
    if (!expect_true(
        g_last_tx_len == datalink_smoke_vectors::kConnectRequestPayloadLen,
        "connect request write length should match payload length"
    )) {
        return EXIT_FAILURE;
    }
    const uint16 transmitted_payload_len =
        g_last_tx_len > 4 ? static_cast<uint16>(g_last_tx_len - 4) : static_cast<uint16>(0);
    if (!expect_true(transmitted_payload_len == 8, "current implementation transmits 8 connect payload bytes")) {
        return EXIT_FAILURE;
    }
    for (uint16 idx = 0; idx < transmitted_payload_len; ++idx) {
        if (!expect_true(
            g_last_tx[4 + idx] == datalink_smoke_vectors::kConnectRequestPayload[idx],
            "transmitted connect payload bytes should match expected prefix"
        )) {
            return EXIT_FAILURE;
        }
    }
    if (!expect_true(
        g_last_tx[g_last_tx_len] == 0xCC,
        "connect path must not modify bytes beyond transmitted length"
    )) {
        return EXIT_FAILURE;
    }

    constexpr uint8 alt_connect_sa = 0x7A;
    g_last_tx.fill(0xCC);
    LinkLayer_ConnectRequest(&link, alt_connect_sa);
    if (!expect_true(g_write_calls == 3, "second LinkLayer_ConnectRequest should trigger a third writeFrame call")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(LinkLayer_GetState(&link) == DL_IDLE, "second connect request should return to DL_IDLE")) {
        return EXIT_FAILURE;
    }
    if (!expect_true(
        g_last_tx[2] == datalink_smoke_vectors::kConnectRequestDa && g_last_tx[3] == alt_connect_sa,
        "second connect request should keep DA and update SA"
    )) {
        return EXIT_FAILURE;
    }
    if (!expect_true(
        g_last_tx[1] == static_cast<uint8>(datalink_smoke_vectors::kConnectRequestPayloadLen + 2),
        "second connect request LEN byte should be payload+2"
    )) {
        return EXIT_FAILURE;
    }
    if (!expect_true(
        g_last_tx_len == datalink_smoke_vectors::kConnectRequestPayloadLen,
        "second connect request write length should match payload length"
    )) {
        return EXIT_FAILURE;
    }
    for (uint16 idx = 0; idx < transmitted_payload_len; ++idx) {
        if (!expect_true(
            g_last_tx[4 + idx] == datalink_smoke_vectors::kConnectRequestPayload[idx],
            "second connect request payload bytes should match expected prefix"
        )) {
            return EXIT_FAILURE;
        }
    }
    if (!expect_true(
        g_last_tx[g_last_tx_len] == 0xCC,
        "second connect request should not modify bytes beyond transmitted length"
    )) {
        return EXIT_FAILURE;
    }

    std::cout << "Datalink smoke test passed.\n";
    return EXIT_SUCCESS;
}


