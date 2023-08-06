# crypto_prices

Get minutely (max 7 day history)/hourly/daily crypto historical prices via cryptocompare API. The API seems to work without the need of any API key

Keeps on retrying if a rate limit error occurs, eventually all the history can be fetched.

# Installation
```
pip install crypto_prices
 ```

# Usage
 
 ```Python
from datetime import datetime
import crypto_prices.price_fetcher as pf

hourly_xrp_prices = pf.fetch_prices(from_sym='XRP', 
                                    to_sym='USD',
                                    from_date=datetime(2007, 1, 1),
                                    freq='H')

# If rate limit errors occur, play around with the delay and number of retry attempts
hourly_xrp_prices = pf.fetch_prices(from_sym='XRP', 
                                    to_sym='USD',
                                    from_date=datetime(2007, 1, 1),
                                    freq='H',
                                    single_call_retry_count=10,
                                    delay_between_retry_attempts=3)
```

