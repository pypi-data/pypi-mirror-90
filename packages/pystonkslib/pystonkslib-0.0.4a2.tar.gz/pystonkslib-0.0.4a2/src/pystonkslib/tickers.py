"""Ticker utilities for getting tickers.

Information available at http://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs

Field Name          Definition
==============================
Symbol	            The one to four or five character identifier for each NASDAQ-listed security.
------------------------------
Security Name	    Company issuing the security.
------------------------------
Market Category	    The category assigned to the issue by NASDAQ based on Listing Requirements. Values:
                    Q = NASDAQ Global Select MarketSM
                    G = NASDAQ Global MarketSM
                    S = NASDAQ Capital Market
------------------------------
Test Issue	        Indicates whether or not the security is a test security.
                    Y = yes, it is a test issue.
                    N = no, it is not a test issue.
------------------------------
Financial Status	Indicates when an issuer has failed to submit its regulatory filings on a timely basis,
                    has failed to meet NASDAQ's continuing listing standards, and/or has filed for bankruptcy.
                    Values include:

                    D = Deficient: Issuer Failed to Meet NASDAQ Continued Listing Requirements
                    E = Delinquent: Issuer Missed Regulatory Filing Deadline
                    Q = Bankrupt: Issuer Has Filed for Bankruptcy
                    N = Normal (Default): Issuer Is NOT Deficient, Delinquent, or Bankrupt.
                    G = Deficient and Bankrupt
                    H = Deficient and Delinquent
                    J = Delinquent and Bankrupt
                    K = Deficient, Delinquent, and Bankrupt
------------------------------
Round Lot	        Indicates the number of shares that make up a round lot for the given security.
------------------------------
File Creation Time  The last row of each Symbol Directory text file contains a timestamp that reports the File
                    Creation Time. The file creation time is based on when NASDAQ Trader generates the file and
                    can be used to determine the timeliness of the associated data. The row contains the words
                    File Creation Time followed by mmddyyyyhhmm as the first field, followed by all delimiters
                    to round out the row. An example: File Creation Time: 1217200717:03

"""

import asyncio
import csv
import datetime as dt
import glob
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from configparser import SectionProxy
from ftplib import FTP
from typing import Iterator

import requests

from pystonkslib.config import get_config, get_config_folder, get_data_folder

LOGGER = logging.getLogger(__name__)
POOL_EXECUTOR = ThreadPoolExecutor(max_workers=10)
WAIT_TIME = 10  # Seconds to wait before a thread will pick back up work to avoid rate limiting.


def get_stock_symbols_file(update: bool = False) -> str:
    """Get the stock symbols file for nyse listed."""
    LOGGER.info("Getting stock symbols file.")
    LOGGER.info("Getting config")
    config = get_config()
    LOGGER.info("Got config")
    symbol_info = config["symbol_info"]
    config_folder = get_config_folder()
    symbol_file_location: str = os.path.join(config_folder, symbol_info["filename"])
    LOGGER.info("Found symbol file location: %s", symbol_file_location)

    if not os.path.exists(symbol_file_location):
        LOGGER.info("No symbols file found - downloading.")
        download_stock_symbols(symbol_info, symbol_file_location)

    if update:
        LOGGER.info("Updating stock symbols by request.")
        download_stock_symbols(symbol_info, symbol_file_location)

    LOGGER.info("Stock symbols available in %s", symbol_file_location)
    return symbol_file_location


def download_stock_symbols(symbol_info: SectionProxy, symbol_file_location: str) -> None:
    """Download stock symbols file."""

    LOGGER.info("Downloading symbol info.")
    ftp = FTP(symbol_info["url"])
    ftp.login()
    ftp.cwd(symbol_info["directory"])
    LOGGER.info("Starting FTP transfer of symbol info.")
    with open(symbol_file_location, "wb") as filepath:
        ftp.retrbinary(f"RETR {symbol_info['filename']}", filepath.write)
    LOGGER.info("Finished FTP transfer of symbol info.")


def get_ticker_iterator(stock_symbols_file: str) -> Iterator:
    """Return an iterator of the stock symbols file."""

    csv.register_dialect("nyse_ticker", delimiter="|", quoting=csv.QUOTE_NONE)
    with open(stock_symbols_file, newline="") as symbol_file_obj:
        reader = csv.reader(symbol_file_obj, "nyse_ticker")
        header = []

        # Iterate through shite - there's probably a better way to pull the first row
        # out without using a csv reader, but this is efficient and optimized in other
        # ways for reading the file, so until it's a problem it's probably not worth
        # focusing on.
        for row_index, row in enumerate(reader):
            if row_index == 0:
                header = row
                continue
            obj = {}

            # Use our header to determine our keys for our values.
            for obj_index, item in enumerate(row):
                key = header[obj_index]
                obj[key] = item
            yield obj


