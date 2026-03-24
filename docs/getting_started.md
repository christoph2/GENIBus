# Getting Started

## Installation

Install the package in editable mode with documentation dependencies:

```bash
pip install -e ".[dev,docs]"
```

## Quick Protocol Check

Create and inspect a connect request PDU:

```python
from genibus.apdu import create_connect_request_pdu

frame = create_connect_request_pdu(destination_address=0x10, source_address=0x01)
print(frame.hex())
```

## Run Tests

```bash
pytest tests/unit
```

