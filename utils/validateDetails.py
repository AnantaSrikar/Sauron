from datetime import datetime
import time

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

globalData = {}
def get_districtsData():
	fileManager = open('res/districts.txt', 'r')
	districtText = fileManager.read()
	districtDataList = districtText.split('\n')

	for districtBoi in districtDataList:
		if (districtBoi.startswith('##')):
			curState = districtBoi.lstrip('## ').replace(' ', '_')
			globalData[curState] = []
		elif(districtBoi.startswith('\t')):
			globalData[curState].append(districtBoi.lstrip())

	return globalData
