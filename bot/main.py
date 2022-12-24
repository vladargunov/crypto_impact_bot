import os

from dotenv import load_dotenv
import telebot
from telebot import types
import time
from init_bot import bot
from utils.response_template import (
    ask_threshold_values,
    generate_price_monitor_response,
)
from utils.database_manipulation import (
    retrieve_latest_prices,
    retrieve_prices_n_minutes_back,
    retrieve_latest_news,
    add_user,
    get_monitor_state,
    change_monitor_state,
)


@bot.message_handler(commands=["start", "help"])
@bot.message_handler(func=lambda msg: msg.text is not None and "/" not in msg.text)
def welcome(message):
    add_user(message.chat.id)
    welcome_message = (
        "Welcome to the Crypto Impact Bot!\nBy using me you can track crypto prices  " + \
		"and news, as well as get notifications when various crypto coins move significantly.\n\n" + \
		"You can ask me several commands:\n" +\
		"/get_latest_prices to get latest prices for BTC, ETH, and XRP\n" + \
		"/get_latest_news to get the latest news article about crypto\n" + \
		"/start_monitoring_crypto to monitor prices of crypto coins and getting notified if their returns move above threshold\n" + \
		"/stop_monitoring_crypto to stop monitoring prices" + \
		"Please note that I am still in development and sometimes might produce some weird results. For any bugs please contact my creator at:\n" + \
		"argunovvlad5@gmail.com"
    )
    bot.send_message(message.chat.id, welcome_message, allow_sending_without_reply=True)


### Get latest data ###
#########################################
@bot.message_handler(commands=["get_latest_prices"])
def get_prices(message):
    out_message, out_data = retrieve_latest_prices()
    bot.send_message(message.chat.id, out_message, allow_sending_without_reply=True)


@bot.message_handler(commands=["get_latest_news"])
def get_news(message):
    out_message = retrieve_latest_news()
    bot.send_message(message.chat.id, out_message, allow_sending_without_reply=True)


#########################################

### Monitor Large Changes in assets ###
#########################################
@bot.message_handler(commands=["start_monitoring_crypto"])
def monitor_price_changes(message):
    ask_threshold_values(message.chat.id, "What threshold value do you wish to set?")


@bot.message_handler(commands=["stop_monitoring_crypto"])
def monitor_price_changes(message):
    change_monitor_state(message.chat.id, 0)


@bot.callback_query_handler(
    func=lambda call: call.data
    in ["0 percent", "0.1 percent", "0.5 percent", "1 percent"]
)
def callback_handler(call):
    threshold_value = float(call.data.split()[0])
    bot.send_message(
        call.message.chat.id,
        f"You have chosen {call.data} threshold.\nMonitoring has started!\nYou will be notified if the return of any coin exceeds the return specified by you over the last 10 minutes.",

    )
    change_monitor_state(call.message.chat.id, 1)
    while get_monitor_state(call.message.chat.id) == 1:
        prev_message, previous_prices = retrieve_prices_n_minutes_back(n_minutes=10)
        latest_message, latest_prices = retrieve_latest_prices()
        notify_user, out_message = generate_price_monitor_response(
            previous_prices, latest_prices, threshold_value, time_interval=10
        )
        if notify_user:
            bot.send_message(call.message.chat.id, out_message, time.sleep(60))


#########################################


bot.infinity_polling()
