
import requests

import praw

import unicodedata as ud

import sys

sys.path.insert(0, "../../Letterboxd/General-league-routines")
from Numsort import numsort

def normalize(string,debug):
	if debug == 'y':
		print('\nNormalize string input:')
		print(string)
	newstring = ''
	for i in range(len(string)):
		char = string[i]
		if debug == 'y':
			print('char:')
			print(char)
			print('ord(char)')
			print(ord(char))
		if char != chr(13):
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
	preflag = 1
	if string != '':
		for i in range(len(string)):
			if string[i] != ' ':
				preflag = 0
	if preflag == 0:
		flag = 0
		while flag == 0:
			if string[0] == ' ':
				string = string[1:]
			elif string[-1] == ' ':
				string = string[:-1]
			else:
				flag = 1
	return string

print('')
PCS_URL = input('Enter URL for PCS results page:\n')
PCSnum = 10

print('')
ExtraRFL_URL = input('Enter URL for ExtraRFL predictions page:\n')
ExtraRFLnum = 8

r1 = requests.get(PCS_URL)
source1 = r1.text

#r2 = requests.get(ExtraRFL_URL)
#source2 = r2.text

# Check if it's a stage race:
isitgc = input('\nAre these stage race GC results? (y/n): ')

# Ask for verbose results?
verbose = input('\nWould you like a verbose output? (y/n/d): ')
if verbose == 'd':
	verbose = 'y'
	debug = 'y'
else:
	debug = 'n'

## GRAB TOP 10 IN PCS RESULTS STANDINGS ##
## Edit: top 11 ##

# Get all riders:
info_blocks = getstrings('all','<tr data-team="','</tr>',source1,0)
riders = []
for i in range(len(info_blocks)):
	riderscheck = list(findstrings('<a href="rider/',info_blocks[i]))
	if riderscheck != []:
		riders = riders+[getstrings('first','<a href="rider/','">',info_blocks[i],0)]
riders_first = []
riders_last = []
weirdnames = ['zsofiaszabo','loughlin','masengesho']
weirdfirst = ['zsofia'     ,'michael' ,'masengesho']
weirdlast  = ['szabo'      ,'loughlin','masengesho']
for i in range(len(riders)):
	weirdflag = 0
	for j in range(len(weirdnames)):
		if riders[i] == weirdnames[j]:
			weirdflag = 1
			first = weirdfirst[j]
			last = weirdlast[j]
	if weirdflag == 0:
		splitnames = riders[i].split('-')
		if len(splitnames) < 2:
			print('')
			print(splitnames)
			sys.exit('ERROR - in main - Rider has less than 2 name words')
		elif len(splitnames) == 2:
			for j in range(len(splitnames)):
				splitnames[j] = splitnames[j].capitalize()
			riders_first = riders_first+[splitnames[0]]
			riders_last = riders_last+[splitnames[1]]
		else:
			first = ''
			last = ''
			for j in range(len(splitnames)):
				splitnames[j] = splitnames[j].capitalize()
				if j < len(splitnames)-2:
					if first == '':
						first = first+splitnames[j]
					else:
						first = first+' '+splitnames[j]
				else:
					if last == '':
						last = last+splitnames[j]
					else:
						last = last+' '+splitnames[j]
			riders_first = riders_first+[first]
			riders_last = riders_last+[last]
	else:
		riders_first = riders_first+[first]
		riders_last = riders_last+[last]

if isitgc == 'y':
	# Get all GC places:
	rider_places = []
	for i in range(len(info_blocks)):
		placecheck = list(findstrings('</td><td class="gc hide" >',info_blocks[i]))
		if placecheck != []:
			test = getstrings('first','</td><td class="gc hide" >','</td>',info_blocks[i],0)
			if test != '':
				rider_places = rider_places+[getstrings('first','</td><td class="gc hide" >','</td>',info_blocks[i],0)]
	# Cut main list to place list:
	riders_first = riders_first[:len(rider_places)]
	riders_last = riders_last[:len(rider_places)]
	# Places should be integers:
	rider_places = [int(val) for val in rider_places]
	# Sort the riders by their GC places:
	sfirst = [fnam for fnum, fnam in sorted(zip(rider_places,riders_first))]
	slast = [fnam for fnum, fnam in sorted(zip(rider_places,riders_last))]
	rider_places.sort()
	riders_first = [val for val in sfirst]
	riders_last = [val for val in slast]

