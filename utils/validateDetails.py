# All the validations and verifications are done here

import json
import os
import schedule
import time

globalData = {}

# To validate the state and district entries made by contributors

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

get_districtsData()

def verifyStateDistrict(stateName, districtName): # this fuction is used in the final pushToSheet.py
	if(stateName in globalData):  #seeing if the state exists
		if(districtName in globalData[stateName]):  # seeing if the district exists inside the state
			return 0
		else:
			return 1 # state found but no district in it
	return 2         # coudn't find the state

# To prevent spamming the crowdsourcing

entryList = []

def refreshDataList():
	entryList = []
	# TODO : remove res/antiSpam.json periodically, every 2 hours

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