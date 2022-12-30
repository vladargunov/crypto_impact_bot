import os

import time

from utils.response_template import (
    generate_price_monitor_response,
)
from utils.database_manipulation import (
    retrieve_latest_prices,
    retrieve_prices_n_minutes_back,
    retrieve_latest_news,
)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from dotenv import load_dotenv

# Load env parameters
load_dotenv()

API_KEY = os.getenv("API_KEY")  # from .env

updater = Updater(token=API_KEY, use_context=True)
dispatcher = updater.dispatcher

# Welcome message
def start(update, context):
    chat_id = update.effective_chat.id
    welcome_message = (
        "Welcome to the Crypto Impact Bot!\nBy using me you can track crypto prices  "
        + "and news, as well as get notifications when various crypto coins move significantly.\n\n"
        + "You can ask me several commands:\n"
        + "/get_latest_prices to get latest prices for BTC, ETH, and XRP\n"
        + "/get_latest_news to get the latest news article about crypto\n"
        + "/start_monitoring_crypto to monitor prices of crypto coins and getting notified if their returns move above threshold\n"
        + "Please note that I am still in development and sometimes might produce some weird results. For any bugs please contact my creator at:\n"
        + "argunovvlad5@gmail.com"
    )
    context.bot.send_message(chat_id=chat_id, text=welcome_message)


### Get latest data ###
#########################################


def get_latest_prices(update, context):
    chat_id = update.effective_chat.id
    out_message, _ = retrieve_latest_prices()
    context.bot.send_message(chat_id=chat_id, text=out_message)


def get_latest_news(update, context):
    chat_id = update.effective_chat.id
    out_message = retrieve_latest_news()
    context.bot.send_message(chat_id=chat_id, text=out_message)


# #########################################

# ### Monitor Large Changes in assets ###
# #########################################
def start_monitoring_crypto(update, context):
    """Starts the conversation and asks the user about their gender."""
    # Setting threshold value
    keyboard = [
        [
            InlineKeyboardButton("0 %", callback_data="0 p"),
            InlineKeyboardButton("0.1 %", callback_data="0.1 p"),
            InlineKeyboardButton("0.5 %", callback_data="0.5 p"),
            InlineKeyboardButton("1 %", callback_data="1 p"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "What threshold value do you wish to set?", reply_markup=reply_markup
    )

    # Setting time interval value
    keyboard = [
        [
            InlineKeyboardButton("5 minutes", callback_data="5 m"),
            InlineKeyboardButton("10 minutes", callback_data="10 m"),
            InlineKeyboardButton("15 minutes", callback_data="15 m"),
            InlineKeyboardButton("20 minutes", callback_data="20 m"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "What time interval value do you wish to set?", reply_markup=reply_markup
    )


def callback_reply(update, context):
    """
    Store context provided by user
    """
    query = update.callback_query
    if query.data in ["0 p", "0.1 p", "0.5 p", "1 p"]:
        # Store value of threshold
        context.user_data["threshold"] = float(query.data.split()[0])
        query.edit_message_text(
            f"You have chosen {context.user_data['threshold']} % price threshold.\n Please also set time interval below."
        )
    elif query.data in ["5 m", "10 m", "15 m", "20 m"]:
        # Store value of time interval
        context.user_data["time_interval"] = int(query.data.split()[0])
        query.edit_message_text(
            f"You have chosen {context.user_data['time_interval']} % time interval.\n Call command /check_movement to see latest updates."
        )


def check_movement(update, context):
    chat_id = update.effective_chat.id
    _, previous_prices = retrieve_prices_n_minutes_back(
        n_minutes=int(context.user_data["time_interval"])
    )
    _, latest_prices = retrieve_latest_prices()
    out_message = generate_price_monitor_response(
        previous_prices,
        latest_prices,
        context.user_data["threshold"],
        time_interval=context.user_data["time_interval"],
    )

    context.bot.send_message(chat_id, out_message)


# #########################################


# Set the commands
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("get_latest_prices", get_latest_prices))
dispatcher.add_handler(CommandHandler("get_latest_news", get_latest_news))
dispatcher.add_handler(
    CommandHandler("start_monitoring_crypto", start_monitoring_crypto)
)
dispatcher.add_handler(CallbackQueryHandler(callback_reply))
dispatcher.add_handler(CommandHandler("check_movement", check_movement))

updater.start_polling()
