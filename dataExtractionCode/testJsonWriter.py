import json
import os
import subprocess
import re

data = dict()
path = "../Documents/Cesium/Apps/ICONData/"

for file in os.listdir(path + 'czml'):
	year = re.search('[\d]+-',file).group(0)[:-1]
	dayOfYear = re.search('-\d+_', file).group(0)[1:-1]
	key = ('%s-%s' % (year,dayOfYear))
	version = int(re.search('v([\d]+)', file).group(0)[1:] + re.search('r([\d])+',file).group(0)[1:])
	ephemType = re.search('-[a-zA-Z]', file).group(0)
	try:
		#check if date already loaded in JSON, if not exception thrown and automatically add as latest version
		stored = data[key]
		storedVersion = int(re.search('v([\d]+)', stored).group(0)[1:] + re.search('r([\d])+',stored).group(0)[1:])
		storedEphemType = re.search('-[a-zA-Z]', stored).group(0)
		if ephemType != storedEphemType:
			if storedEphemType == '-p' and ephemType == '-d':
				data[key] = file
		else:
			if version > storedVersion:
				data[key] = file
	except KeyError:
		data[key] = file

with open(path + 'fileMap.json', 'w') as outfile:
	json.dump(data, outfile)
