
import requests

import praw

import unicodedata as ud

import sys

sys.path.insert(0, "../Letterboxd/General-league-routines")
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
ExtraRFL_URL = input('Enter URL for ExtraRFL predictions page:\n')
ExtraRFLnum = 8

debug = 'n'
verbose = 'y'

userskip = ''

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
	if users_temp[i] != userskip:
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
				print('\n** x1 ERROR ** '+users_temp[i])
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
				print('\n** pick1_3 = Nobody Nobody ** '+users_temp[i])
			pick1_1 = removespace(pick1_1)
			pick1_2 = removespace(pick1_2)
			pick1_3 = removespace(pick1_3)
			if verbose == 'y':
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
riders = []
riders = riders+['']
riders = riders+[' ']
for i in range(len(users)):
	for j in range(len(picks[i])):
		flag = 0
		if len(picks[i][j]) >= 40:
			picks[i][j] = ' '
		for k in range(len(riders)):
			kflag = 0
			picklow = picks[i][j].lower()
			ridelow = riders[k].lower()
			if len(picklow) == 0:
				pcheck = 0
			elif len(picklow) == 1:
				pcheck = 1
			elif len(picklow) == 2:
				pcheck = 2
			else:
				pcheck = 3
			if len(ridelow) == 0:
				rcheck = 0
			elif len(ridelow) == 1:
				rcheck = 1
			elif len(ridelow) == 2:
				rcheck = 2
			else:
				rcheck = 3
			if picklow == ridelow:
				kflag = 1
			elif removespace(picklow) == removespace(ridelow):
				kflag = 1
			elif pcheck == 2:
				if picklow[1:] == ridelow or picklow[:-1] == ridelow:
					kflag = 1
				elif rcheck == 2:
					if picklow[1:] == ridelow[1:] or picklow == ridelow[1:] or picklow[:-1] == ridelow[:-1] or picklow == ridelow[:-1]:
						kflag = 1
				elif rcheck == 3:
					if picklow[1:] == ridelow[2:] or picklow == ridelow[2:] or picklow[:-1] == ridelow[:-2] or picklow == ridelow[:-2]:
						kflag = 1
			elif pcheck == 3:
				if picklow[1:] == ridelow or picklow[:-1] == ridelow or picklow[2:] == ridelow or picklow[:-2] == ridelow:
					kflag = 1
				elif rcheck == 2:
					if picklow[1:] == ridelow[1:] or picklow == ridelow[1:] or picklow[:-1] == ridelow[:-1] or picklow == ridelow[:-1] or picklow[2:] == ridelow[1:] or picklow[:-2] == ridelow[:-1]:
						kflag = 1
				elif rcheck == 3:
					if picklow[1:] == ridelow[2:] or picklow == ridelow[2:] or picklow[:-1] == ridelow[:-2] or picklow == ridelow[:-2] or picklow[2:] == ridelow[2:] or picklow[:-2] == ridelow[:-2]:
						kflag = 1
			if kflag == 1:
				flag = 1
				picks[i][j] = riders[k]
		if flag == 0:
			print('\nCURRENT RIDERS:')
			for k in range(len(riders)):
				print(str(k+1)+' '+riders[k])
			answer = input('\nIs '+picks[i][j]+' in the rider list? (y/n): ')
			if answer == 'y':
				answer2 = input('Which place? ')
				picks[i][j] = riders[int(answer2)-1]
			else:
				riders = riders+[picks[i][j]]

print('\n*****')
for i in riders:
	print(i)
print('*****')

weights = [2,1.8,1.6,1.4,1.2,1,1,1]
scores = [0 for i in riders]

print('')
for i in range(len(users)):
	for j in range(len(picks[i])):
		flag = 0
		for k in range(len(riders)):
			if picks[i][j].lower() == riders[k].lower():
				flag = 1
				if verbose == 'y':
					print(users[i]+' '+picks[i][j]+' '+riders[k]+' '+str(scores[k])+' '+str(weights[j])+' '+str(scores[k]+weights[j]))
				scores[k] = scores[k]+weights[j]
		if flag == 0:
			print("\n********** RIDERS DIDN'T MATCH **********")

scores_temp = [val for val in scores]
riders_temp = [val for val in riders]
sscores,sriders = numsort(scores_temp,riders_temp,1,1)

print('')
for i in range(len(sriders)):
	print('{:<5.1f} {}'.format(sscores[i],sriders[i]))
print('')
