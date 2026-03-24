# Protocol Overview

A GENIBus telegram has this wire format:

`[SD][LEN][DA][SA][...APDUs...][CRC_HI][CRC_LO]`

- `SD` start delimiter (`0x27` request, `0x24` reply, `0x26` message)
- `LEN` payload length of `DA + SA + APDUs`
- `CRC` computed over `frame[1:-2]`

## APDU Header

Each APDU starts with two bytes:

- `byte 0`: class in low 4 bits
- `byte 1`: operation/ack in high 2 bits, data length in low 6 bits

See `genibus.gbdefs` for enum definitions and class capability tables.

