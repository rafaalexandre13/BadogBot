from decouple import config
from telegram import Bot
from telegram.ext import CommandHandler, Updater

BOTTOKEN = config('BOTTOKEN')
bot = Bot(BOTTOKEN)
updater = Updater(BOTTOKEN)
