#!/usr/bin/env python
"""TCP test client for the pass-through server example."""

from __future__ import annotations

import argparse
import logging
import socket
import time

SERVER = "192.168.1.2"
PORT = 6734
TIMEOUT_SECONDS = 0.5
POLL_INTERVAL_SECONDS = 1.0
BUFFER_SIZE = 1024

CONNECT_REQ = bytes(
    (
        0x27,
        0x0E,
        0xFE,
        0x01,
        0x00,
        0x02,
        0x02,
        0x03,
        0x04,
        0x02,
        0x2E,
        0x2F,
        0x02,
        0x02,
        0x94,
        0x95,
        0xA2,
        0xAA,
    )
)


def build_parser() -> argparse.ArgumentParser:
    """Create command-line parser.

    Returns:
        argparse.ArgumentParser: Configured parser instance.
    """
    parser = argparse.ArgumentParser(description="GENIBus pass-through TCP test client")
    parser.add_argument("--server", default=SERVER)
    parser.add_argument("--port", type=int, default=PORT)
    return parser


def configure_logging() -> None:
    """Configure console logging output."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def run_client(server: str, port: int) -> None:
    """Run the polling loop and print responses.

    Args:
        server: Target server host or IP.
        port: Target TCP port.
    """
    logger = logging.getLogger("TestClient")
    with socket.create_connection((server, port), timeout=TIMEOUT_SECONDS) as sock:
        sock.settimeout(TIMEOUT_SECONDS)
        logger.info("TCP client connected to %s:%d", server, port)
        while True:
            logger.info("Sending connect request")
            sock.sendall(CONNECT_REQ)
            try:
                response = sock.recv(BUFFER_SIZE)
                logger.info("Response: %s", [hex(value) for value in response])
            except TimeoutError:
                logger.warning("No response within %.1fs", TIMEOUT_SECONDS)
            time.sleep(POLL_INTERVAL_SECONDS)


def main() -> None:
    """Parse args and start the TCP test client."""
    args = build_parser().parse_args()
    configure_logging()
    run_client(server=args.server, port=args.port)


if __name__ == "__main__":
    main()

