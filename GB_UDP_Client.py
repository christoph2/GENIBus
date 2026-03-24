#!/usr/bin/env python
"""Legacy diagnostic client for receiving GENIBus TCP traffic."""

from __future__ import annotations

import argparse
import logging
import socket

SERVER = "192.168.100.20"
PORT = 6734
BUFFER_SIZE = 1024
TIMEOUT_SECONDS = 1.0


def build_parser() -> argparse.ArgumentParser:
    """Create command-line parser.

    Returns:
        argparse.ArgumentParser: Configured parser instance.
    """
    parser = argparse.ArgumentParser(description="Receive and print TCP GENIBus payloads.")
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
    """Connect to server and print incoming payloads.

    Args:
        server: Target host or IP.
        port: Target TCP port.
    """
    logger = logging.getLogger("GB_UDP_Client")
    with socket.create_connection((server, port), timeout=TIMEOUT_SECONDS) as sock:
        sock.settimeout(TIMEOUT_SECONDS)
        logger.info("TCP client connected to %s:%d", server, port)
        while True:
            try:
                payload = sock.recv(BUFFER_SIZE)
                if not payload:
                    logger.info("Connection closed by remote host")
                    return
                logger.info("Payload: %r", payload)
            except TimeoutError:
                logger.debug("No payload received within timeout")


def main() -> None:
    """Parse args and start the diagnostic client."""
    args = build_parser().parse_args()
    configure_logging()
    run_client(server=args.server, port=args.port)


if __name__ == "__main__":
    main()
