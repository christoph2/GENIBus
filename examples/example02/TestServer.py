#!/usr/bin/env python
"""Simple TCP logging server for GENIBus example traffic."""

from __future__ import annotations

import argparse
import logging
import socket
import socketserver
from pathlib import Path

PORT = 6734
BUFFER_SIZE = 1024


def build_parser() -> argparse.ArgumentParser:
    """Create command-line parser.

    Returns:
        argparse.ArgumentParser: Configured parser instance.
    """
    parser = argparse.ArgumentParser(description="Run a TCP logging server for GENIBus traffic.")
    parser.add_argument("--host", default=socket.gethostbyname(socket.gethostname()))
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--log-file", type=Path, default=Path("genibus.log"))
    return parser


def configure_logging() -> None:
    """Configure console logging for server diagnostics."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


class LoggingRequestHandler(socketserver.BaseRequestHandler):
    """Handle a single TCP client and append received frames to a file."""

    def handle(self) -> None:
        logger = logging.getLogger("TestServer")
        peer = self.client_address
        logger.info("Connected: %s", peer)
        log_file: Path = self.server.log_file  # type: ignore[attr-defined]
        while True:
            data = self.request.recv(BUFFER_SIZE)
            if not data:
                break
            with log_file.open("a", encoding="utf-8") as output:
                output.write(f"{data.hex()}\n")
        logger.info("Disconnected: %s", peer)


class ThreadedTcpServer(socketserver.ThreadingTCPServer):
    """Threading TCP server with address reuse enabled."""

    allow_reuse_address = True


def main() -> None:
    """Run the TCP logging server until interrupted."""
    args = build_parser().parse_args()
    configure_logging()
    server_address = (args.host, args.port)
    with ThreadedTcpServer(server_address, LoggingRequestHandler) as server:
        server.log_file = args.log_file  # type: ignore[attr-defined]
        logging.getLogger("TestServer").info("TCP server listening on %s:%d", args.host, args.port)
        server.serve_forever()


if __name__ == "__main__":
    main()


