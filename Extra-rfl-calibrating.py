
import requests

import praw

import unicodedata as ud

def normalize(string):
	newstring = ''
	for i in range(len(string)):
		char = string[i]
		desc = ud.name(char)
		cutoff = desc.find(' WITH ')
		if cutoff != -1:
			desc = desc[:cutoff]
			try:
				char = ud.lookup(desc)
			except KeyError:
				pass  # removing "WITH ..." produced an invalid name
		newstring = newstring+char
	return newstring

def findstrings(substring,string):
	# Initialize flag to see if any substrings are found:
	lastfound = -1
	# While loop until no more substrings are found:
	while True:
		# Find next instance of substring in string, starting right after the location of the previous string:
		lastfound = string.find(substring,lastfound+1)
		# If no more substring are found, end the function:
		if lastfound == -1:  
			break
		# If a new substring is found, record its location:
		yield lastfound

def getstrings(which,prestring,poststring,source,lastflag):
	# First find the start of the string:
	length = len(prestring)
	prevalue = list(findstrings(prestring,source))
	# If first instance wanted:
	if which == 'first':
		prevalue = [prevalue[0]+length]
	# If last instance wanted:
	elif which == 'last':
		prevalue = [prevalue[-1]+length]
	# If all instances wanted:
	elif which == 'all':
		prevalue = [item+length for item in prevalue]
	else:
		sys.exit('ERROR - in getstrings - Invalid input for "which"')
	# Find the location of the end of string, and get the strings:
	strings = []
	for beginning in prevalue:
		end = source.find(poststring,beginning)
		if lastflag == 1:
			value = source[beginning:]
		else:
			value = source[beginning:end]
		strings = strings+[value]
	# If just one string desired, return a scalar, otherwise return the array:
	if which == 'first' or which == 'last':
		return strings[0]
	elif which == 'all':
		return strings

def removespace(string):
	flag = 0
	while flag == 0:
		if string[0] == ' ':
			string = string[1:]
		elif string[-1] == ' ':
			string = string[:-1]
		else:
			flag = 1
	return string

# url = URL for PCS results page
# level = WT, Pro, 1, 2
# type = 1 or 2
# placepoints = 10 element array
# yearweight = divide previous year points by this much
# classweight = 5 element array
# samerace = same race last year gets multiplied by this much
def predict(url,level,type,placepoints,yearweight,classweight,samerace):

	PCS_URL = url+'/startlist'

	race = getstrings('first','/race/','/',PCS_URL,0)
	year = getstrings('first','/'+race+'/','/',PCS_URL,0)
	
	r1 = requests.get(PCS_URL)
	source1 = r1.text
	
	# Get all riders:
	riders = getstrings('all','"rider/','">',source1,0)
	
	# Get all rider URLs:
	riderurls = ['https://www.procyclingstats.com/rider/' for i in riders]
	for i in range(len(riders)):
		riderurls[i] = riderurls[i]+riders[i]
	
	scores = [0 for val in riders]
	
	print('')
	# Go through all riders:
	for i in range(len(riderurls)):
		# Get current year info:
