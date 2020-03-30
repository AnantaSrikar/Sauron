from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from datetime import datetime
from utils import pushToSheet, scoreManager

markdown = "Markdown" # just telegram API things, will be used below to reply to a user's message

tokens = []  # the token for the bot to run and the url for editing the sheet, secrets

def getTokens():
	fileManager = open('res/TOKENS.txt', 'r')  
	tokenText = fileManager.read()
	tokens = tokenText.split('\n') # tokens[0] = token for bot, token[1] = url for editing sheet, gitigored the file
	return tokens

def get_dateTime():
	date = datetime.now().strftime("%d/%m/20%y")
	time = datetime.now().strftime("%H:%M")
	return [date, time]

tokens = getTokens()

def start(update, context): # this will be a command, invoked by /start, message replied will as below
	update.message.reply_text("Hey there {}! I'm still awake! Try /help for more intel.".format(update.message.from_user.mention_markdown()), parse_mode = markdown)

def help(update, context): # help command, would directly send the reply as in res/bot_intro
	fileManager = open('res/bot_intro.txt', 'r')
	bot_intro = fileManager.read()
	update.message.reply_text(bot_intro)
	fileManager.close()

def databaseUpdates(update, context): # this is the one that handles the regular messages, unlike commands, we have mor econtrol over them
	#update.message gives us the message, and update.message.text gives us the exact text
	#the update.message has more attributes to it like from_user which gives us the user, and more can be done with that
	if(update.message.text.startswith('#infected')): 
		infectionData = update.message.text.split(' ')
		if(len(infectionData) != 5):# infectionData = ['#infected', state, district, count, link]
			update.message.reply_text('Invalid format, please try again') # state district number link
		else:
			# TODO : check if the case already exists
			infectionData.insert(1, get_dateTime()[0])
			infectionData.insert(2, get_dateTime()[1]) # infectionData = ['#infected', date, time, state, district, count, link]
			update.message.reply_text(pushToSheet.infection_update(infectionData))
			scoreManager.updatePoints(update.message.from_user.id, update.message.from_user.full_name)

	elif(update.message.text.startswith('#death')): # similar to #infected (sorry for being lazy)
		deathData = update.message.text.split(' ')
		if(len(deathData) != 5):
			update.message.reply_text('Invalid format, please try again')
		else:
			# TODO : check if the case already exists
			deathData.insert(1, get_dateTime()[0])
			deathData.insert(2, get_dateTime()[1])
			update.message.reply_text(pushToSheet.death_update(deathData))
			scoreManager.updatePoints(update.message.from_user.id, update.message.from_user.full_name)

	elif(update.message.text.startswith('#reportError')): #this still has ti be made (I need help)
		# TODO : add report error feature
		update.message.reply_text('Hol up {}! This feature is being made'.format(update.message.from_user.mention_markdown()), parse_mode = markdown)
	
	elif(update.message.text.startswith('#districtList')): #replies with the districts.txt document
		#context.bot gives us the bot, another way of sending messages, but needs more arguments, so I generally avoid it
		context.bot.send_document(update.message.chat.id, document = open('res/districts.txt', 'rb'), reply_to_message_id = update.message.message_id)

	elif(update.message.text.startswith('#getLink')): #send the link, will change it to view only link once in action
		# TODO : send a 'view only' link
		update.message.reply_text('This is the link : {}'.format(tokens[1]))
	
	elif(update.message.text.startswith('#leaderBoard')): # this will reply with the leaderboard, almost done
		# TODO : show the leaderboard
		update.message.reply_text(scoreManager.getLeaderBoard())
		#update.message.reply_text('Hol up {}! This feature is being made'.format(update.message.from_user.mention_markdown()), parse_mode = markdown)
	
	elif(update.message.text.startswith('#')): #i nvalid use of #, ex : #infection instead of #infected will send this
		update.message.reply_text("Yo what?! {} Please check what you've entered! Try /help for more intel".format(update.message.from_user.mention_markdown()), parse_mode = markdown)

	elif ('ok boomer' in update.message.text.lower() or 'boomer' in update.message.text.lower()): # just an easter egg ;)
		context.bot.send_photo(update.message.chat.id, photo = open('res/ok_boomer.jpg', 'rb'), reply_to_message_id = update.message.message_id)

def main():

	getTokens()
	global tokens

	updater = Updater(token = tokens[0], use_context = True)  # telgram API thing

	dispatcher = updater.dispatcher # this too

	dispatcher.add_handler(CommandHandler('start', start)) #for adding a command, we need to do this, start is the function declared above
	dispatcher.add_handler(CommandHandler('help', help)) # similarly for help, the string is the command that invokes the function
	dispatcher.add_handler(MessageHandler(Filters.text, databaseUpdates)) # for all messages

	print('Bot started running!')

	updater.start_polling() # Starts the bot

	updater.idle() # Stops the bot gracefully

if __name__ == '__main__':
	main()