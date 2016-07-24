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

location_button = KeyboardButton(Emoji.ROUND_PUSHPIN+" Enviar localização",request_location=True)
cinemas_button = KeyboardButton(Emoji.MOVIE_CAMERA+" Listar cinemas")
filmes_button = KeyboardButton(Emoji.CLAPPER_BOARD+" Listar filmes")
pesquisar_button = KeyboardButton(Emoji.RIGHT_POINTING_MAGNIFYING_GLASS+" Pesquisar")
keyboard = [[cinemas_button],[filmes_button],[pesquisar_button],[location_button]]
buttons_markup = ReplyKeyboardMarkup(keyboard)

def start(bot, update):
	start_markup = ReplyKeyboardMarkup([[location_button]],one_time_keyboard=True)
	bot.sendMessage(update.message.chat_id, text=start_text, reply_markup=start_markup, parse_mode="Markdown")

def ajuda(bot, update):
	bot.sendMessage(update.message.chat_id,text=help_text, parse_mode="Markdown", reply_markup=buttons_markup)

def handle_location(bot, update):
	loc = "'"+str(update.message.location.latitude)+", "+str(update.message.location.longitude)+"'"
	db.atualizar_local(update.message.from_user.id, loc)
	bot.sendMessage(update.message.chat_id,text=local_atualizado_text, parse_mode="Markdown", reply_markup=buttons_markup)

def local(bot, update, args):
	if len(args)==0:
		bot.sendMessage(update.message.chat_id,text=local_vazio_text, parse_mode="Markdown")
	else:
		db.atualizar_local(update.message.from_user.id, "'"+" ".join(args)+"'")
		bot.sendMessage(update.message.chat_id,text=local_atualizado_text, parse_mode="Markdown", reply_markup=buttons_markup)

def handle_message(bot, update):
	txt = update.message.text
	if txt == Emoji.MOVIE_CAMERA + " Listar cinemas":
		listar(bot, update, mode=0)
	elif txt == Emoji.CLAPPER_BOARD + " Listar filmes":
		listar(bot, update, mode=1)
	elif txt == Emoji.RIGHT_POINTING_MAGNIFYING_GLASS + " Pesquisar":
		bot.sendMessage(update.message.chat_id,text=pesquisar_text, parse_mode="Markdown")
	else:
		listar(bot, update, mode=2, q=txt)

def listar(bot, update, mode=0, q='', date=0):
	print("listar")
	if update.callback_query is None:
		print("no callback")
		uid = update.message.from_user.id
		sel=0
		edit=False
	else:
		print("callback found")
		uid = update.callback_query.message.from_user.id
		data = update.callback_query.data.split('#')
		mode = int(data[0])
		sel = int(data[1])
		q = data[2]
		edit=True
	print(uid)
	print(mode)
	print(sel)
	print(q)

	loc = db.get_user_location(uid)
	if loc is None:
		bot.sendMessage(update.message.chat_id,text=local_nao_definido, parse_mode="Markdown", reply_markup=buttons_markup)
	else:
		print(loc)
		serial = serialize(loc,sort=mode,q=q,date=date)
		lista = serial[1:]
		days = serial[0]
		n = len(lista)

		if sel<0:
			sel = 0
		if sel>=n:
			sel = n-1
		print(n)
		if n > 1:
			ante = InlineKeyboardButton('◀',callback_data=str(mode)+'#'+str(sel-1)+'#'+q)
			atual = InlineKeyboardButton(str(sel+1)+'/'+str(n),switch_inline_query=lista[sel]["name"])
			prox = InlineKeyboardButton('▶',callback_data=str(mode)+'#'+str(sel+1)+'#'+q)
			keyboard = [[ante, atual, prox]]
			markup = InlineKeyboardMarkup(keyboard)
		else:
			markup = buttons_markup
		print("hello!")
		msgtext = cineminha(lista)[sel]

		if edit:
			print("Edit!")
			print(uid)
			print(update.callback_query.message.message_id)
			a = bot.editMessageText(text=msgtext, chat_id=uid, message_id=update.callback_query.message.message_id,parse_mode="Markdown", reply_markup=inlinemarkup)
			if a!=True:
				print(a.text)
			else:
				print("True!")
		else:
			print("not Edit!")
			bot.sendMessage(update.message.chat_id,text=msgtext, parse_mode="Markdown", reply_markup=markup)

def handle_callback(bot, update):
	print("callback received")
	listar(bot, update)

def handle_inline(bot, update):
	loc = db.get_user_location(update.inline_query.from_user.id)
	results = inline(loc, update.inline_query.query)
	bot.answerInlineQuery(update.inline_query.id, results=results, is_personal=True)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', ajuda))
updater.dispatcher.add_handler(CommandHandler('local', local, pass_args=True))
updater.dispatcher.add_handler(MessageHandler([Filters.location], handle_location))
updater.dispatcher.add_handler(MessageHandler([Filters.text], handle_message))
updater.dispatcher.add_handler(CallbackQueryHandler(handle_callback))
updater.dispatcher.add_handler(InlineQueryHandler(handle_inline))

updater.idle()