riders_first_all = [val for val in riders_first]
riders_last_all = [val for val in riders_last]

# Get 11th rider:
riders_last_11 = riders_last[PCSnum]
riders_first_11 = riders_first[PCSnum]
# Cut to first 10:
riders_last = riders_last[:PCSnum]
riders_first = riders_first[:PCSnum]

# Remove accents and such:
for i in range(len(riders_last)):
	riders_last[i] = normalize(riders_last[i],debug)
	riders_first[i] = normalize(riders_first[i],debug)
riders_last_11 = normalize(riders_last_11,debug)
riders_first_11 = normalize(riders_first_11,debug)

print('')
print('RACE RESULTS')
print('')
for i in range(len(riders_first)):
	print('{:<2d} {} {}'.format(i+1,riders_first[i],riders_last[i]))
print('{}{:<2d} {} {}'.format('\n',11,riders_first_11,riders_last_11))

# Remove accents and such for all riders as well:
for i in range(len(riders_last_all)):
	riders_last_all[i] = normalize(riders_last_all[i],debug)
	riders_first_all[i] = normalize(riders_first_all[i],debug)

## GRAB EXTRARFL PREDICTIONS ##

reddit = praw.Reddit(client_id='YsgWL2Nj_Cc6mg',client_secret='GMbjBrnX3WcMbM5L6m_k7D6vSp8',user_agent='ExtraRFL scorer')
submission = reddit.submission(url=ExtraRFL_URL)
submission.comments.replace_more(limit=None)
users_temp = []
bodies = []
for top_level_comment in submission.comments:
	users_temp = users_temp+[str(top_level_comment.author)]
	bodies = bodies+[str(top_level_comment.body)]

users = []
picks = []
print('')
for i in range(len(users_temp)):
	check = list(findstrings('(x2.0)',bodies[i]))
	if check != []:
		users = users+[users_temp[i]]
		if debug == 'y':
			print('')
			print(users_temp[i])
		pick2 = getstrings('first','(x2.0)','\n',bodies[i],0)
		if debug == 'y':
			print('pick2')
			print(pick2)
		pick2 = removespace(pick2)
		pick18 = getstrings('first','(x1.8)','\n',bodies[i],0)
		if debug == 'y':
			print('pick18')
			print(pick18)
		pick18 = removespace(pick18)
		pick16 = getstrings('first','(x1.6)','\n',bodies[i],0)
		if debug == 'y':
			print('pick16')
			print(pick16)
		pick16 = removespace(pick16)
		pick14 = getstrings('first','(x1.4)','\n',bodies[i],0)
		if debug == 'y':
			print('pick14')
			print(pick14)
		pick14 = removespace(pick14)
		pick12 = getstrings('first','(x1.2)','\n',bodies[i],0)
		if debug == 'y':
			print('pick12')
			print(pick12)
		pick12 = removespace(pick12)
		pick1 = getstrings('all','(x1.0)','\n',bodies[i],0)
		pick1f = getstrings('last','(x1.0)','\n',bodies[i],1)
		if debug == 'y':
			print('pick1')
			print(pick1)
			print('pick1f')
			print(pick1f)
		pick1flag2 = 0
		if len(pick1) != 3:
			print('** x1 ERROR ** '+users_temp[i])
			if len(pick1) == 2:
				pick1flag2 = 1
		pick1_1 = pick1[0]
		pick1_2 = pick1[1]
		count = 0
		for j in range(len(pick1f)):
			if pick1f[j] == '\n':
				count = count+1
		if pick1flag2 == 0:
			if count > 1:
				pick1_3 = pick1[2]
			else:
				pick1_3 = pick1f
		else:
			pick1_3 = 'Nobody Nobody'
			print('** pick1_3 = Nobody Nobody ** '+users_temp[i])
		pick1_1 = removespace(pick1_1)
		pick1_2 = removespace(pick1_2)
		pick1_3 = removespace(pick1_3)
		if debug == 'y':
			print('\nUser Picks:')
			print(users_temp[i])
			print(pick2)
			print(pick18)
			print(pick16)
			print(pick14)
			print(pick12)
			print(pick1_1)
			print(pick1_2)
			print(pick1_3)
		picks = picks+[[normalize(pick2,debug),normalize(pick18,debug),normalize(pick16,debug),normalize(pick14,debug),normalize(pick12,debug),normalize(pick1_1,debug),normalize(pick1_2,debug),normalize(pick1_3,debug)]]

