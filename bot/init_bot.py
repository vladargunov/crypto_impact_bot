import os

from dotenv import load_dotenv
import telebot

# Load env parameters
load_dotenv()

API_KEY = os.getenv("API_KEY")  # from .env

# Start TeleBot
bot = telebot.TeleBot(API_KEY, parse_mode=None)
