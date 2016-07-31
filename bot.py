import os, logging, textos
from telegram.ext import Updater, CommandHandler, MessageHandler, InlineQueryHandler, CallbackQueryHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Emoji
from db import DataBase
from fetch import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s(%(lineno)d) - %(message)s',level=logging.INFO)

TOKEN = os.environ.get('TOKEN')
APPNAME = os.environ.get('APPNAME')
lang = os.environ.get('lang')
PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(TOKEN)
updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
updater.bot.setWebhook("https://"+APPNAME+".herokuapp.com/"+TOKEN)

db = DataBase()

def buttons_markup(lang):
	return ReplyKeyboardMarkup([
		[KeyboardButton(textos.buttons[lang][0])],
		[KeyboardButton(textos.buttons[lang][1])],
		[KeyboardButton(textos.buttons[lang][2],request_location=True)],
		[KeyboardButton(textos.buttons[lang][3])]
	])

def start(bot, update):
	uid = update.message.from_user.id
	loc = db.get_loc(uid)
	if loc is None:
		start_markup = ReplyKeyboardMarkup([[KeyboardButton(textos.buttons["pt-br"][2],request_location=True)]])
		bot.sendMessage(uid, text=textos.start[lang], reply_markup=start_markup, parse_mode="Markdown")
	else:
		bot.sendMessage(uid,text=textos.help[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))

def help(bot, update):
	uid = update.message.from_user.id
	bot.sendMessage(uid,text=textos.help[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))

def handle_location(bot, update):
	uid = update.message.from_user.id
	loc = str(update.message.location.latitude)+", "+str(update.message.location.longitude)
	if db.set_loc(uid, loc):
		bot.sendMessage(uid,text=textos.loc_updated[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))
	else:
		bot.sendMessage(uid,text=textos.help[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))

def local(bot, update, args):
	uid = update.message.from_user.id
	if len(args)==0:
		bot.sendMessage(uid,text=textos.loc_empty[lang], parse_mode="Markdown")
	else:
		if db.set_loc(uid, " ".join(args)):
			bot.sendMessage(uid,text=textos.loc_updated[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))
		else:
			bot.sendMessage(uid,text=textos.help[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))

def handle_message(bot, update):
	uid = update.message.from_user.id
	txt = update.message.text
	if txt == textos.buttons[lang][0]:
		listar(bot, update, mode=1)
	elif txt == textos.buttons[lang][1]:
		listar(bot, update, mode=0)
	elif txt == textos.buttons[lang][3]:
		bot.sendMessage(uid,text=textos.help[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))
	else:
		listar(bot, update, mode=2, q=txt)

def listar(bot, update, mode=0, q='', date=0):
	uid = update.message.from_user.id
	loc = db.get_loc(uid)
	if loc is None:
		bot.sendMessage(uid,text=textos.loc_undefined[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))
	else:
		serial = serialize(loc, sort=mode, q=q)
		lista = serial[1:]
		n = len(lista)

		keyboard = []
		if len(lista)>1:
			for item in lista:
				button = InlineKeyboardButton(item["name"],callback_data=str(0)+'#'+item["name"]+'#0')
				keyboard.append([button])

			if len(keyboard)==0:
				markup = buttons_markup(lang)
				msgtext = textos.no_results[lang]
			else:
				markup = InlineKeyboardMarkup(keyboard)
				msgtext = textos.results[lang]

		else:
			days = serial[0]
			msgtext = cineminha(lista)[0]

			if len(days)>1:
				buttons = []
				for day in days:
					day_number = str(days.index(day))
					if lang == "pt-br":
						label = day.replace('-feira','')
					else:
						label = day
					if day_number == date:
						label = '« '+day+' »'
					buttons.append(InlineKeyboardButton(label,callback_data=str(1)+'#'+q+'#'+day_number))
				markup = InlineKeyboardMarkup([buttons])
			else:
				markup = buttons_markup(lang)

		bot.sendMessage(uid,text=msgtext, parse_mode="Markdown", reply_markup=markup)

def handle_callback(bot, update):
	uid = update.callback_query.from_user.id
	loc = db.get_loc(uid)
	if loc is None:
		bot.sendMessage(uid,text=textos.loc_undefined[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))
	else:

		data = update.callback_query.data.split('#')
		mode = int(data[0])
		q = data[1]
		date = data[2]

		serial = serialize(loc, q=q, date=date)
		lista = serial[1:]
		days = serial[0]
		msgtext = cineminha(lista)[0]

		if len(days)>1:
			buttons = []
			for day in days:
				day_number = str(days.index(day))
				if lang == "pt-br":
					label = day.replace('-feira','')
				else:
					label = day
				if day_number == date:
					label = '« '+day+' »'
				buttons.append(InlineKeyboardButton(label,callback_data=str(1)+'#'+q+'#'+day_number))
			markup = InlineKeyboardMarkup([buttons])
		else:
			markup = buttons_markup(lang)

		if mode==0:
			bot.sendMessage(uid,text=msgtext, parse_mode="Markdown", reply_markup=markup)
		elif mode==1:
			bot.editMessageText(text=msgtext, chat_id=uid, message_id=update.callback_query.message.message_id,parse_mode="Markdown", reply_markup=markup)

def handle_inline(bot, update):
	uid = update.inline_query.from_user.id
	loc = db.get_loc(uid)
	results = inline(loc, update.inline_query.query, lang)
	bot.answerInlineQuery(update.inline_query.id, results=results, is_personal=True)

def movies(bot, update):
	listar(bot, update, mode=1)

def theaters(bot, update):
	listar(bot, update, mode=0)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler(textos.command[lang][0], movies))
updater.dispatcher.add_handler(CommandHandler(textos.command[lang][1], theaters))
updater.dispatcher.add_handler(CommandHandler(textos.command[lang][2], help))
updater.dispatcher.add_handler(CommandHandler('local', local, pass_args=True))

updater.dispatcher.add_handler(MessageHandler([Filters.location], handle_location))
updater.dispatcher.add_handler(MessageHandler([Filters.text], handle_message))

updater.dispatcher.add_handler(CallbackQueryHandler(handle_callback))
updater.dispatcher.add_handler(InlineQueryHandler(handle_inline))

updater.idle()