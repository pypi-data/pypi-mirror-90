# pybarry

Python3 library for [Barry](https://barry.energy/dk).

Get electricity consumption price.

## Install

```
pip3 install pybarry
```

## Example:

```python
from pybarry import Barry

access_token = '<your barry token>'
barry_connection = Barry(access_token=access_token)
# Get price_code from where your metering point is located
latest_price = barry_connection.update_price_data(price_code=price_code)
print(latest_price)
```