# *****************************************************************************
#
# Copyright (c) 2020, the pyEX authors.
#
# This file is part of the jupyterlab_templates library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
from functools import wraps
from io import BytesIO

import pandas as pd
import requests
from deprecation import deprecated
from IPython.display import Image as ImageI
from PIL import Image as ImageP

from ..common import (
    _UTC,
    _expire,
    _getJson,
    _quoteSymbols,
    _raiseIfNotStr,
    _reindex,
    _toDatetime,
    json_normalize,
)


@_expire(hour=4, tz=_UTC)
def company(symbol, token="", version="", filter=""):
    """Company reference data

    https://iexcloud.io/docs/api/#company
    Updates at 4am and 5am UTC every day

    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/company", token, version, filter)


def _companyToDF(c, token="", version="", filter=""):
    """internal"""
    df = json_normalize(c)
    _toDatetime(df)
    _reindex(df, "symbol")
    return df


@wraps(company)
def companyDF(symbol, token="", version="", filter=""):
    c = company(symbol, token, version, filter)
    df = _companyToDF(c)
    return df


@_expire(hour=5, tz=_UTC)
def insiderRoster(symbol, token="", version="", filter=""):
    """Returns the top 10 insiders, with the most recent information.

    https://iexcloud.io/docs/api/#insider-roster
    Updates at 5am, 6am ET every day

    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/insider-roster", token, version, filter)


@wraps(insiderRoster)
def insiderRosterDF(symbol, token="", version="", filter=""):
    val = insiderRoster(symbol, token, version, filter)
    df = pd.DataFrame(val)
    _toDatetime(df, cols=[], tcols=["reportDate"])
    return df


@_expire(hour=5, tz=_UTC)
def insiderSummary(symbol, token="", version="", filter=""):
    """Returns aggregated insiders summary data for the last 6 months.

    https://iexcloud.io/docs/api/#insider-summary
    Updates at 5am, 6am ET every day

    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/insider-summary", token, version, filter)


@wraps(insiderSummary)
def insiderSummaryDF(symbol, token="", version="", filter=""):
    val = insiderSummary(symbol, token, version, filter)
    df = pd.DataFrame(val)
    _toDatetime(df)
    return df


@_expire(hour=5, tz=_UTC)
def insiderTransactions(symbol, token="", version="", filter=""):
    """Returns insider transactions.

    https://iexcloud.io/docs/api/#insider-transactions
    Updates at UTC every day

    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/insider-transactions", token, version, filter)


@wraps(insiderTransactions)
def insiderTransactionsDF(symbol, token="", version="", filter=""):
    val = insiderTransactions(symbol, token, version, filter)
    df = pd.DataFrame(val)
    _toDatetime(df)
    return df


@_expire(hour=0, tz=_UTC)
def logo(symbol, token="", version="", filter=""):
    """This is a helper function, but the google APIs url is standardized.

    https://iexcloud.io/docs/api/#logo
    8am UTC daily

    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/logo", token, version, filter)


@_expire(hour=0, tz=_UTC)
def logoPNG(symbol, token="", version="", filter=""):
    """This is a helper function, but the google APIs url is standardized.

    https://iexcloud.io/docs/api/#logo
    8am UTC daily

    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        image: result as png
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    response = requests.get(logo(symbol, token, version, filter)["url"])
    return ImageP.open(BytesIO(response.content))


@_expire(hour=0, tz=_UTC)
def logoNotebook(symbol, token="", version="", filter=""):
    """This is a helper function, but the google APIs url is standardized.

    https://iexcloud.io/docs/api/#logo
    8am UTC daily

    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        image: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    url = logo(symbol, token, version, filter)["url"]
    return ImageI(url=url)


@_expire(hour=8, tz=_UTC)
def peers(symbol, token="", version="", filter=""):
    """Peers of ticker

    https://iexcloud.io/docs/api/#peers
    8am UTC daily

    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/peers", token, version, filter)


def _peersToDF(p):
    """internal"""
    df = pd.DataFrame(p, columns=["symbol"])
    _toDatetime(df)
    _reindex(df, "symbol")
    df["peer"] = df.index
    return df


@wraps(peers)
def peersDF(symbol, token="", version="", filter=""):
    p = peers(symbol, token, version, filter)
    df = _peersToDF(p)
    return df


@_expire(hour=8, tz=_UTC)
@deprecated(details="Deprecated: IEX Cloud status unkown")
def relevant(symbol, token="", version="", filter=""):
    """Same as peers

    https://iexcloud.io/docs/api/#relevant
    Args:
        symbol (str): Ticker to request
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson("stock/" + symbol + "/relevant", token, version, filter)


@wraps(relevant)
@deprecated(details="Deprecated: IEX Cloud status unkown")
def relevantDF(symbol, token="", version="", filter=""):
    df = pd.DataFrame(relevant(symbol, token, version, filter))
    _toDatetime(df)
    return df
