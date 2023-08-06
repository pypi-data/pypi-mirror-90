# Izihawa Types

Pure Python varint encoding and type routines

## Example

```python
from izihawa_types import varint, process_varint


x = varint(123123)

assert(x == b'\xf3\xc1\x07')
assert(123123 == process_varint(x))
```