# fleep-py
A python Fleep API client


## Example

```python3
from fleep_client import FleepClient

c = FleepClient()
# connect using env variables: FLEEP_EMAIL, FLEEP_PASSWORD
c.connect()
c.send('conv-id', 'hello')
```

## LICENSE

MIT License
