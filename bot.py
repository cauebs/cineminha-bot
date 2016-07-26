import os, logging
from telegram.ext import Updater, CommandHandler, MessageHandler, InlineQueryHandler, CallbackQueryHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Emoji, ForceReply
from db import DataBase
from fetch import *
from textos import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s(%(lineno)d) - %(message)s',level=logging.INFO)

TOKEN = os.environ.get('TOKEN')
APPNAME = os.environ.get('APPNAME')
PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(TOKEN)
updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
updater.bot.setWebhook("https://"+APPNAME+".herokuapp.com/"+TOKEN)

db = DataBase()

filmes_button = KeyboardButton(Emoji.CLAPPER_BOARD+" Listar filmes")
cinemas_button = KeyboardButton(Emoji.MOVIE_CAMERA+" Listar cinemas")
pesquisar_button = KeyboardButton(Emoji.RIGHT_POINTING_MAGNIFYING_GLASS+" Pesquisar")
location_button = KeyboardButton(Emoji.ROUND_PUSHPIN+" Enviar localização",request_location=True)
keyboard = [[filmes_button],[cinemas_button],[pesquisar_button],[location_button]]
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
		bot.sendMessage(update.message.chat_id,text=pesquisar_text, parse_mode="Markdown", reply_markup=ForceReply(force_reply=True))
	else:
		listar(bot, update, mode=2, q=txt)

def listar(bot, update, mode=0, q=''):
	uid = update.message.from_user.id
	loc = db.get_user_location(uid)
	if loc is None:
		bot.sendMessage(update.message.chat_id,text=local_nao_definido, parse_mode="Markdown", reply_markup=buttons_markup)
	else:

		serial = serialize(loc,sort=mode,q=q)
		lista = serial[1:]
		n = len(lista)

		keyboard = []

		for item in lista:
			button = InlineKeyboardButton(item["name"],callback_data=str(0)+'#'+item["name"]+'#0')
			keyboard.append([button])

		if len(keyboard)==0:
			markup = buttons_markup
			msgtext = '*Não foi encontrado nenhum resultado.*\nTente outra coisa ou atualize sua localização'
		else:
			markup = InlineKeyboardMarkup(keyboard)
			msgtext = 'Selecione um para obter mais informações:'

		bot.sendMessage(update.message.chat_id,text=msgtext, parse_mode="Markdown", reply_markup=markup)

def handle_callback(bot, update):

	uid = update.callback_query.from_user.id
	loc = db.get_user_location(uid)
	if loc is None:
		bot.sendMessage(update.message.chat_id,text=local_nao_definido, parse_mode="Markdown", reply_markup=buttons_markup)
	else:

		data = update.callback_query.data.split('#')
		mode = int(data[0])
		q = data[1]
		date = data[2]

		serial = serialize(loc,q=q, date=date)
		lista = serial[1:]
		days = serial[0]
		msgtext = cineminha(lista)[0]

		if len(days)>1:
			buttons = []
			for day in days:
				day_number = str(days.index(day))
				if day_number == date:
					label = '« '+day.replace('-feira','')+' »'
				else:
					label = day.replace('-feira','')
				buttons.append(InlineKeyboardButton(label,callback_data=str(1)+'#'+q+'#'+day_number))
			markup = InlineKeyboardMarkup([buttons])
		else:
			markup = buttons_markup

		if mode==0:
			bot.sendMessage(uid,text=msgtext, parse_mode="Markdown", reply_markup=markup)
		elif mode==1:
			bot.editMessageText(text=msgtext, chat_id=uid, message_id=update.callback_query.message.message_id,parse_mode="Markdown", reply_markup=markup)

def handle_inline(bot, update):
	loc = db.get_user_location(update.inline_query.from_user.id)
	results = inline(loc, update.inline_query.query)
	bot.answerInlineQuery(update.inline_query.id, results=results, is_personal=True)

def announce(bot, update, args):
	if update.message.from_user.id == 61407387:
		msg = " ".join(args)
		db.cur.execute("SELECT id FROM users")
		lista = db.cur.fetchall()
		for user in lista:
			bot.sendMessage(user[0],text=msg,parse_mode="Markdown",disable_notification=True,reply_markup=buttons_markup)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', ajuda))
updater.dispatcher.add_handler(CommandHandler('local', local, pass_args=True))
updater.dispatcher.add_handler(MessageHandler([Filters.location], handle_location))
updater.dispatcher.add_handler(MessageHandler([Filters.text], handle_message))
updater.dispatcher.add_handler(CallbackQueryHandler(handle_callback))
updater.dispatcher.add_handler(InlineQueryHandler(handle_inline))
updater.dispatcher.add_handler(CommandHandler('announce', announce, pass_args=True))
updater.idle()