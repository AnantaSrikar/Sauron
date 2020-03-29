import gspread
from oauth2client.service_account import ServiceAccountCredentials
from StartTheBot import getTokens
from utils.validateDetails import verifyStateDistrict
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('res/credentials.json',scope)

client = gspread.authorize(creds)
tokens = getTokens()

sheet = client.open_by_url(tokens[1]).worksheet('Sheet1')

def next_available_row(worksheet):
	str_list = list(filter(None, worksheet.col_values(1)))
	return str(len(str_list)+1)

def death_update(dataList):
	next_row = next_available_row(sheet)
	column = "A"
	i = 1
	if(verifyStateDistrict(dataList[3], dataList[4]) == 0):
		while(column < "H"):
			if(column != "E"):
				sheet.update_acell("{}{}".format(column,next_row), dataList[i])
				i += 1
			column = chr(ord(column) + 1)
		return 'I have updated my database successfully!'
	elif(verifyStateDistrict(dataList[3], dataList[4]) == 1):
		return 'Unable to find {} in {}, please check and try again'.format(dataList[4], dataList[3])
	elif(verifyStateDistrict(dataList[3], dataList[4]) == 2):
		return 'Unable to find {}, please check and try again'.format(dataList[3])

def infection_update(dataList):
	next_row = next_available_row(sheet)
	column = "A"
	i = 1
	if(verifyStateDistrict(dataList[3], dataList[4]) == 0):
		while(column < "H"):
			if(column != "F"):
				sheet.update_acell("{}{}".format(column,next_row), dataList[i])
				i += 1
			column = chr(ord(column) + 1)
		return 'I have updated my database successfully!'
	elif(verifyStateDistrict(dataList[3], dataList[4]) == 1):
		return 'Unable to find {} in {}, please check and try again'.format(dataList[4], dataList[3])
	elif(verifyStateDistrict(dataList[3], dataList[4]) == 2):
		return 'Unable to find {}, please check and try again'.format(dataList[3])