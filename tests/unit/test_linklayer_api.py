from collections.abc import Iterable

from genibus.linklayer import serialport
from genibus.linklayer.connection import ConnectionIF


class DummyConnection(ConnectionIF):
    DRIVER = "Dummy"

    def __init__(self) -> None:
        super().__init__()
        self.connected = False

    def connect(self) -> bool:
        self.connected = True
        return True

    def disconnect(self) -> None:
        self.connected = False

    def write(self, data: Iterable[int]) -> None:
        _ = list(data)

    def read(self) -> bytearray | None:
        return bytearray([0x01])

    def close(self) -> None:
        self.disconnect()


class FakeSerialHandle:
    def __init__(self, port_name: str, baudrate: int) -> None:
        self.portstr = port_name
        self.baudrate = baudrate
        self.in_waiting = 3
        self.rts = True
        self.dtr = True
        self.closed = False
        self.flushed = False
        self.written = bytearray()
        self._read_buffer = bytearray([0x11, 0x22, 0x33])

    def write(self, data: bytearray) -> None:
        self.written.extend(data)

    def read(self, amount: int) -> bytearray:
        return self._read_buffer[:amount]

    def flush(self) -> None:
        self.flushed = True

    def close(self) -> None:
        self.closed = True


class FakeSerialModule:
    EIGHTBITS = 8
    PARITY_NONE = "N"
    STOPBITS_ONE = 1
    SerialException = RuntimeError

    def __init__(self) -> None:
        self.instances = []

    def Serial(self, port_name, baudrate, bytesize, parity, stopbits, timeout):
        _ = (bytesize, parity, stopbits, timeout)
        handle = FakeSerialHandle(port_name, baudrate)
        self.instances.append(handle)
        return handle


def test_connectionif_snake_case_and_legacy_aliases() -> None:
    connection = DummyConnection()

    assert connection.get_driver() == "Dummy"
    assert connection.getDriver() == "Dummy"
    assert connection.display_name == "Dummy"
    assert connection.displayName == "Dummy"

    with connection as ctx:
        assert ctx.connected is True

    assert connection.connected is False


def test_serial_port_connect_write_read_disconnect(monkeypatch) -> None:
    fake_serial = FakeSerialModule()
    monkeypatch.setattr(serialport, "serial", fake_serial)
    monkeypatch.setattr(serialport, "serial_available", True)

    port = serialport.SerialPort("COM9", baudrate=19200)

    assert port.connect() is True
    assert port.connected is True

    port.write([0x01, 0x02, 0x03])
    assert fake_serial.instances[0].written == bytearray([0x01, 0x02, 0x03])
    assert fake_serial.instances[0].flushed is True

    result = port.read()
    assert result == bytearray([0x11, 0x22, 0x33])

    # Legacy alias still forwards to snake_case method.
    port.output(True)
    assert fake_serial.instances[0].rts is False
    assert fake_serial.instances[0].dtr is False

    port.disconnect()
    assert port.connected is False
    assert fake_serial.instances[0].closed is True

