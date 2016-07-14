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

def atualizar_local(tid, loc):
	db.cur.execute("SELECT * FROM users WHERE id="+tid)
	if db.cur.fetchone() is None:
		db.cur.execute("INSERT INTO users VALUES ("+tid+", "+loc+");")
	else:
		db.cur.execute("UPDATE users SET location="+loc+" WHERE id="+tid+";")
	db.conn.commit()

def start(bot, update):
	button = KeyboardButton(Emoji.ROUND_PUSHPIN+" Enviar localização",request_location=True)
	keyboard = [[button]]
	rep_markup = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
	bot.sendMessage(update.message.chat_id, text=start_text, reply_markup=rep_markup)

def location(bot, update):
	tid = str(update.message.from_user.id)
	loc = "'"+str(update.message.location.latitude)+", "+str(update.message.location.longitude)+"'"
	atualizar_local(tid, loc)
	bot.sendMessage(update.message.chat_id,text=local_atualizado_text)

def local(bot, update, args):
	if len(args)==0:
		bot.sendMessage(update.message.chat_id,text=local_vazio_text)
	else:
		tid = str(update.message.from_user.id)
		loc = "'"+" ".join(args)+"'"
		atualizar_local(tid, loc)
		bot.sendMessage(update.message.chat_id,text=local_atualizado_text)

def filmes(bot, update):
	bot.sendMessage(update.message.chat_id,text='Hello '+update.message.from_user.first_name)

def cinemas(bot, update):
	bot.sendMessage(update.message.chat_id,text='Hello '+update.message.from_user.first_name)

def pesquisar(bot, update):
	bot.sendMessage(update.message.chat_id,text='Hello '+update.message.from_user.first_name)

def feedback(bot, update, args):
	bot.sendMessage(61407387,text='Feedback (@cineminha_bot): '+" ".join(args))

def query(bot, update, args):
	db.cur.execute(" ".join(args))
	response = db.cur.fetchall()
	text = ''
	for i in response:
		text += str(i) + '\n'
	bot.sendMessage(update.message.chat_id,text=text,parse_mode='Markdown')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler([Filters.location], location))
updater.dispatcher.add_handler(CommandHandler('local', local, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('filmes', filmes))
updater.dispatcher.add_handler(CommandHandler('cinemas', cinemas))
updater.dispatcher.add_handler(CommandHandler('pesquisar', pesquisar))
updater.dispatcher.add_handler(CommandHandler('feedback', feedback, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('query', query, pass_args=True))

updater.idle()