def get_valid_tickers() -> list:
    """Get valid tickers based on some sane filters."""
    LOGGER.info("Getting valid tickers.")
    valid_tickers = []

    stock_symbols_file = get_stock_symbols_file()
    LOGGER.info("Got stock symbols file %s.", stock_symbols_file)

    ticker_iterator = get_ticker_iterator(stock_symbols_file)
    LOGGER.info("Got ticker iterator %s.", ticker_iterator)
    last_index = 0
    for index, ticker in enumerate(ticker_iterator):
        # We don't want to care about financial statuses that aren't in good standing.
        if ticker.get("Financial Status") != "N":
            continue
        # We don't want to care about test issues.
        if ticker.get("Test Issue") == "Y":
            continue
        last_index = index
        valid_tickers.append(ticker)
    LOGGER.info("Found %s valid tickers out of %s", len(valid_tickers), last_index)
    return valid_tickers


def get_todays_seconds() -> int:
    """Get epoch time for todays seconds."""

    delta = dt.datetime.now() - dt.datetime(1970, 1, 1)
    todays_seconds = int(delta.total_seconds())
    return todays_seconds


def _get_symbol_data(symbol: str, today_seconds: int) -> int:
    """Get symbol data for a given symbol."""
    data_folder = get_data_folder()
    download_url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1=0&period2={today_seconds}&interval=1d&events=history&includeAdjustedClose=true"  # pylint: disable=line-too-long
    result = requests.get(download_url, allow_redirects=True)
    data_filepath = os.path.join(data_folder, f"{symbol}_data.csv")
    if result.status_code == 200:
        with open(data_filepath, "wb") as symbol_file:
            length = symbol_file.write(result.content)
            LOGGER.info("Got results for symbol %s: %s", symbol, length)
    elif result.status_code == 401:
        LOGGER.error("Got some rate limiting. Not saving a file.")
        length = -1
    elif result.status_code == 404:
        LOGGER.error("No data available for ticker %s.", symbol)
        with open(data_filepath, "wb") as symbol_file:
            symbol_file.write(b"")
        length = -1
    else:
        LOGGER.error("Something's fucky for %s: %s", symbol, result.status_code)
        length = -1
    return length


async def get_symbol_data(symbol: str, today_seconds: int) -> int:
    """Get the data for a given symbol."""

    future = POOL_EXECUTOR.submit(_get_symbol_data, *(symbol, today_seconds))
    result = await asyncio.wrap_future(future)
    return result


async def get_all_data(symbols: list) -> list:
    """Get all the data for the symbols that have been requested."""

    # NOTE: This will almost immediately hit rate limitations - so be wise
    # how you use this.

    LOGGER.info("Getting data for %s symbols", len(symbols))
    today_seconds = get_todays_seconds()
    LOGGER.debug("Todays seconds is: %s", today_seconds)

    data_futures = [asyncio.ensure_future(get_symbol_data(symbol, today_seconds)) for symbol in symbols]
    result = await asyncio.gather(*data_futures)
    return result


def get_missing_symbols(symbols: list) -> list:
    """Get the list of symbols that still need downloading."""
    data_folder = os.path.join(get_config_folder(), "data")
    existing_ticker_files = glob.glob(os.path.join(data_folder, "*.csv"))

    existing_tickers = [os.path.basename(tickerfile).split("_data")[0] for tickerfile in existing_ticker_files]

    missing_tickers = sorted(set(symbols) - set(existing_tickers))
    return missing_tickers


async def get_chunked_data() -> None:
    """Get chunked data because we can't overwhelm amazon with 4k requests."""
    chunk_size = 20

    all_symbols = [str(ticker["Symbol"]) for ticker in get_valid_tickers()]
    needed_symbols = get_missing_symbols(all_symbols)

    while needed_symbols:
        requested_symbols = needed_symbols[:chunk_size]
        LOGGER.info("Getting data for %s", ",".join(requested_symbols))
        await get_all_data(requested_symbols)
        needed_symbols = get_missing_symbols(all_symbols)
        LOGGER.info("%s symbols still need fetching.", len(needed_symbols))
