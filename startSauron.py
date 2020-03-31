from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from datetime import datetime
import schedule
import time
import logging
from utils import pushToSheet, scoreManager
from utils.validateDetails import refreshDataList

logging.basicConfig(filename = 'res/complete.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

markdown = "Markdown" # just telegram API things, will be used below to reply to a user's message

tokens = []  # the token for the bot to run and the url for editing the sheet, secrets

def getTokens():
	fileManager = open('res/TOKENS.txt', 'r')  
	tokenText = fileManager.read()
	tokens = tokenText.split('\n') # tokens[0] = token for bot, token[1] = url for editing sheet, gitigored the file
	return tokens

def job():
	print('Hey, its gonna work')

def get_dateTime():
	date = datetime.now().strftime("%d/%m/20%y")
	time = datetime.now().strftime("%H:%M")
	return [date, time]

tokens = getTokens()

def start(update, context): # this will be a command, invoked by /start, message replied will as below
	if(update.message.chat.id != -479059156 and update.message.chat.id != 648854668):
		update.message.reply_text("{} I don't do PMs, come over to the main group".format(update.message.from_user.mention_markdown()), parse_mode = markdown)
	else:
		update.message.reply_text("Hey there {}! I'm still awake! Try /help for more intel.".format(update.message.from_user.mention_markdown()), parse_mode = markdown)

def help(update, context): # help command, would directly send the reply as in res/bot_intro
	if(update.message.chat.id != -479059156 and update.message.chat.id != 648854668):
		update.message.reply_text("{} I don't do PMs, come over to the main group".format(update.message.from_user.mention_markdown()), parse_mode = markdown)
	else:
		fileManager = open('res/bot_intro.txt', 'r')
		bot_intro = fileManager.read()
		update.message.reply_text(bot_intro)
		fileManager.close()
	
def lowerAll(daList):
	for i in range(len(daList)):
		daList[i] = daList[i].lower()

def databaseUpdates(update, context): # this is the one that handles the regular messages, unlike commands, we have mor econtrol over them
	#update.message gives us the message, and update.message.text gives us the exact text
	#the update.message has more attributes to it like from_user which gives us the user, and more can be done with that
	if(update.message.chat.id != -479059156 and update.message.chat.id != 648854668): # TODO : add group link once made
		update.message.reply_text("{} I don't do PMs, come over to the main group".format(update.message.from_user.mention_markdown()), parse_mode = markdown)
	
	else:
		if(update.message.text.startswith('#infected')): 
			infectionData = update.message.text.split(' ')
			lowerAll(infectionData)
			if(len(infectionData) != 5):# infectionData = ['#infected', state, district, count, link]
				update.message.reply_text('Invalid format, please try again') # state district number link
			else:
				infectionData.insert(1, get_dateTime()[0])
				infectionData.insert(2, get_dateTime()[1]) # infectionData = ['#infected', date, time, state, district, count, link]
				result = pushToSheet.infection_update(infectionData)
				if(result[1]):
					scoreManager.updatePoints(update.message.from_user.id, update.message.from_user.full_name)
				update.message.reply_text(result[0])				

		elif(update.message.text.startswith('#death')): # similar to #infected (sorry for being lazy)
			deathData = update.message.text.split(' ')
			lowerAll(deathData)
			if(len(deathData) != 5):
				update.message.reply_text('Invalid format, please try again')
			else:
				deathData.insert(1, get_dateTime()[0])
				deathData.insert(2, get_dateTime()[1])
				result = pushToSheet.death_update(deathData)
				if(result[1]):
					scoreManager.updatePoints(update.message.from_user.id, update.message.from_user.full_name)
				update.message.reply_text(result[0])				

		elif(update.message.text.startswith('#reportError')): #this still has ti be made (I need help)
			# TODO : add report error feature
			update.message.reply_text('Hol up {}! This feature is being made'.format(update.message.from_user.mention_markdown()), parse_mode = markdown)
		
		elif(update.message.text.startswith('#districtList')): #replies with the districts.txt document
			#context.bot gives us the bot, another way of sending messages, but needs more arguments, so I generally avoid it
			context.bot.send_document(update.message.chat.id, document = open('res/districts.txt', 'rb'), reply_to_message_id = update.message.message_id)

		elif(update.message.text.startswith('#getLink')): #send the link, will change it to view only link once in action
			# TODO : send a 'view only' link
			update.message.reply_text('This is the link : {}'.format(tokens[1]))
		
		elif(update.message.text.startswith('#chatID')):
			update.message.reply_text('ChatID = {}'.format(update.message.chat.id))
		
		elif(update.message.text.startswith('#leaderBoard')): # this will reply with the leaderboard, almost done
			update.message.reply_text(scoreManager.getLeaderBoard())
		
		elif(update.message.text.startswith('#')): #i nvalid use of #, ex : #infection instead of #infected will send this
			update.message.reply_text("Yo what?! {} Please check what you've entered! Try /help for more intel".format(update.message.from_user.mention_markdown()), parse_mode = markdown)

		elif ('ok boomer' in update.message.text.lower() or 'boomer' in update.message.text.lower()): # just an easter egg ;)
			context.bot.send_photo(update.message.chat.id, photo = open('res/ok_boomer.jpg', 'rb'), reply_to_message_id = update.message.message_id)

def main():

	getTokens()
	global tokens

	updater = Updater(token = tokens[0], use_context = True)  # telgram API thing

	dispatcher = updater.dispatcher # this too

	schedule.every(2).hours.do(refreshDataList)

	dispatcher.add_handler(CommandHandler('start', start)) #for adding a command, we need to do this, start is the function declared above
	dispatcher.add_handler(CommandHandler('help', help)) # similarly for help, the string is the command that invokes the function
	dispatcher.add_handler(MessageHandler(Filters.text, databaseUpdates)) # for all messages

	print('Bot started running!')
	
	updater.start_polling() # Starts the bot

	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	while True:
		schedule.run_pending()
		time.sleep(1)

	updater.idle() # Stops the bot gracefully

if __name__ == '__main__':
	main()