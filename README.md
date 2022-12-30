# CryptoImpact Bot

Welcome to the Crypto Impact Bot!

https://t.me/crypto_impact_bot

By using me you can track crypto prices  and news, as well as get notifications when various crypto coins move significantly.

You can ask me several commands:

/get_latest_prices to get latest prices for BTC, ETH, and XRP

/get_latest_news to get the latest news article about crypto

/start_monitoring_crypto to monitor prices of crypto coins and getting notified if their returns move above threshold

For any bugs please contact my creator at: argunovvlad5@gmail.com

-------
This project was made as a final task of python course from MSAI program

-------
How the bot was set up?

1. A Postgress Database was set up to track changes in stocks and articles

2. One virtual machine is responsible for updating the database by constantly querying API, it is achieved by executing the "start.sh" file.

3. Another virtual machine is used as a server, where a file "main.py" is executed.


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
