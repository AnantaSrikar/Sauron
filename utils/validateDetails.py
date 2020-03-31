# All the validations and verifications are done here

import json
import os
import schedule
import time
import difflib

globalData = {}

# To validate the state and district entries made by contributors

def lowerAll(daList):
	for i in range(len(daList)):
		daList[i] = daList[i].lower()

def get_districtsData():
	fileManager = open('res/districts.txt', 'r')
	districtText = fileManager.read()
	districtDataList = districtText.split('\n')
	lowerAll(districtDataList)

	for districtBoi in districtDataList:
		if (districtBoi.startswith('##')):
			curState = districtBoi.lstrip('## ').replace(' ', '_')
			globalData[curState] = []
		elif(districtBoi.startswith('\t')):
			globalData[curState].append(districtBoi.lstrip())

get_districtsData()

def approxName(stateName, districtName, errorType):
	matches = []
	if(errorType == 1):
		matches = difflib.get_close_matches(districtName, globalData[stateName])
	elif(errorType == 2):
		matches = difflib.get_close_matches(stateName, globalData)
	matchString = ''
	if(len(matches) == 0):
		return 'None, try /help for getting help'
	
	for match in matches:
		matchString += match + '\n'
	
	return matchString

def verifyStateDistrict(stateName, districtName): # this fuction is used in the final pushToSheet.py
	if(stateName in globalData):  #seeing if the state exists
		if(districtName in globalData[stateName] or districtName == 'dist_na'):  # seeing if the district exists inside the state
			return [0]
		else:
			return [1, approxName(stateName, districtName, 1)] # state found but no district in it
	return [2, approxName(stateName, districtName, 2)]         # coudn't find the state

# To prevent spamming the crowdsourcing

entryList = []

def refreshDataList():
	global entryList
	entryList = []
	try:
		os.remove('res/antiSpam.json')
	except:
		pass

def reloadSpamData():
	try:
		global entryList
		entryList = json.load(open('res/antiSpam.json', 'r'))
	except:
		pass

def verifySpam(stateName, districtName, reportType):
	
	reloadSpamData()
	
	if([stateName, districtName, reportType] not in entryList):
		entryList.append([stateName, districtName, reportType])
		j = json.dumps(entryList)
		f = open('res/antiSpam.json', 'w')
		f.write(j)
		f.close()
		return True
	
	return False


def verifyNum(number):
	try:
		number = int(number)
		return True
	except:
		return False