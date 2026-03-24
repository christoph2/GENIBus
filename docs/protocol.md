# Protocol Overview

A GENIBus telegram has this wire format:

`[SD][LEN][DA][SA][...APDUs...][CRC_HI][CRC_LO]`

- `SD` start delimiter (`0x27` request, `0x24` reply, `0x26` message)
- `LEN` payload length of `DA + SA + APDUs` (`len(frame) - 4`)
- `CRC` computed over `frame[1:-2]` (excludes `SD` and CRC bytes)

## Addressing and Limits

- Maximum telegram length is `259` bytes.
- Broadcast destination address is `0xFF`.
- Connection request destination address is `0xFE`.

## CRC Scope

The CRC bytes are appended as `CRC_HI`, `CRC_LO`.

- Sender computes CRC over `LEN..last_apdu_byte`.
- Receiver validates against the trailing two CRC bytes.

In Python code this corresponds to:

- append: `genibus.utils.crc.append_tel(...)`
- check: `genibus.utils.crc.check_tel(...)`

## APDU Header

Each APDU starts with two bytes:

- `byte 0`: APDU class in low 4 bits, upper 4 bits reserved
- `byte 1`: operation/ack in high 2 bits, data length in low 6 bits

Bit layout:

- `header0 = 0brrrrcccc`
  - `cccc`: class (`APDUClass`)
  - `rrrr`: reserved
- `header1 = 0booLLLLLL`
  - `oo`: operation or acknowledge (`Operation` / `Acknowledge`)
  - `LLLLLL`: APDU payload byte count

## Class Capabilities

Not every APDU class supports every operation.

- Valid combinations are declared in `genibus.gbdefs.CLASS_CAPABILITIES`.
- Parsers should reject unknown class values.
- Builders should only emit class/operation pairs listed in capabilities.

## Example Frame

Example request frame (hex bytes):

`27 07 20 01 02 C3 02 10 1A 90 1C`

- `27`: request start delimiter
- `07`: length (`DA + SA + APDUs`)
- `20`: destination address
- `01`: source address
- `02 C3 02 10 1A`: one APDU (class/operation/length + payload)
- `90 1C`: CRC

See `genibus.gbdefs` for enum definitions and class capability tables.

