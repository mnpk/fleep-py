# Fleep-py
A python [Fleep](https://fleep.io) API client

Fleep has the RESTful API and you can find the documentation [here](https://fleep.io/fleepapi/).
This package makes it easy to use fleep API in python.

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
