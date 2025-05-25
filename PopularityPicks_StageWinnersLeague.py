
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
		if char != chr(13) and char != chr(9):
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

debug = 'n'
verbose = 'y'

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
	check = list(findstrings('Stage 1:',bodies[i]))
	if check != []:
		users = users+[users_temp[i]]
		if debug == 'y':
			print('')
			print(users_temp[i])
		pick1 = getstrings('first','Stage 1:','\n',bodies[i],0)
		if debug == 'y':
			print('pick1')
			print(pick1)
		pick1 = removespace(pick1)
		pick2 = getstrings('first','Stage 2:','\n',bodies[i],0)
		if debug == 'y':
			print('pick2')
			print(pick2)
		pick2 = removespace(pick2)
		pick3 = getstrings('first','Stage 3:','\n',bodies[i],0)
		if debug == 'y':
			print('pick3')
			print(pick3)
		pick3 = removespace(pick3)
		pick4 = getstrings('first','Stage 4:','\n',bodies[i],0)
		if debug == 'y':
			print('pick4')
			print(pick4)
		pick4 = removespace(pick4)
		pick5 = getstrings('first','Stage 5:','\n',bodies[i],0)
		if debug == 'y':
			print('pick5')
			print(pick5)
		pick5 = removespace(pick5)
		pick6 = getstrings('first','Stage 6:','\n',bodies[i],0)
		if debug == 'y':
			print('pick6')
			print(pick6)
		pick6 = removespace(pick6)
		pick7 = getstrings('first','Stage 7:','\n',bodies[i],0)
		if debug == 'y':
			print('pick7')
			print(pick7)
		pick7 = removespace(pick7)
		pick8 = getstrings('first','Stage 8:','\n',bodies[i],0)
		if debug == 'y':
			print('pick8')
			print(pick8)
		pick8 = removespace(pick8)
		pick9 = getstrings('first','Stage 9:','\n',bodies[i],0)
		if debug == 'y':
			print('pick9')
			print(pick9)
		pick9 = removespace(pick9)
		pick10 = getstrings('first','Stage 10:','\n',bodies[i],0)
		if debug == 'y':
			print('pick10')
			print(pick10)
		pick10 = removespace(pick10)
		pick11 = getstrings('first','Stage 11:','\n',bodies[i],0)
		if debug == 'y':
			print('pick11')
			print(pick11)
		pick11 = removespace(pick11)
		pick12 = getstrings('first','Stage 12:','\n',bodies[i],0)
		if debug == 'y':
			print('pick12')
			print(pick12)
		pick12 = removespace(pick12)
		pick13 = getstrings('first','Stage 13:','\n',bodies[i],0)
		if debug == 'y':
			print('pick13')
			print(pick13)
		pick13 = removespace(pick13)
		pick14 = getstrings('first','Stage 14:','\n',bodies[i],0)
		if debug == 'y':
			print('pick14')
			print(pick14)
		pick14 = removespace(pick14)
		pick15 = getstrings('first','Stage 15:','\n',bodies[i],0)
		if debug == 'y':
			print('pick15')
			print(pick15)
		pick15 = removespace(pick15)
		pick16 = getstrings('first','Stage 16:','\n',bodies[i],0)
		if debug == 'y':
			print('pick16')
			print(pick16)
		pick16 = removespace(pick16)
		pick17 = getstrings('first','Stage 17:','\n',bodies[i],0)
		if debug == 'y':
			print('pick17')
			print(pick17)
		pick17 = removespace(pick17)
		pick18 = getstrings('first','Stage 18:','\n',bodies[i],0)
		if debug == 'y':
			print('pick18')
			print(pick18)
		pick18 = removespace(pick18)
		pick19 = getstrings('first','Stage 19:','\n',bodies[i],0)
		if debug == 'y':
			print('pick19')
			print(pick19)
		pick19 = removespace(pick19)
		pick20 = getstrings('first','Stage 20:','\n',bodies[i],0)
		if debug == 'y':
			print('pick20')
			print(pick20)
		pick20 = removespace(pick20)
		pick21 = getstrings('first','Stage 21:','\n',bodies[i],0)
		if debug == 'y':
			print('pick21')
			print(pick21)
		pick21 = removespace(pick21)
		if verbose == 'y':
			print('\nUser Picks:')
			print(users_temp[i])
			print(pick1)
			print(pick2)
			print(pick3)
			print(pick4)
			print(pick5)
			print(pick6)
			print(pick7)
			print(pick8)
			print(pick9)
			print(pick10)
			print(pick11)
			print(pick12)
			print(pick13)
			print(pick14)
			print(pick15)
			print(pick16)
			print(pick17)
			print(pick18)
			print(pick19)
			print(pick20)
			print(pick21)
		picks = picks+[[normalize(pick1,debug),normalize(pick2,debug),normalize(pick3,debug),normalize(pick4,debug),normalize(pick5,debug),normalize(pick6,debug),normalize(pick7,debug),normalize(pick8,debug),normalize(pick9,debug),normalize(pick10,debug),normalize(pick11,debug),normalize(pick12,debug),normalize(pick13,debug),normalize(pick14,debug),normalize(pick15,debug),normalize(pick16,debug),normalize(pick17,debug),normalize(pick18,debug),normalize(pick19,debug),normalize(pick20,debug),normalize(pick21,debug)]]

