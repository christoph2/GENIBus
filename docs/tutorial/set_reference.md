# Tutorial: Set a Reference Value

Use `DeviceDB` to resolve datapoints by symbolic name, then build an APDU request.

```python
from genibus.devices.db import DeviceDB

db = DeviceDB()
item = db.datapoint_from_name("magna", "ref_rem")
print(item)
```

Once you have class and ID, compose the write APDU with `genibus.apdu` helpers.

