import os
from dotenv import load_dotenv
import schedule
import time
import requests
from collections import deque
from utils.database_manipulation import add_articles, add_prices
import datetime

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_QUERY_FREQUENCY = int(os.getenv("NEWS_QUERY_FREQUENCY"))
SUPPORTED_TICKERS = os.getenv("SUPPORTED_TICKERS")
PRICES_API_KEY = os.getenv("PRICES_API_KEY")
PRICES_QUERY_FREQUENCY = int(os.getenv("PRICES_QUERY_FREQUENCY"))


def query_news(time_interval_data):
    base_link = "https://cryptonews-api.com/api/v1?"
    parameters = {
        "tickers": SUPPORTED_TICKERS,
        "items": 100,
        "page": 1,
        "date": f"last{time_interval_data}min",
        "token": NEWS_API_KEY,
    }

    re = requests.get(base_link, params=parameters).json()

    return re["data"]


def query_prices():
    """
    Gets latest prices of SUPPORTED_TICKERS and returns them
    in the form {'ticker_name' : value}
    """
    base_link = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
    parameters = {"symbol": SUPPORTED_TICKERS, "convert": "USD"}
    headers = {
        "X-CMC_PRO_API_KEY": PRICES_API_KEY,
    }

    re = requests.get(base_link, params=parameters, headers=headers).json()

    re_data = {}
    for ticker in SUPPORTED_TICKERS.split(","):
        re_data[ticker] = re["data"][ticker][0]["quote"]["USD"]["price"]

    return re_data


def monitor_news(**kwargs):
    """
    Add news to database
    """
    news = query_news(**kwargs)
    add_articles(news)


def monitor_prices(**kwargs):
    """
    Add prices to database
    """
    prices = query_prices(**kwargs)
    add_prices(prices)


if __name__ == "__main__":
    # Run scheduling for quering news articles
    schedule.every(NEWS_QUERY_FREQUENCY).minutes.do(
        monitor_news, time_interval_data=NEWS_QUERY_FREQUENCY
    )
    # Run scheduling for quering stocks
    schedule.every(PRICES_QUERY_FREQUENCY).minutes.do(monitor_prices)

    while True:
        schedule.run_pending()
        time.sleep(1)
