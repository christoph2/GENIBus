# Tutorial: Connect to a Pump

This tutorial shows a minimal TCP connection setup.

```python
from genibus.linklayer.tcpclient import Connector

with Connector(host="127.0.0.1", port=6734) as client:
    client.connect()
    # Use APDU helpers to send requests via client.write(...)
```

For real hardware, use `SerialPort` and configure RS-485 direction handling.