#		print(riders[i])
		r = requests.get(riderurls[i])
		source = r.text
		# Make sure data exists:
		flag1 = 0
		check = getstrings('first','</b> km in <b>','</b>',source,0)
		if check == '0':
			flag1 = 1
		else:
			# Grab info blocks:
			info1 = getstrings('first','</th></tr></thead><tbody><tr data-main=','<a class="more" href="rider',source,0)
			info2 = getstrings('all','>more</a></td></tr><tr data-main=','<a class="more" href="rider',source,0)
			info = [info1]
			info = info+info2
			# Grab various info:
			places = []
			races = []
			kinds = []
			classes = []
			years = []
			for j in range(len(info)):
				races_temp = getstrings('first','<a href="race/','/',info[j],0)
				places_temp = getstrings('first','</td><td>','</td>',info[j],0)
				places_check = list(findstrings('"linethrough"',places_temp))
				if places_check != []:
					places_temp = getstrings('first','"linethrough">','<',places_temp,0)
				kinds_temp = getstrings('first',races_temp+'/'+year+'/','">',info[j],0)
				# One day race:
				if kinds_temp == 'result':
					places = places+[places_temp]
					races = races+[getstrings('first','<a href="race/','/',info[j],0)]
					kinds = kinds+[getstrings('first',races[-1]+'/'+year+'/','">',info[j],0)]
					classes = classes+[getstrings('first','</b></a> (',')',info[j],0)]
				# Stage race:
				else:
					if places_temp == '':
						classes_temp = getstrings('first','</b></a> (',')',info[j],0)
					else:
						if getstrings('first','<a href="race/','/',info[j],0) == races_temp:
							places = places+[places_temp]
							races = races+[getstrings('first','<a href="race/','/',info[j],0)]
							kinds = kinds+[getstrings('first',races[-1]+'/'+year+'/','">',info[j],0)]
							classes = classes+[classes_temp]
						else:
							print('\n**** ERROR IN CLASSIFYING STAGE RACE ****\n')
				years = years+[year]
		# Get previous year info:
		prevyear = str(int(year)-1)
		r = requests.get(riderurls[i]+'/'+prevyear)
		source = r.text
		flag2 = 0
		check = getstrings('first','</b> km in <b>','</b>',source,0)
		if check == '0':
			flag2 = 1
		else:
			# Grab info blocks:
			info1 = getstrings('first','</th></tr></thead><tbody><tr data-main=','<a class="more" href="rider',source,0)
			info2 = getstrings('all','>more</a></td></tr><tr data-main=','<a class="more" href="rider',source,0)
			info = [info1]
			info = info+info2
			# Grab various info:
			for j in range(len(info)):
				races_temp = getstrings('first','<a href="race/','/',info[j],0)
				places_temp = getstrings('first','</td><td>','</td>',info[j],0)
				places_check = list(findstrings('"linethrough"',places_temp))
				if places_check != []:
					places_temp = getstrings('first','"linethrough">','<',places_temp,0)
				kinds_temp = getstrings('first',races_temp+'/'+prevyear+'/','">',info[j],0)
				# One day race:
				if kinds_temp == 'result':
					places = places+[places_temp]
					races = races+[getstrings('first','<a href="race/','/',info[j],0)]
					kinds = kinds+[getstrings('first',races[-1]+'/'+prevyear+'/','">',info[j],0)]
					classes = classes+[getstrings('first','</b></a> (',')',info[j],0)]
				# Stage race:
				else:
					if places_temp == '':
						classes_temp = getstrings('first','</b></a> (',')',info[j],0)
					else:
						if getstrings('first','<a href="race/','/',info[j],0) == races_temp:
							places = places+[places_temp]
							races = races+[getstrings('first','<a href="race/','/',info[j],0)]
							kinds = kinds+[getstrings('first',races[-1]+'/'+prevyear+'/','">',info[j],0)]
							classes = classes+[classes_temp]
						else:
							print('\n**** ERROR IN CLASSIFYING STAGE RACE ****\n')
				years = years+[prevyear]
		places_temp = []
		for j in range(len(places)):
			if places[j] == 'DNF' or places[j] == 'DNS' or places[j] == 'DF' or places[j] == 'OTL' or places[j] == 'DSQ':
				places_temp = places_temp+[0]
			else:
				places_temp = places_temp+[int(places[j])]
		places = [val for val in places_temp]
		print(str(i+1)+'/'+str(len(riderurls)))
	
	#	for j in range(len(races)):
	#		print(races[j]+' '+classes[j]+' '+kinds[j]+' '+str(places[j]))
	
		# Compute scores:
	
		# One day races:
		if type == '1':
			for j in range(len(classes)):
				if classes[j][0] == '1':
					points = 0
	#				print('place = '+str(places[j]))
					if places[j] == 1:
						points = placepoints[0]
					elif places[j] == 2:
						points = placepoints[1]
					elif places[j] == 3:
						points = placepoints[2]
					elif places[j] == 4:
						points = placepoints[3]
					elif places[j] == 5:
						points = placepoints[4]
					elif places[j] == 6:
						points = placepoints[5]
					elif places[j] == 7:
						points = placepoints[6]
					elif places[j] == 8:
						points = placepoints[7]
					elif places[j] == 9:
						points = placepoints[8]
					elif places[j] == 10:
						points = placepoints[9]
	#				print('class = '+classes[j][2:])
					if years[j] == prevyear:
						points = points/yearweight
					if classes[j][2:] == 'UWT':
						points = points*classweight[0]
					elif classes[j] == 'WC':
						points = points*classweight[1]
					elif classes[j][2:] == 'Pro' or classes[j][2:] == 'HC':
						points = points*classweight[2]
					elif classes[j][2:] == '1' or classes[j] == 'CC':
						points = points*classweight[3]
					elif classes[j][2:] == '2' or classes[j] == 'NC':
						points = points*classweight[4]
					if races[j] == race and years[j] != year:
						points = points*samerace
	#				print('points = '+str(points))
					scores[i] = scores[i]+points
	
	# Sort scores:
	sriders = [fnam for fnum, fnam in sorted(zip(scores,riders))]
	sriders.reverse()
	scores.sort()
	scores.reverse()

	# Grab the top 8 results:
	sriders = sriders[:8]
	scores = scores[:8]

	# Compute results:
	r2 = requests.get(url)
	source2 = r2.text
	riders_results = getstrings('all','<a href="rider/','">',source2,0)
	# Cut to first 10:
	riders_results = riders_results[:10]
	# Get score:
	score = 0
	points = [15,12,10,8,6,5,4,3,2,1]
	weights = [2,1.8,1.6,1.4,1.2,1,1,1]
	for i in range(len(sriders)):
		for j in range(len(riders_results)):
			if sriders[i] == riders_results[j]:
				score = score+weights[i]*points[j]

	return score


url = 'https://www.procyclingstats.com/race/liege-bastogne-liege/2020'
level = 'WT'
type = '1'

results = []

placepoints = [512,256,128,64,32,16,8,4,2,1]
yearweight = 3
classweight = [5,4,3,2,1]
samerace = yearweight*2
results = results+[predict(url,level,type,placepoints,yearweight,classweight,samerace)]

print('\n** 1/5 **')

placepoints = [512,256,128,64,32,16,8,4,2,1]
yearweight = 4
classweight = [5,4,3,2,1]
samerace = yearweight*2
results = results+[predict(url,level,type,placepoints,yearweight,classweight,samerace)]

print('\n** 2/5 **')

placepoints = [512,256,128,64,32,16,8,4,2,1]
yearweight = 5
classweight = [5,4,3,2,1]
samerace = yearweight*2
results = results+[predict(url,level,type,placepoints,yearweight,classweight,samerace)]

print('\n** 3/5 **')

placepoints = [512,256,128,64,32,16,8,4,2,1]
yearweight = 10
classweight = [5,4,3,2,1]
samerace = yearweight*2
results = results+[predict(url,level,type,placepoints,yearweight,classweight,samerace)]

print('\n** 4/5 **')

placepoints = [1000,750,500,250,100,50,25,10,5,1]
yearweight = 3
classweight = [5,4,3,2,1]
samerace = yearweight*2
results = results+[predict(url,level,type,placepoints,yearweight,classweight,samerace)]

print('\n** 5/5 **')

print('')
for i in range(len(results)):
	print(str(i+1)+' '+str(results[i]))
