import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton, Emoji
from textos import *
from db import DataBase

TOKEN = os.environ.get('TOKEN')
APPNAME = os.environ.get('APPNAME')

PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(TOKEN)
updater.start_webhook(listen="0.0.0.0",
					  port=PORT,
					  url_path=TOKEN)
updater.bot.setWebhook("https://"+APPNAME+".herokuapp.com/"+TOKEN)

db = DataBase()

def start(bot, update):
	tid = update.message.from_user.id
	#if db.curr.execute("SELECT location FROM users WHERE "+tid)
	button = KeyboardButton(Emoji.ROUND_PUSHPIN+" Enviar localização",request_location=True)
	keyboard = [[button]]
	rep_markup = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
	bot.sendMessage(update.message.chat_id, text=starttext, reply_markup=rep_markup)

def location(bot, update):
	tid = update.message.from_user.id
	loc = str(update.message.location.latitude)+", "+str(update.message.location.longitude)
	db.curr.execute("INSERT INTO users VALUES ("+tid+", "+loc+");")

def filmes(bot, update):
	bot.sendMessage(update.message.chat_id,text='Hello '+update.message.from_user.first_name)

def cinemas(bot, update):
	bot.sendMessage(update.message.chat_id,text='Hello '+update.message.from_user.first_name)

def pesquisar(bot, update):
	bot.sendMessage(update.message.chat_id,text='Hello '+update.message.from_user.first_name)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('filmes', filmes))
updater.dispatcher.add_handler(CommandHandler('cinemas', cinemas))
updater.dispatcher.add_handler(CommandHandler('pesquisar', pesquisar))
updater.dispatcher.add_handler(MessageHandler([Filters.location], location))

updater.idle()