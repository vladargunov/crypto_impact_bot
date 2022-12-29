import datetime

from database.create_session import create_session
from models.article import Article
from models.stocks import Stocks

MONTH_MAPPER = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def add_articles(articles, **kwargs):
    added_keys = ["news_url", "title", "time", "source_name", "tickers"]

    session = create_session(**kwargs)  # additional args for custom engine for testing
    for article in articles:
        # Adjust date for SQL
        date_input = article["date"].split()
        article["time"] = datetime.datetime(
            year=int(date_input[3]),
            month=MONTH_MAPPER[date_input[2]],
            day=int(date_input[1]),
            hour=int(date_input[4][:2]),
            minute=int(date_input[4][3:5]),
            second=int(date_input[4][6:]),
        )

        article["time"] = int(article["time"].timestamp())
        # Adjust tickers for SQL
        article["tickers"] = " ".join(article["tickers"])

        data = {key: article.get(key, -100) for key in added_keys}
        article_ = Article(**data)
        session.add(article_)

    session.commit()
    session.close()


def add_prices(prices, **kwargs):
    """
    Add prices to the database
    """
    session = create_session(**kwargs)  # additional args for custom engine for testing
    prices["time"] = int(datetime.datetime.now().timestamp())
    stocks_ = Stocks(**prices)
    session.add(stocks_)
    session.commit()
    session.close()




def retrieve_latest_news():
    """
    Retrieve latest news from database
    """
    session = create_session()
    last_article = session.query(Article).order_by(Article.id.desc()).first()
    session.close()
    out_str = "Latest Article:\n"
    out_str += str(f"Title: {last_article.title}\n")
    out_str += str(f"Tickers: {last_article.tickers}\n")
    out_str += str(f"URL {last_article.news_url}\n")

    return out_str


def retrieve_latest_prices():
    """
    Retrieve latest news from database
    """
    session = create_session()
    last_prices = session.query(Stocks).order_by(Stocks.id.desc()).first()
    session.close()
    out_str = "Latest prices:\n"
    out_str += str(f"BTC {last_prices.BTC}\n")
    out_str += str(f"ETH {last_prices.ETH}\n")
    out_str += str(f"XRP {last_prices.XRP}\n")

    data = {
        "BTC": float(last_prices.BTC),
        "ETH": float(last_prices.ETH),
        "XRP": float(last_prices.XRP),
    }
    return out_str, data


def retrieve_prices_n_minutes_back(n_minutes=10):
    """
    Retrieve latest news from database
    """
    session = create_session()
    prices = session.query(Stocks).order_by(Stocks.id.desc()).offset(n_minutes).first()
    session.close()
    out_str = f"Prices {n_minutes} minutes back:\n"
    out_str += str(f"BTC {prices.BTC}\n")
    out_str += str(f"ETH {prices.ETH}\n")
    out_str += str(f"XRP {prices.XRP}\n")

    data = {
        "BTC": float(prices.BTC),
        "ETH": float(prices.ETH),
        "XRP": float(prices.XRP),
    }

    return out_str, data
