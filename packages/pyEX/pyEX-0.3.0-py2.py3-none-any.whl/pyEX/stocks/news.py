# *****************************************************************************
#
# Copyright (c) 2020, the pyEX authors.
#
# This file is part of the jupyterlab_templates library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
from functools import wraps

import pandas as pd

from ..common import _getJson, _quoteSymbols, _raiseIfNotStr, _reindex, _toDatetime


def news(symbol, count=10, token="", version="", filter=""):
    """News about company

    https://iexcloud.io/docs/api/#news
    Continuous

    Args:
        symbol (str): Ticker to request
        count (int): limit number of results
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
        dict: result
    """
    _raiseIfNotStr(symbol)
    symbol = _quoteSymbols(symbol)
    return _getJson(
        "stock/" + symbol + "/news/last/" + str(count), token, version, filter
    )


def _newsToDF(n):
    """internal"""
    df = pd.DataFrame(n)
    _toDatetime(df, cols=[], tcols=["datetime"])
    _reindex(df, "datetime")
    return df


@wraps(news)
def newsDF(symbol, count=10, token="", version="", filter=""):
    n = news(symbol, count, token, version, filter)
    df = _newsToDF(n)
    return df


def marketNews(count=10, token="", version="", filter=""):
    """News about market

    https://iexcloud.io/docs/api/#news
    Continuous

    Args:
        count (int): limit number of results
        token (str): Access token
        version (str): API version
        filter (str): filters: https://iexcloud.io/docs/api/#filter-results

    Returns:
        dict or DataFrame: result
        dict: result
    """
    return _getJson("stock/market/news/last/" + str(count), token, version, filter)


@wraps(marketNews)
def marketNewsDF(count=10, token="", version="", filter=""):
    df = pd.DataFrame(marketNews(count, token, version, filter))
    _toDatetime(df)
    _reindex(df, "datetime")
    return df
