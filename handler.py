from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Emoji
from db import DataBase
from fetch import *
db = DataBase()

def buttons_markup(lang):
	return ReplyKeyboardMarkup([
		[KeyboardButton(strings.buttons[lang][0])],
		[KeyboardButton(strings.buttons[lang][1])],
		[KeyboardButton(strings.buttons[lang][2],request_location=True)],
		[KeyboardButton(strings.buttons[lang][3])]
	])

def days_markup(days, count, id, title):
	if count>0:
		keyboard = []
		if len(days)>1:
			day_buttons = []
			for day in days:
				label, identifier = day
				if lang == "pt-br":
					label = label.replace('-feira','')
				if str(identifier) == 'current':
					label = '« '+label+' »'
				day_buttons.append(InlineKeyboardButton(label,callback_data='1##'+id+'##'+identifier))
			keyboard.append(day_buttons)

		keyboard.append([InlineKeyboardButton(strings.share[lang],switch_inline_query=title)])
		markup = InlineKeyboardMarkup(keyboard)
	else:
		markup = buttons_markup(lang)

	return markup

def start(bot, update):
	uid = update.message.from_user.id
	loc = db.get_loc(uid)
	if loc is None:
		start_markup = ReplyKeyboardMarkup([[KeyboardButton(strings.buttons[lang][2],request_location=True)]])
		bot.sendMessage(uid, text=strings.start[lang], reply_markup=start_markup, parse_mode="Markdown")
	else:
		bot.sendMessage(uid,text=strings.help[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))

def help(bot, update):
	uid = update.message.from_user.id
	bot.sendMessage(uid,text=strings.help[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))

def handle_location(bot, update):
	uid = update.message.from_user.id
	loc = str(update.message.location.latitude)+", "+str(update.message.location.longitude)
	if db.set_loc(uid, loc):
		bot.sendMessage(uid,text=strings.loc_updated[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))
	else:
		bot.sendMessage(uid,text=strings.help[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))

def local(bot, update, args):
	uid = update.message.from_user.id
	if len(args)==0:
		bot.sendMessage(uid,text=strings.loc_empty[lang], parse_mode="Markdown")
	else:
		if db.set_loc(uid, " ".join(args)):
			bot.sendMessage(uid,text=strings.loc_updated[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))
		else:
			bot.sendMessage(uid,text=strings.help[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))

def handle_message(bot, update):
	uid = update.message.from_user.id
	txt = update.message.text
	if txt == strings.buttons[lang][0]:
		selector(bot, update, mode=1)
	elif txt == strings.buttons[lang][1]:
		selector(bot, update, mode=0)
	elif txt == strings.buttons[lang][3]:
		bot.sendMessage(uid,text=strings.help[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))
	else:
		selector(bot, update, mode=2, q=txt)

def selector(bot, update, mode=0, q='', id='', date=0):
	uid = update.message.from_user.id
	loc = db.get_loc(uid)
	if loc is None:
		bot.sendMessage(uid,text=strings.loc_undefined[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))
	else:
		if id!='':
			serial = serialize(loc, id=id)
		else:
			serial = serialize(loc, sort=mode, q=q)
		lista = serial[1:]
		n = len(lista)

		keyboard = []
		if len(lista)>1:
			for item in lista:
				button = InlineKeyboardButton(item["name"],callback_data='0##'+item["id"]+'##0')
				keyboard.append([button])

			if len(keyboard)==0:
				markup = buttons_markup(lang)
				msgtext = strings.no_results[lang]
			else:
				markup = InlineKeyboardMarkup(keyboard)
				msgtext = strings.results[lang]

		else:
			days = serial[0]
			msgtext = cineminha(lista)[0]

			markup = days_markup(days, len(lista), id, q)

		bot.sendMessage(uid,text=msgtext, parse_mode="Markdown", reply_markup=markup)

def handle_callback(bot, update):
	if update.callback_query.data == 'go go go':
		announce(bot, update, None, confirmed=True)
	else:
		uid = update.callback_query.from_user.id
		loc = db.get_loc(uid)
		if loc is None:
			bot.sendMessage(uid,text=strings.loc_undefined[lang], parse_mode="Markdown", reply_markup=buttons_markup(lang))
		else:

			data = update.callback_query.data.split('##')
			mode = int(data[0])
			id = data[1]
			date = data[2]

			serial = serialize(loc, id=id, date=date)

			lista = serial[1:]
			days = serial[0]
			msgtext = cineminha(lista)[0]

			markup = days_markup(days, len(lista), id, lista[0]["name"])

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
	selector(bot, update, mode=1)

def theaters(bot, update):
	selector(bot, update, mode=0)

def announce(bot, update, args, confirmed=False):
	if not confirmed:
		uid = update.message.from_user.id
		if uid == 61407387:
			markup = InlineKeyboardMarkup([[InlineKeyboardButton("GO",callback_data='go go go')]])
			try:
				bot.sendMessage(uid,text=" ".join(args), parse_mode="Markdown", reply_markup=markup, disable_web_page_preview=True)
			except:
				bot.sendMessage(uid,text="Something wrong with your message. Remember:`parse_mode=\"Markdown\"`", parse_mode="Markdown")
	else:
		user_list = db.get_users()
		text = update.callback_query.message.text
		for user in user_list:
			success = False
			while(not success):
				msg = bot.sendMessage(user[0],text=text, parse_mode="Markdown", markup=buttons_markup(lang), disable_web_page_preview=True)
				try:
					success = msg.text == text
				except:
					success = False
					