# First go through all picks and check for errors:
riders = []
for i in range(len(users)):
	for j in range(len(picks[i])):
		flag = 0
		if riders == []:
			riders = riders+[picks[i][j]]
		else:
			for k in range(len(riders)):
				if picks[i][j].lower() == riders[k].lower():
					flag = 1
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

scores1 = [0 for i in riders]
scores2 = [0 for i in riders]
scores3 = [0 for i in riders]
scores4 = [0 for i in riders]
scores5 = [0 for i in riders]
scores6 = [0 for i in riders]
scores7 = [0 for i in riders]
scores8 = [0 for i in riders]
scores9 = [0 for i in riders]
scores10 = [0 for i in riders]
scores11 = [0 for i in riders]
scores12 = [0 for i in riders]
scores13 = [0 for i in riders]
scores14 = [0 for i in riders]
scores15 = [0 for i in riders]
scores16 = [0 for i in riders]
scores17 = [0 for i in riders]
scores18 = [0 for i in riders]
scores19 = [0 for i in riders]
scores20 = [0 for i in riders]
scores21 = [0 for i in riders]

print('')
for i in range(len(users)):
	for j in range(len(picks[i])):
		flag = 0
		for k in range(len(riders)):
			if picks[i][j].lower() == riders[k].lower():
				flag = 1
				if j+1 == 1:
					scores1[k] = scores1[k]+1
				elif j+1 == 2:
					scores2[k] = scores2[k]+1
				elif j+1 == 3:
					scores3[k] = scores3[k]+1
				elif j+1 == 4:
					scores4[k] = scores4[k]+1
				elif j+1 == 5:
					scores5[k] = scores5[k]+1
				elif j+1 == 6:
					scores6[k] = scores6[k]+1
				elif j+1 == 7:
					scores7[k] = scores7[k]+1
				elif j+1 == 8:
					scores8[k] = scores8[k]+1
				elif j+1 == 9:
					scores9[k] = scores9[k]+1
				elif j+1 == 10:
					scores10[k] = scores10[k]+1
				elif j+1 == 11:
					scores11[k] = scores11[k]+1
				elif j+1 == 12:
					scores12[k] = scores12[k]+1
				elif j+1 == 13:
					scores13[k] = scores13[k]+1
				elif j+1 == 14:
					scores14[k] = scores14[k]+1
				elif j+1 == 15:
					scores15[k] = scores15[k]+1
				elif j+1 == 16:
					scores16[k] = scores16[k]+1
				elif j+1 == 17:
					scores17[k] = scores17[k]+1
				elif j+1 == 18:
					scores18[k] = scores18[k]+1
				elif j+1 == 19:
					scores19[k] = scores19[k]+1
				elif j+1 == 20:
					scores20[k] = scores20[k]+1
				elif j+1 == 21:
					scores21[k] = scores21[k]+1
		if flag == 0:
			print("\n********** RIDERS DIDN'T MATCH **********")

