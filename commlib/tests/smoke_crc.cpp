#include <array>
#include <cstdlib>
#include <iostream>

extern "C" {
#include "genibus/crc.h"
}

int main() {
    // Payload bytes: LEN + DA + SA + APDU bytes (without SD and without CRC bytes).
    constexpr std::array<uint8, 8> payload = {
        0x07, 0x20, 0x01, 0x02, 0xC3, 0x02, 0x10, 0x1A,
    };
    constexpr uint16 expected_crc = 0x6FE3;

    const uint16 actual_crc = Crc_CalculateCRC16(payload.data(), static_cast<uint16>(payload.size()), 0xFFFF);
    if (actual_crc != expected_crc) {
        std::cerr << "CRC mismatch: expected 0x" << std::hex << expected_crc
                  << ", got 0x" << actual_crc << "\n";
        return EXIT_FAILURE;
    }

    std::cout << "CRC smoke test passed (0x" << std::hex << actual_crc << ").\n";
    return EXIT_SUCCESS;
}

