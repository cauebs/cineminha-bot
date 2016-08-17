import os, logging, strings
from telegram.ext import Updater, CommandHandler, MessageHandler, InlineQueryHandler, CallbackQueryHandler, Filters
from handler import *

log_level = os.environ.get('LOGLEVEL')
if log_level == 'debug':
	logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
elif log_level == 'info':
	logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TOKEN = os.environ.get('TOKEN')
APPNAME = os.environ.get('APPNAME')
lang = os.environ.get('lang')
PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(TOKEN)
#updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
updater.bot.setWebhook()#"https://"+APPNAME+".herokuapp.com/"+TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler(strings.command[lang][0], movies))
updater.dispatcher.add_handler(CommandHandler(strings.command[lang][1], theaters))
updater.dispatcher.add_handler(CommandHandler(strings.command[lang][2], help))
updater.dispatcher.add_handler(CommandHandler('local', local, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('announce', announce, pass_args=True))

updater.dispatcher.add_handler(MessageHandler([Filters.location], handle_location))
updater.dispatcher.add_handler(MessageHandler([Filters.text], handle_message))

updater.dispatcher.add_handler(CallbackQueryHandler(handle_callback))
updater.dispatcher.add_handler(InlineQueryHandler(handle_inline))

updater.start_polling()
updater.idle()