# First go through all picks and check for errors:
tocheck = []
for i in range(len(users)):
	for j in range(len(picks[i])):
		flag = 0
		for k in range(len(riders_first_all)):
			if picks[i][j].lower() == riders_first_all[k].lower()+' '+riders_last_all[k].lower():
				flag = 1
		if flag == 0:
			if tocheck != []:
				for k in range(len(tocheck)):
					if picks[i][j].lower() == tocheck[k].lower():
						flag = 1
				if flag == 0:
					tocheck = tocheck+[picks[i][j]]
			else:
				tocheck = tocheck+[picks[i][j]]

if tocheck != []:
	resolution = ['' for i in tocheck]
	for i in range(len(tocheck)):
		answer = input('\nIs '+tocheck[i]+' in the race results? (y/n): ')
		if answer == 'y':
			answer2 = input('Which place? ')
			resolution[i] = int(answer2)-1
		else:
			resolution[i] = 'checked'

points = [15,12,10,8,6,5,4,3,2,1]
weights = [2,1.8,1.6,1.4,1.2,1,1,1]
scores = [0 for i in users]
scores11 = [0 for i in users]

# Check duplicates just in case:
checked = [0 for val in users]
for i in range(len(users)):
	if checked[i] == 0:
		for j in range(len(users)):
			if i != j and users[j] == users[i] and checked[j] == 0:
				users[j] = users[j]+'_dupe2'
				checked[j] = 1
		checked[i] = 1

for i in range(len(users)):
	if verbose == 'y':
		print('\n'+users[i])
	for j in range(len(picks[i])):
		flag1 = 0
		if tocheck != []:
			flag2 = 0
			for k in range(len(tocheck)):
				if picks[i][j].lower() == tocheck[k].lower():
					flag2 = 1
					if resolution[k] == 'checked':
						flag1 = 1
					elif resolution[k] == 10:
						current = riders_first_11+' '+riders_last_11
					else:
						current = riders_first[resolution[k]]+' '+riders_last[resolution[k]]
			if flag2 == 0:
				current = picks[i][j]
		else:
			current = picks[i][j]
		if flag1 == 0:
			for k in range(len(riders_first)):
				if current.lower() == riders_first[k].lower()+' '+riders_last[k].lower():
					if verbose == 'y':
						print(current.lower()+' '+str(scores[i])+' + '+str(weights[j])+' * '+str(points[k])+' = '+str(scores[i]+weights[j]*points[k]))
					scores[i] = scores[i]+weights[j]*points[k]
			if current.lower() == riders_first_11.lower()+' '+riders_last_11.lower():
				if verbose == 'y':
					print('11TH RIDER PICK: '+current.lower()+' '+str(scores11[i])+' + '+str(weights[j])+' = '+str(scores11[i]+weights[j]))
				scores11[i] = scores11[i]+weights[j]

scores_temp = [val for val in scores]
users_temp = [val for val in users]
sscores,susers = numsort(scores_temp,users_temp,1,1)
scores_temp = [val for val in scores]
scores11_temp = [val for val in scores11]
sscores,sscores11 = numsort(scores_temp,scores11_temp,0,1)

print('')
for i in range(len(susers)):
	print('{:<5.1f} {}'.format(sscores[i],susers[i]))
print('')
print('11th Place Points')
newscores11 = []
newusers11 = []
newusers = [val.lower() for val in susers]
newusers.sort()
for i in range(len(newusers)):
	for j in range(len(susers)):
		if susers[j].lower() == newusers[i]:
			newusers11 = newusers11+[susers[j]]
			newscores11 = newscores11+[sscores11[j]]
for i in range(len(newusers)):
	print('{:<5.1f} {}'.format(newscores11[i],newusers11[i]))
print('')