scores1_temp = [val for val in scores1]
scores2_temp = [val for val in scores2]
scores3_temp = [val for val in scores3]
scores4_temp = [val for val in scores4]
scores5_temp = [val for val in scores5]
scores6_temp = [val for val in scores6]
scores7_temp = [val for val in scores7]
scores8_temp = [val for val in scores8]
scores9_temp = [val for val in scores9]
scores10_temp = [val for val in scores10]
scores11_temp = [val for val in scores11]
scores12_temp = [val for val in scores12]
scores13_temp = [val for val in scores13]
scores14_temp = [val for val in scores14]
scores15_temp = [val for val in scores15]
scores16_temp = [val for val in scores16]
scores17_temp = [val for val in scores17]
scores18_temp = [val for val in scores18]
scores19_temp = [val for val in scores19]
scores20_temp = [val for val in scores20]
scores21_temp = [val for val in scores21]
riders1_temp = [val for val in riders]
riders2_temp = [val for val in riders]
riders3_temp = [val for val in riders]
riders4_temp = [val for val in riders]
riders5_temp = [val for val in riders]
riders6_temp = [val for val in riders]
riders7_temp = [val for val in riders]
riders8_temp = [val for val in riders]
riders9_temp = [val for val in riders]
riders10_temp = [val for val in riders]
riders11_temp = [val for val in riders]
riders12_temp = [val for val in riders]
riders13_temp = [val for val in riders]
riders14_temp = [val for val in riders]
riders15_temp = [val for val in riders]
riders16_temp = [val for val in riders]
riders17_temp = [val for val in riders]
riders18_temp = [val for val in riders]
riders19_temp = [val for val in riders]
riders20_temp = [val for val in riders]
riders21_temp = [val for val in riders]
sscores1,sriders1 = numsort(scores1_temp,riders1_temp,1,1)
sscores2,sriders2 = numsort(scores2_temp,riders2_temp,1,1)
sscores3,sriders3 = numsort(scores3_temp,riders3_temp,1,1)
sscores4,sriders4 = numsort(scores4_temp,riders4_temp,1,1)
sscores5,sriders5 = numsort(scores5_temp,riders5_temp,1,1)
sscores6,sriders6 = numsort(scores6_temp,riders6_temp,1,1)
sscores7,sriders7 = numsort(scores7_temp,riders7_temp,1,1)
sscores8,sriders8 = numsort(scores8_temp,riders8_temp,1,1)
sscores9,sriders9 = numsort(scores9_temp,riders9_temp,1,1)
sscores10,sriders10 = numsort(scores10_temp,riders10_temp,1,1)
sscores11,sriders11 = numsort(scores11_temp,riders11_temp,1,1)
sscores12,sriders12 = numsort(scores12_temp,riders12_temp,1,1)
sscores13,sriders13 = numsort(scores13_temp,riders13_temp,1,1)
sscores14,sriders14 = numsort(scores14_temp,riders14_temp,1,1)
sscores15,sriders15 = numsort(scores15_temp,riders15_temp,1,1)
sscores16,sriders16 = numsort(scores16_temp,riders16_temp,1,1)
sscores17,sriders17 = numsort(scores17_temp,riders17_temp,1,1)
sscores18,sriders18 = numsort(scores18_temp,riders18_temp,1,1)
sscores19,sriders19 = numsort(scores19_temp,riders19_temp,1,1)
sscores20,sriders20 = numsort(scores20_temp,riders20_temp,1,1)
sscores21,sriders21 = numsort(scores21_temp,riders21_temp,1,1)

print('')
print('STAGE 1')
for i in range(len(sriders1)):
	print('{:<5.1f} {}'.format(sscores1[i],sriders1[i]))
print('')
print('STAGE 2')
for i in range(len(sriders2)):
	print('{:<5.1f} {}'.format(sscores2[i],sriders2[i]))
print('')
print('STAGE 3')
for i in range(len(sriders3)):
	print('{:<5.1f} {}'.format(sscores3[i],sriders3[i]))
print('')
print('STAGE 4')
for i in range(len(sriders4)):
	print('{:<5.1f} {}'.format(sscores4[i],sriders4[i]))
print('')
print('STAGE 5')
for i in range(len(sriders5)):
	print('{:<5.1f} {}'.format(sscores5[i],sriders5[i]))
print('')
print('STAGE 6')
for i in range(len(sriders6)):
	print('{:<5.1f} {}'.format(sscores6[i],sriders6[i]))
print('')
print('STAGE 7')
for i in range(len(sriders7)):
	print('{:<5.1f} {}'.format(sscores7[i],sriders7[i]))
print('')
print('STAGE 8')
for i in range(len(sriders8)):
	print('{:<5.1f} {}'.format(sscores8[i],sriders8[i]))
print('')
print('STAGE 9')
for i in range(len(sriders9)):
	print('{:<5.1f} {}'.format(sscores9[i],sriders9[i]))
print('')
print('STAGE 10')
for i in range(len(sriders10)):
	print('{:<5.1f} {}'.format(sscores10[i],sriders10[i]))
print('')
print('STAGE 11')
for i in range(len(sriders11)):
	print('{:<5.1f} {}'.format(sscores11[i],sriders11[i]))
print('')
print('STAGE 12')
for i in range(len(sriders12)):
	print('{:<5.1f} {}'.format(sscores12[i],sriders12[i]))
print('')
print('STAGE 13')
for i in range(len(sriders13)):
	print('{:<5.1f} {}'.format(sscores13[i],sriders13[i]))
print('')
print('STAGE 14')
for i in range(len(sriders14)):
	print('{:<5.1f} {}'.format(sscores14[i],sriders14[i]))
print('')
print('STAGE 15')
for i in range(len(sriders15)):
	print('{:<5.1f} {}'.format(sscores15[i],sriders15[i]))
print('')
print('STAGE 16')
for i in range(len(sriders16)):
	print('{:<5.1f} {}'.format(sscores16[i],sriders16[i]))
print('')
print('STAGE 17')
for i in range(len(sriders17)):
	print('{:<5.1f} {}'.format(sscores17[i],sriders17[i]))
print('')
print('STAGE 18')
for i in range(len(sriders18)):
	print('{:<5.1f} {}'.format(sscores18[i],sriders18[i]))
print('')
print('STAGE 19')
for i in range(len(sriders19)):
	print('{:<5.1f} {}'.format(sscores19[i],sriders19[i]))
print('')
print('STAGE 20')
for i in range(len(sriders20)):
	print('{:<5.1f} {}'.format(sscores20[i],sriders20[i]))
print('')
print('STAGE 21')
for i in range(len(sriders21)):
	print('{:<5.1f} {}'.format(sscores21[i],sriders21[i]))
print('')
