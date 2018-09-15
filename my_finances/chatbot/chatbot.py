from decouple import config
from telegram import Bot
from telegram import ParseMode
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.ext import CallbackQueryHandler as CallbkQueHand
from telegram.ext import ConversationHandler as ConvHand
from my_finances import ocr
from my_finances.database_manage import Database

BOTTOKEN = config('BOTTOKEN')
bot = Bot(BOTTOKEN)
updater = Updater(BOTTOKEN)

