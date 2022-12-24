# CryptoImpact Bot

Welcome to the Crypto Impact Bot!

https://t.me/crypto_impact_bot

By using me you can track crypto prices  and news, as well as get notifications when various crypto coins move significantly.

You can ask me several commands:

/get_latest_prices to get latest prices for BTC, ETH, and XRP

/get_latest_news to get the latest news article about crypto

/start_monitoring_crypto to monitor prices of crypto coins and getting notified if their returns move above threshold

/stop_monitoring_crypto to stop monitoring pricesPlease note that I am still in development and sometimes might produce some weird results.

For any bugs please contact my creator at: argunovvlad5@gmail.com

-------
This project was made as a final task of python course from MSAI program

-------
How to start up bot?

1. Go to the [bot](/bot) directory and run the command: `pip install -e .` to install it as a package.

2. Run `poetry install` to install all project packages

3. Run `poetry run bash start.sh` to start updating the database and using the APIs

4. Run `poetry run python main.py` to start the server

Note that for successfull start of the project you must have a *.env* file with all the configuration and API keys.

Below I also publish a sample of code that is used in my .env file:

```
API_KEY = SOME_KEY1 # telegram API key

# Data management
SQLALCHEMY_DATABASE_URI = sqlite:///database.db

# Cryptonews API
NEWS_API_KEY = SOME_KEY2 # API key from https://cryptonews-api.com, you need a premium account for that to work properly

# Supported TICKERS
SUPPORTED_TICKERS = 'BTC,ETH,XRP' # string of tickers with comma between

# Query frequency
NEWS_QUERY_FREQUENCY = 15 # mins
PRICES_QUERY_FREQUENCY = 1 # mins

# CoinAPI API
PRICES_API_KEY = SOME_KEY3 # API key from https://docs.coinapi.io/, can use basic account
```
