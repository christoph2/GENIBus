import socket

import pytest

from genibus.linklayer import tcpclient


class FakeSocketHandle:
    def __init__(self) -> None:
        self.closed = False
        self.timeout = None
        self.connected_addr = None
        self.sent = bytearray()
        self._recv_data = bytearray([0xA1, 0xB2, 0xC3])
        self.sockopts = []

    def setsockopt(self, level, optname, value) -> None:
        self.sockopts.append((level, optname, value))

    def settimeout(self, timeout: float) -> None:
        self.timeout = timeout

    def connect(self, addr) -> None:
        self.connected_addr = addr

    def sendall(self, data: bytearray) -> None:
        self.sent.extend(data)

    def recv(self, bufsize: int) -> bytearray:
        return self._recv_data[:bufsize]

    def close(self) -> None:
        self.closed = True


class FakeSocketModule:
    AF_INET = socket.AF_INET
    SOCK_STREAM = socket.SOCK_STREAM
    SOL_SOCKET = socket.SOL_SOCKET
    SO_REUSEADDR = socket.SO_REUSEADDR

    def __init__(self) -> None:
        self.instances = []

    def socket(self, family, socktype):
        _ = (family, socktype)
        handle = FakeSocketHandle()
        self.instances.append(handle)
        return handle


def test_connection_factory_alias() -> None:
    assert tcpclient.connection_factory("0") == "Simulator"
    assert tcpclient.connection_factory("1") == "Arduino / TCP"
    assert tcpclient.ConnectionFactory("1") == "Arduino / TCP"


def test_connector_connect_write_read_disconnect(monkeypatch) -> None:
    fake_socket = FakeSocketModule()
    monkeypatch.setattr(tcpclient, "socket", fake_socket)

    connector = tcpclient.Connector(server_ip="127.0.0.1", server_port=6734, timeout=0.2, buffer_size=16)

    assert connector.connect() is True
    assert connector.connected is True
    assert fake_socket.instances[0].connected_addr == ("127.0.0.1", 6734)
    assert fake_socket.instances[0].timeout == 0.2

    connector.write([0x10, 0x20])
    assert fake_socket.instances[0].sent == bytearray([0x10, 0x20])

    result = connector.read()
    assert result == bytearray([0xA1, 0xB2, 0xC3])

    connector.disconnect()
    assert connector.connected is False
    assert fake_socket.instances[0].closed is True


def test_connector_legacy_constructor_aliases(monkeypatch) -> None:
    fake_socket = FakeSocketModule()
    monkeypatch.setattr(tcpclient, "socket", fake_socket)

    connector = tcpclient.Connector(serverIP="localhost", serverPort=1234)
    assert connector.server_ip == "localhost"
    assert connector.server_port == 1234
    assert connector.serverIP == "localhost"
    assert connector.serverPort == 1234


def test_connector_read_when_disconnected_returns_none() -> None:
    connector = tcpclient.Connector(server_ip="127.0.0.1", server_port=6734)

    assert connector.read() is None


def test_connector_write_when_disconnected_raises() -> None:
    connector = tcpclient.Connector(server_ip="127.0.0.1", server_port=6734)

    with pytest.raises(RuntimeError):
        connector.write([0x01])

