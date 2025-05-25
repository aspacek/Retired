
import requests

import unicodedata as ud

import sys

sys.path.insert(0, "../../Letterboxd/General-league-routines")
from Numsort import numsort

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

print('')
PCS_URL = input('Enter URL for PCS results page:\n')

print('')
race = input('Enter race URL (after procyclingstats.com/race/):\n')

print('')
number = int(input('Enter the number of riders:\n'))
print('')

r1 = requests.get(PCS_URL)
source1 = r1.text

# Get all riders:
info_blocks = getstrings('all','<tr data-team="','</tr>',source1,0)
riders = []
for block in info_blocks:
	riderscheck = list(findstrings('<a href="rider/',block))
	if riderscheck != []:
		riders = riders+[getstrings('first','<a href="rider/','">',block,0)]

# Go to each rider's page, check their top results:
topresult_riders = []
count = 1
for rider in riders:
	if count < number+1:
		if count % 10 == 0:
			print(str(count)+' out of '+str(number))
		r2 = requests.get('https://www.procyclingstats.com/rider/'+rider)
		source2 = r2.text
		info_block = getstrings('first','<h3>Top results</h3>','<h3>Teams</h3>',source2,0)
		topresultcheck = list(findstrings(race,info_block))
		if topresultcheck != []:
			topresult_riders = topresult_riders+[rider]
		count = count+1

print('')
print('TOP RESULTS')
print('')
if topresult_riders != []:
	for rider in topresult_riders:
		print(rider)
else:
	print('No top results!')
print('')
