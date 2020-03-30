# To validate the state and district entries made by contributors

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

get_districtsData()

def verifyStateDistrict(stateName, districtName): # this fuction is used in the final pushToSheet.py
	if(stateName in globalData):  #seeing if the state exists
		if(districtName in globalData[stateName]):  # seeing if the district exists inside the state
			return 0
		else:
			return 1 # state found but no district in it
	return 2         # coudn't find the state