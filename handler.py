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

def location(bot, update):
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

def filmes(bot, update):
	loc = db.get_user_location(update.message.from_user.id)
	if loc is None:
		bot.sendMessage(update.message.chat_id,text=local_nao_definido, parse_mode="Markdown")
	else:
		for i in fetch.cineminha(fetch.serialize(loc, sort=1)[1:]):
			bot.sendMessage(update.message.chat_id,text=i, parse_mode="Markdown")

def cinemas(bot, update):
	loc = db.get_user_location(update.message.from_user.id)
	if loc is None:
		bot.sendMessage(update.message.chat_id,text=local_nao_definido, parse_mode="Markdown")
	else:
		for i in fetch.cineminha(fetch.serialize(loc)[1:]):
			bot.sendMessage(update.message.chat_id,text=i, parse_mode="Markdown")

def pesquisar(bot, update):
	loc = db.get_user_location(update.message.from_user.id)
	if loc is None:
		bot.sendMessage(update.message.chat_id,text=local_nao_definido, parse_mode="Markdown")
	else:
		for i in fetch.cineminha(fetch.serialize(loc, q=update.message.text)[1:]):
			bot.sendMessage(update.message.chat_id,text=i, parse_mode="Markdown")

def messages(bot, update):
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

def inline(bot, update):
	loc = db.get_user_location(update.inline_query.from_user.id)
	results = fetch.inline(loc, update.inline_query.query)
	bot.answerInlineQuery(update.inline_query.id, results=results, is_personal=True)