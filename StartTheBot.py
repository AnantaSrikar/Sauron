from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from datetime import datetime
from utils import pushToSheet, scoreManager

markdown = "Markdown"

tokens = []

def getTokens():
	fileManager = open('res/TOKENS.txt', 'r')  
	tokenText = fileManager.read()
	tokens = tokenText.split('\n')
	return tokens

def get_dateTime():
	date = datetime.now().strftime("%d/%m/20%y")
	time = datetime.now().strftime("%H:%M")
	return [date, time]

tokens = getTokens()

def start(update, context):
	update.message.reply_text("Hey there {}! I'm still awake! Try /help for more intel.".format(update.message.from_user.mention_markdown()), parse_mode = markdown)

def help(update, context):
	fileManager = open('res/bot_intro.txt', 'r')
	bot_intro = fileManager.read()
	update.message.reply_text(bot_intro)
	fileManager.close()

def databaseUpdates(update, context):

	if(update.message.text.startswith('#infected')): # infectionData = ['#infected', date, time, state, district, count, link]
		infectionData = update.message.text.split(' ')
		if(len(infectionData) != 5):
			update.message.reply_text('Invalid format, please try again') # state district number link
		else:
			# TODO : check if the case already exists
			infectionData.insert(1, get_dateTime()[0])
			infectionData.insert(2, get_dateTime()[1])
			update.message.reply_text(pushToSheet.infection_update(infectionData))
			scoreManager.updatePoints(update.message.from_user.id)

	elif(update.message.text.startswith('#death')):
		deathData = update.message.text.split(' ')
		if(len(deathData) != 5):
			update.message.reply_text('Invalid format, please try again')
		else:
			# TODO : check if the case already exists
			deathData.insert(1, get_dateTime()[0])
			deathData.insert(2, get_dateTime()[1])
			update.message.reply_text(pushToSheet.death_update(deathData))
			scoreManager.updatePoints(update.message.from_user.id)

	elif(update.message.text.startswith('#reportError')):
		update.message.reply_text('Hol up {}! This feature is being made'.format(update.message.from_user.mention_markdown()), parse_mode = markdown)

	elif(update.message.text.startswith('#getLink')):
		update.message.reply_text('This is the link : {}'.format(tokens[1]))
	
	elif(update.message.text.startswith('#')):
		update.message.reply_text("Yo what?! {} please check what you've entered! Try /help for more intel".format(update.message.from_user.mention_markdown()), parse_mode = markdown)

	elif ('ok boomer' in update.message.text.lower() or 'boomer' in update.message.text.lower()):
		context.bot.send_photo(update.message.chat.id, photo = open('res/ok_boomer.jpg', 'rb'), reply_to_message_id = update.message.message_id)

def main():

	getTokens()
	global tokens

	updater = Updater(token = tokens[0], use_context = True)

	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler('start', start))
	dispatcher.add_handler(CommandHandler('help', help))
	dispatcher.add_handler(MessageHandler(Filters.text, databaseUpdates))

	print('Bot started running!')

	updater.start_polling() # Starts the bot

	updater.idle() # Stops the bot gracefully

if __name__ == '__main__':
	main()