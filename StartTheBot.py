from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from utils import pushToSheet

markdown = "Markdown"

tokens = []

def getTokens():
	fileManager = open('res/TOKENS.txt', 'r')  
	tokenText = fileManager.read()
	tokens = tokenText.split('\n')
	return tokens

tokens = getTokens()

def start(update, context):
	update.message.reply_text("Hey there {}! I'm still awake".format(update.message.from_user.mention_markdown()), parse_mode = markdown)

def databaseUpdates(update, context):

	if(update.message.text.startswith('#infected')):
		infectionData = update.message.text.split(' ')
		if(len(infectionData) != 7):
			update.message.reply_text('Invalid format, please try again') # date time state district number link
		else:
			update.message.reply_text(pushToSheet.infection_update(infectionData))
			
	
	elif(update.message.text.startswith('#death')):
		print('Got the death')
		deathData = update.message.text.split(' ')
		if(len(deathData) != 7):
			update.message.reply_text('Invalid format, please try again')
		else:
			update.message.reply_text(pushToSheet.death_update(deathData))

def main():

	getTokens()
	global tokens

	updater = Updater(token = tokens[0], use_context = True)

	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler('start', start))
	dispatcher.add_handler(MessageHandler(Filters.text, databaseUpdates))

	print('Bot started running!')

	updater.start_polling() # Starts the bot

	updater.idle() # Stops the bot gracefully

if __name__ == '__main__':
	main()