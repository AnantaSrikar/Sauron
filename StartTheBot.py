from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

markdown = "Markdown"

tokens = []

def getTokens():
	fileManager = open('res/TOKENS.txt', 'r')  
	tokenText = fileManager.read()
	global tokens
	tokens = tokenText.split('\n')

def start(update, context):
	update.message.reply_text("Hey there {}! I'm still awake".format(update.message.from_user.mention_markdown()), parse_mode = markdown)

def main():

	getTokens()
	global tokens

	updater = Updater(token = tokens[0], use_context = True)

	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler('start', start))

	updater.start_polling() # Starts the bot

	updater.idle() # Stops the bot gracefully

if __name__ == '__main__':
	main()