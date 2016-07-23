import os
from telegram.ext import Updater, CommandHandler, MessageHandler, InlineQueryHandler, CallbackQueryHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Emoji
from db import DataBase
from fetch import *
from textos import *

TOKEN = os.environ.get('TOKEN')
APPNAME = os.environ.get('APPNAME')

PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(TOKEN)
updater.start_webhook(listen="0.0.0.0",
					  port=PORT,
					  url_path=TOKEN)
updater.bot.setWebhook("https://"+APPNAME+".herokuapp.com/"+TOKEN)

db = DataBase()

location_button = KeyboardButton(Emoji.ROUND_PUSHPIN+" Atualizar localização",request_location=True)
cinemas_button = KeyboardButton(Emoji.MOVIE_CAMERA+" Listar cinemas")
filmes_button = KeyboardButton(Emoji.CLAPPER_BOARD+" Listar filmes")
pesquisar_button = KeyboardButton(Emoji.RIGHT_POINTING_MAGNIFYING_GLASS+" Pesquisar")
keyboard = [[cinemas_button],[filmes_button],[pesquisar_button],[location_button]]
rep_markup = ReplyKeyboardMarkup(keyboard)

def start(bot, update):
	location_button = KeyboardButton(Emoji.ROUND_PUSHPIN+" Enviar localização",request_location=True)
	keyboard = [[location_button]]
	start_markup = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
	bot.sendMessage(update.message.chat_id, text=start_text, reply_markup=start_markup, parse_mode="Markdown")

def ajuda(bot, update):
	bot.sendMessage(update.message.chat_id,text=help_text, parse_mode="Markdown")

def handle_location(bot, update):
	tid = str(update.message.from_user.id)
	loc = "'"+str(update.message.location.latitude)+", "+str(update.message.location.longitude)+"'"
	bot.sendMessage(update.message.chat_id,text=local_atualizado_text, parse_mode="Markdown", reply_markup=rep_markup)
	db.atualizar_local(tid, loc)

def local(bot, update, args):
	if len(args)==0:
		bot.sendMessage(update.message.chat_id,text=local_vazio_text, parse_mode="Markdown")
	else:
		tid = str(update.message.from_user.id)
		loc = "'"+" ".join(args)+"'"
		bot.sendMessage(update.message.chat_id,text=local_atualizado_text, parse_mode="Markdown", reply_markup=rep_markup)
		db.atualizar_local(tid, loc)

def filmes(bot, update, sel=0):
	loc = db.get_user_location(update.message.from_user.id)
	if loc is None:
		bot.sendMessage(update.message.chat_id,text=local_nao_definido, parse_mode="Markdown")
	else:
		lista = serialize(loc,sort=1)[1:]

		if len(lista) > 1:
			if sel<0:
				sel = 0
			if sel>len(lista):
				sel = len(lista)-1
			ante = InlineKeyboardButton('◀',callback_data='f'+str(sel-1))
			atual = InlineKeyboardButton(str(sel+1)+'/'+str(len(lista)),switch_inline_query=lista[sel]["name"])
			prox = InlineKeyboardButton('▶',callback_data='f'+str(sel+1))
			keyboard = [[ante, atual, prox]]
			msgtext = cineminha([lista[sel]])[0]
			inlinemarkup = InlineKeyboardMarkup(keyboard)
			bot.sendMessage(update.message.chat_id,text=msgtext, parse_mode="Markdown", reply_markup=inlinemarkup)

def cinemas(bot, update, sel=0):
	loc = db.get_user_location(update.message.from_user.id)
	if loc is None:
		bot.sendMessage(update.message.chat_id,text=local_nao_definido, parse_mode="Markdown")
	else:
		lista = serialize(loc)[1:]

		if len(lista) > 1:
			if sel<0:
				sel = 0
			if sel>len(lista):
				sel = len(lista)-1
			ante = InlineKeyboardButton('◀',callback_data='c'+str(sel-1))
			atual = InlineKeyboardButton(str(sel+1)+'/'+str(len(lista)),switch_inline_query=lista[sel]["name"])
			prox = InlineKeyboardButton('▶',callback_data='c'+str(sel+1))
			keyboard = [[ante, atual, prox]]
			msgtext = cineminha([lista[sel]])[0]
			inlinemarkup = InlineKeyboardMarkup(keyboard)
			bot.sendMessage(update.message.chat_id,text=msgtext, parse_mode="Markdown", reply_markup=inlinemarkup)

def pesquisar(bot, update, sel=0):
	loc = db.get_user_location(update.message.from_user.id)
	if loc is None:
		bot.sendMessage(update.message.chat_id,text=local_nao_definido, parse_mode="Markdown")
	else:
		for i in cineminha(serialize(loc, q=update.message.text)[1:]):
			bot.sendMessage(update.message.chat_id,text=i, parse_mode="Markdown")

def handle_message(bot, update):
	if update.message.text == Emoji.MOVIE_CAMERA + " Listar cinemas":
		cinemas(bot, update)
	elif update.message.text == Emoji.CLAPPER_BOARD + " Listar filmes":
		filmes(bot, update)
	elif update.message.text == Emoji.RIGHT_POINTING_MAGNIFYING_GLASS + " Pesquisar":
		bot.sendMessage(update.message.chat_id,text=pesquisar_text, parse_mode="Markdown")
	else:
		pesquisar(bot, update)

#def feedback(bot, update, args):
#	bot.sendMessage(61407387,text='Feedback: '+" ".join(args), parse_mode="Markdown")
#	bot.sendMessage(update.message.chat_id,text=feedback_text, parse_mode="Markdown")

def handle_callback(bot, update, update_queue):
	data = update.callback_query.data

	if data[0] == 'c':
		lista = serialize(loc)[1:]

	elif data[0] == 'f':
		lista = serialize(loc,sort=1)[1:]

	sel = int(data[1:])
	chat_id = update.callback_query.from_user.id
	loc = db.get_user_location(chat_id)

	if sel<0:
		sel = 0
	if sel>len(lista):
		sel = len(lista)-1

	ante = InlineKeyboardButton('◀',callback_data=data[0]+str(sel-1))
	atual = InlineKeyboardButton(str(sel+1)+'/'+str(len(lista)),switch_inline_query=lista[sel]["name"])
	prox = InlineKeyboardButton('▶',callback_data=data[0]+str(sel+1))
	keyboard = [[ante, atual, prox]]
	msgtext = cineminha([lista[sel]])[0]

	inlinemarkup = InlineKeyboardMarkup(keyboard)

	bot.editMessageText(text=msgtext, chat_id=chat_id, message_id=update.callback_query.message.message_id,parse_mode="Markdown", reply_markup=inlinemarkup)


def handle_inline(bot, update):
	loc = db.get_user_location(update.inline_query.from_user.id)
	results = inline(loc, update.inline_query.query)
	bot.answerInlineQuery(update.inline_query.id, results=results, is_personal=True)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', ajuda))
updater.dispatcher.add_handler(CommandHandler('local', local, pass_args=True))
#updater.dispatcher.add_handler(CommandHandler('feedback', feedback, pass_args=True))
updater.dispatcher.add_handler(MessageHandler([Filters.location], handle_location))
updater.dispatcher.add_handler(MessageHandler([Filters.text], handle_message))
updater.dispatcher.add_handler(CallbackQueryHandler(handle_callback,pass_update_queue=True))
updater.dispatcher.add_handler(InlineQueryHandler(handle_inline))

updater.idle()
