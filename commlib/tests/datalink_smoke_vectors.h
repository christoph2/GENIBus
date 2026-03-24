#ifndef GENIBUS_DATALINK_SMOKE_VECTORS_H
#define GENIBUS_DATALINK_SMOKE_VECTORS_H

#include <array>

extern "C" {
#include "genibus/datalink.h"
}

namespace datalink_smoke_vectors {

constexpr uint8 kConnectRequestSa = 0x01;

constexpr std::array<uint8, 3> kSendPduPayload = {
    0xAA, 0xBB, 0xCC,
};

// Self-consistent frame for current LinkLayer_VerifyCRC behavior:
// CRC is validated over LEN..CRC_HI (CRC_LO is not included).
constexpr std::array<uint8, 6> kFeedValidFrame = {
    GB_SD_REPLY, 0x02, 0x00, 0x04, 0x7A, 0xB1,
};

} // namespace datalink_smoke_vectors

#endif // GENIBUS_DATALINK_SMOKE_VECTORS_H

