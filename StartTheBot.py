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


def databaseUpdates(update, context):

	if(update.message.text.startswith('#infected')):
		infectionData = update.message.text.split(' ')
		if(len(infectionData) != 4):
			update.message.reply_text('Invalid format, please try again')
		else:
			replyText = ''
			replyText += 'City : {}\n'.format(infectionData[1])
			replyText += 'Count : {}\n'.format(infectionData[2])
			replyText += 'Link : {}\n'.format(infectionData[3])
			update.message.reply_text(replyText)
	
	elif(update.message.text.startswith('#death')):
		deathData = update.message.text.split(' ')
		if(len(infectionData) != 4):
			update.message.reply_text('Invalid format, please try again')
		else:
			replyText = ''
			replyText += 'City : {}\n'.format(deathData[1])
			replyText += 'Count : {}\n'.format(deathData[2])
			replyText += 'Link : {}\n'.format(deathData[3])
			update.message.reply_text(replyText)

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