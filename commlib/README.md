# commlib CMake Quickstart

This folder now includes a standalone CMake build for the legacy C commlib.

## Build

```bash
cmake -S commlib -B commlib/build-cmake
cmake --build commlib/build-cmake
```

## Run Smoke Tests

```bash
cmake -S commlib -B commlib/build-cmake -DGENIBUS_BUILD_TESTS=ON
cmake --build commlib/build-cmake
ctest --test-dir commlib/build-cmake -C Debug --output-on-failure
```

## Notes

- `src/posix_serial.c` is built only on UNIX when `GENIBUS_BUILD_POSIX_SERIAL=ON`.
- On non-UNIX hosts, the core CRC + datalink objects still build.
- Include root is set to `commlib/`, so headers like `genibus/types.h` resolve.
- `tests/smoke_crc.cpp` validates the CRC core function against a known vector.
- `tests/smoke_datalink.cpp` validates key datalink state and CRC checks.
- `tests/smoke_datalink_feed.cpp` validates `LinkLayer_Feed` for valid/invalid CRC, segmented reassembly, and backlog processing across multiple calls.

## Roadmap

- Migrate C translation units to modern C++20 wrappers/RAII where needed.
- Add portable serial abstraction for non-POSIX platforms.
- Add unit tests for commlib entry points (`LinkLayer_*`, `Crc_CalculateCRC16`).

