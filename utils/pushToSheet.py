import gspread
from oauth2client.service_account import ServiceAccountCredentials
from StartTheBot import getTokens
from datetime import datetime
import time

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('res/credentials.json',scope)

client = gspread.authorize(creds)
tokens = getTokens()

sheet = client.open_by_url(tokens[1]).worksheet('Sheet1')

def next_available_row(worksheet):
	str_list = list(filter(None, worksheet.col_values(1)))
	return str(len(str_list)+1)

def validate_date(dateString):
	day, month, year = dateString.split('/')
	try:
		datetime(int(year), int(month), int(day))
		return True
	except ValueError:
		return False

def validate_time(timeString):
	try:
		time.strptime(timeString, '%H:%M')
		return True
	except ValueError:
		return False

def death_update(dataList):
	next_row = next_available_row(sheet)
	column = "A"
	i = 1
	if(validate_date(dataList[1]) and validate_time(dataList[2])):
		while(column < "H"):
			if(column != "E"):
				sheet.update_acell("{}{}".format(column,next_row), dataList[i])
				i += 1
			column = chr(ord(column) + 1)
		return 'I have updated my database successfully!'
	elif(not validate_date(dataList[1])):
		return 'Invalid date format, try again'
	elif(not validate_time(dataList[2])):
		return 'Invalid time format, try again'

def infection_update(dataList):
	next_row = next_available_row(sheet)
	column = "A"
	i = 1
	if(validate_date(dataList[1]) and validate_time(dataList[2])):
		while(column < "H"):
			if(column != "F"):
				sheet.update_acell("{}{}".format(column,next_row), dataList[i])
				i += 1
			column = chr(ord(column) + 1)
		return 'I have updated my database successfully!'
	elif(not validate_date(dataList[1])):
		return 'Invalid date format, try again'
	elif(not validate_time(dataList[2])):
		return 'Invalid time format, try again'