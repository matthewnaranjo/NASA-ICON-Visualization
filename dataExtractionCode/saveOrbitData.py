import json
import os
import subprocess
import re
import datetime

pathToJSON = "../Documents/Cesium/Apps/ICONData/"
pathToData = "/../../disks/data/icon/Repository/Archive/LEVEL.0.PRIME/GROUND/"

data = dict()
log = dict()

with open(pathToJSON + 'fileMap.json') as d_file:
	czmlLoaded = json.load(d_file)

ephemerisList = ['EPHEMERIS', 'EPHEMERIS.PREDICTIVE']

for ephem in [0,1]:
	ephemeris = ephemerisList[ephem]
	for year in os.listdir(pathToData + ephemeris):
		for file in os.listdir(pathToData + ephemeris + '/' + year):
			if year == '2016':
				break
			dayOfYear = re.search('-\d+_', file).group(0)[1:-1]
			key = ('%s-%s' % (year,dayOfYear))
			version = int(re.search('v([\d]+)', file).group(0)[1:] + re.search('r([\d])+',file).group(0)[1:])
			try:
				#check if date already loaded in JSON, if not exception thrown and automatically converted to czml
				loaded = czmlLoaded[key]
				loadedVersion = int(re.search('v([\d]+)', loaded).group(0)[1:] + re.search('r([\d])+',loaded).group(0)[1:])
				ephemType = re.search('-[a-zA-Z]', file).group(0)
				if ephem == 0:
					if ephemType == '-p':
						log[key] = file
						subprocess.call(['python create.py -d %s -y %s -v %s -e %s' % (dayOfYear, year, version, ephem)], shell = True)
				else:
					if ephemType == '-p':
						if version > loadedVersion:
							subprocess.call(['python create.py -d %s -y %s -v %s -e %s' % (dayOfYear, year, version, ephem)], shell = True)
							log[key] = file
			except KeyError:
				subprocess.call(['python create.py -d %s -y %s -v %s -e %s' % (dayOfYear, year, version, ephem)], shell = True)
				log[key] = file

for file in os.listdir(pathToJSON + 'czml'):
	year = re.search('[\d]+-',file).group(0)[:-1]
	dayOfYear = re.search('-\d+_', file).group(0)[1:-1]
	key = ('%s-%s' % (year,dayOfYear))
	version = int(re.search('v([\d]+)', file).group(0)[1:] + re.search('r([\d])+',file).group(0)[1:])
	ephemType = re.search('-[a-zA-Z]', file).group(0)
	print(ephemType)
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

with open(pathToJSON + 'fileMap.json', 'w') as outfile:
	json.dump(data, outfile)

with open(pathToJSON + 'log.txt', 'a') as outfile:
	json.dump({datetime.datetime.now().strftime("%m-%d-%Y"):log}, outfile)
