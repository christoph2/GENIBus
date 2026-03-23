# AGENTS.md – GENIBus Codebase Guide

## Project Overview

Grundfos **GENIBus** protocol implementation targeting both Python (library + GUI tool) and Arduino/embedded C++.
The Python library (`genibus/`) is the primary deliverable; `tools/genicontrol/` is a wxPython GUI for Magma/UPE pump control.

---

## Repository Layout

| Path | Purpose |
|------|---------|
| `genibus/` | Core Python GENIBus library (installable via `setup.py`) |
| `genibus/gbdefs.py` | All protocol constants, enums (`APDUClass`, `Operation`, `FrameType`) |
| `genibus/apdu.py` | PDU/APDU builders; entry point for constructing telegrams |
| `genibus/linklayer/` | Transport layer: `SerialPort` and `Connector` (TCP) implement `ConnectionIF` ABC |
| `genibus/linklayer/parser.py` | Frame parser: validates CRC, dissects APDUs into `ParseResult` namedtuples |
| `genibus/devices/db.py` | `DeviceDB` Singleton – loads `*.json` device models into in-memory SQLite |
| `genibus/devices/*.json` | Device data item tables (e.g. `magna.json`, `upe.json`) |
| `genibus/config/units.json` | Physical unit definitions loaded by `DeviceDB` |
| `genibus/utils/crc.py` | CRC-HQX (seed 0xffff XOR 0xffff) via `binascii.crc_hqx` |
| `genibus/utils/classes.py` | `SingletonBase` (thread-safe double-checked locking) |
| `commlib/` | Hardware-independent C++ GENIBus datalink layer (POSIX serial/timer) |
| `tools/genicontrol/` | wxPython MVC GUI; uses `wx.lib.pubsub` + `Queue` for threading |
| `examples/` | Arduino `.ino` sketches and matching Python test servers |

---

## Frame & Protocol Architecture

```
[SD (1)] [LEN (1)] [DA (1)] [SA (1)] [...APDUs...] [CRC_HI (1)] [CRC_LO (1)]
```

- **SD** – start delimiter: `0x27` REQUEST, `0x24` REPLY, `0x26` MESSAGE
- **LEN** – byte count of `[DA, SA, APDUs]` (i.e. `len(frame) - 4`)
- **CRC** – computed over `frame[1:-2]` (excludes SD and the CRC bytes themselves)
- Maximum telegram length: **259 bytes**; broadcast address: **0xFF**; connect request address: **0xFE**

Each APDU begins with two header bytes:

```
byte 0: [class (4 lsb)] | [reserved (4 msb)]
byte 1: [op/ack (2 msb)] | [dataByteCount (6 lsb)]
```

Valid operation codes per class are declared in `gbdefs.CLASS_CAPABILITIES`.

---

## Device Data Model

Device data items live in `genibus/devices/<model>.json` as JSON arrays with schema:

```json
["datapoint_name", <class_int>, <id_int>, <access_int>, "<note>"]
```

`DeviceDB` (Singleton) auto-imports all `*.json` files from that directory and `units.json` at first instantiation.
Datapoints are **always addressed by string name** (e.g. `'ref_rem'`, `'unit_family'`) – the DB resolves them to numeric IDs.
Currently supported model: `"magna"` (also `"upe"`).

---

## Key Patterns

- **Singleton**: `DeviceDB` extends `SingletonBase`; safe to call `DeviceDB()` repeatedly – same instance returned.
- **ConnectionIF ABC**: all transports expose `connect / disconnect / write / read / close`. New transports must subclass it and set `DRIVER` class attribute.
- **CRC scope**: `crc.append_tel(pdu)` appends 2 bytes; `crc.check_tel(frame)` raises `CrcError` on mismatch (or returns `False` with `silent=True`).
- **Python 2/3 compatibility**: codebase targets Python 2.7, 3.4, 3.5; uses `enum34` shim for Python < 3.4. Avoid Python-3-only syntax.

---

## Developer Workflows

### Install & Run Tests

```powershell
pip install -r requirements.txt
python setup.py test                                   # runs genibus.tests suite
coverage run --source=genibus setup.py test            # with coverage (as used in CI)
```

Test modules live in `genibus/tests/` and follow the `unittest` pattern; each has a standalone `main()` guard.

### Run a Single Test Module

```powershell
python -m unittest genibus.tests.testAPDU
python -m unittest genibus.tests.testCrc
```

### Arduino / C++ Library

The C++ library under `commlib/` uses an Autotools build:

```bash
autoreconf -i
./configure && make
```

---

## Integration Points

- **Serial transport** (`genibus/linklayer/serialport.py`): RS-485 half-duplex; `write()` calls `output(True)` (line direction) before sending.
- **TCP transport** (`genibus/linklayer/tcpclient.py`): connects to Arduino pass-through server (see `examples/passThruServer/`); default port **6734**.
- **UDP client** (`GB_UDP_Client.py`): minimal diagnostic client targeting Arduino board IP `192.168.100.20`.
- **GeniControl GUI** (`tools/genicontrol/`): wxPython 2.x; uses `wx.lib.pubsub` (legacy `setuparg1` style) – incompatible with wxPython 4+.

---

## Key Files for Quick Reference

- Protocol constants → `genibus/gbdefs.py`
- PDU construction examples → `genibus/tests/testAPDU.py`
- CRC test vectors (known-good frames) → `genibus/tests/testCrc.py`
- Device datapoint names for `"magna"` → `genibus/devices/magna.json`

