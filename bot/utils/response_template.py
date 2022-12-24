from telebot import types
from init_bot import bot


def generate_yes_no_markup(callback_yes="cb_yes", callback_no="cb_no"):
    """
    Generates markup with yes or no answers
    """
    markup = types.InlineKeyboardMarkup(row_width=1)
    yes = types.InlineKeyboardButton(text="Yes", callback_data=callback_yes)
    no = types.InlineKeyboardButton(text="No", callback_data=callback_no)
    markup.add(yes, no)
    return markup


def ask_yes_no_question(text, chat_id, callback_yes="cb_yes", callback_no="cb_no"):
    """
    Asks question with possible answers yes or no
    and predefined callback
    """
    markup = generate_yes_no_markup(callback_yes, callback_no)
    bot.send_message(chat_id, text, reply_markup=markup)


def generate_threshold_markup():
    """
    Generates markup for 3 possible thresholds: 1,2,5 percent
    """
    markup = types.InlineKeyboardMarkup(row_width=1)
    percent_0 = types.InlineKeyboardButton(text="0 %", callback_data="0 percent")
    percent_1 = types.InlineKeyboardButton(text="0.1 %", callback_data="0.1 percent")
    percent_2 = types.InlineKeyboardButton(text="0.5 %", callback_data="0.5 percent")
    percent_5 = types.InlineKeyboardButton(text="1 %", callback_data="1 percent")
    markup.add(percent_0, percent_1, percent_2, percent_5)
    return markup


def ask_threshold_values(chat_id, text):
    """
    Asks which threshold to set for price monitoring
    """
    markup = generate_threshold_markup()
    bot.send_message(chat_id, text, reply_markup=markup)


def generate_price_monitor_response(
    previous_prices, current_prices, threshold, time_interval
):
    out_str = ""
    for name_asset in previous_prices.keys():
        price_return = current_prices[name_asset] / previous_prices[name_asset] - 1
        if price_return > threshold / 100:
            out_str += f"{name_asset} return is more than {threshold} percent\n"
            out_str += f"{name_asset} current price is {current_prices[name_asset]} \n"
            out_str += f"{name_asset} price {time_interval} minutes ago is {previous_prices[name_asset]} \n"
            out_str += "##################\n"
        elif price_return < -threshold / 100:
            out_str += f"{name_asset} return is less than{threshold} percent\n"
            out_str += f"{name_asset} current price is {current_prices[name_asset]} \n"
            out_str += f"{name_asset} price {time_interval} minutes ago is {previous_prices[name_asset]} \n"
            out_str += "##################\n"
    if out_str != "":
        notify_user = True
    else:
        notify_user = False
    return notify_user, out_str
