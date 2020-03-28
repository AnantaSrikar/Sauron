import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('res/credentials.json',scope)

client = gspread.authorize(creds)

sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1WK6eWSLzwnaFr5XX1xFkzcWzJOdhcdkRDh3whP7kFCY/edit#gid=0').worksheet('Sheet1')

def next_available_row(worksheet):
	str_list = list(filter(None, worksheet.col_values(1)))
	return str(len(str_list)+1)


def death_update(dataList):
	next_row = next_available_row(sheet)
	column = "A"
	i = 1
	while(column < "H"):
		if(column != "E"):
			sheet.update_acell("{}{}".format(column,next_row), dataList[i])
			i += 1
		column = chr(ord(column) + 1)

def infection_update(dataList):
	next_row = next_available_row(sheet)
	column = "A"
	i = 1
	while(column < "H"):
		if(column != "F"):
			sheet.update_acell("{}{}".format(column,next_row), dataList[i])
			i += 1
		column = chr(ord(column) + 1)
	

