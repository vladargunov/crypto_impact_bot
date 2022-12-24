import telebot
from telebot import types

from init_bot import bot
from utils.response_template import ask_yes_no_question


def start_monitoring(message):
    """
    Ask user for what threshold for changes to report
    """
    ask_yes_no_question(
        text="Do you want to start monitoring news?",
        chat_id=message.chat.id,
        callback_yes="monitor_yes",
        callback_no="monitor_no",
    )


def callback_start_monitoring(call):
    """
    Callback on check_registered
    """
    if call.data == "monitor_yes":
        bot.send_message(call.message.chat.id, "Great, now you are connected!")
    elif call.data == "monitor_no":
        bot.send_message(call.message.chat.id, "Ok, see ya later")
