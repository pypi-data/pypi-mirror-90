# Python Async Bittrex API Wrapper

This package is used by the Bittrex integration of Home Assistant.

[![PyPI version](https://badge.fury.io/py/aiobittrexapi.svg)](https://badge.fury.io/py/aiobittrexapi)
![Python Tests](https://github.com/DevSecNinja/aiobittrexapi/workflows/Python%20Tests/badge.svg)
![Upload Python Package](https://github.com/DevSecNinja/aiobittrexapi/workflows/Upload%20Python%20Package/badge.svg)
[![codecov](https://codecov.io/gh/DevSecNinja/aiobittrexapi/branch/main/graph/badge.svg?token=938OECIJ6W)](https://codecov.io/gh/DevSecNinja/aiobittrexapi)

## Example

```` python
from aiobittrexapi import Bittrex
from aiobittrexapi.errors import (
    BittrexApiError,
    BittrexResponseError,
    BittrexInvalidAuthentication,
)

import asyncio
from typing import Optional

API_KEY = ""
API_SECRET = ""


async def main(api_key: Optional[str] = None, api_secret: Optional[str] = None):
    if api_key and api_secret:
        api = Bittrex(api_key, api_secret)
    else:
        api = Bittrex()

    try:
        # Get the active markets from Bittrex - works without secret & key
        markets = await api.get_markets()
        print(markets)

        # Get the tickers
        tickers = await api.get_tickers()
        print(tickers)

        # Get your account data - requires secret & key
        account = await api.get_account()
    except BittrexApiError as e:
        print(e)
    except BittrexResponseError as e:
        print("Invalid response:", e)
    except BittrexInvalidAuthentication:
        print("Invalid authentication. Please provide a correct API Key and Secret")
    else:
        print(account)
    finally:
        await api.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    if API_KEY and API_SECRET:
        loop.run_until_complete(main(API_KEY, API_SECRET))
    else:
        loop.run_until_complete(main())

````

## Feedback & Pull Requests

All feedback and Pull Requests are welcome!

## Development

Don't forget to create your venv

```` python
python3 -m venv venv
source venv/bin/activate

````
