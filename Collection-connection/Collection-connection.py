##############################
## Collection-connection.py ##
##############################

##
## Written by Alex Spacek
## February 2025
## (Copied from Film_actors_check.py)
## Last updated: May 2025
##

############################################################################
############################################################################

##
## Imports
##

# sys module - reads in input values
#            - exits program on error
import sys

# csv module - read and write csv files
import csv

# time module - lets us wait
import time

import requests

import locale

from pathlib import Path

from shutil import copyfile

import os

sys.path.insert(0, "../../Letterboxd/General-league-routines")
from Findstrings import findstrings
from Getstrings import getstrings
from Numsort import numsort
from Getuserfilms import getuserfilms
from Getfilminfo import getfilminfo

############################################################################
############################################################################

##
## Main Routine
##

# How long to wait between Letterboxd page reads, in seconds
wait_time_secs = 15

# Enter a film name as it appears in the Letterboxd URL
# For example, https://letterboxd.com/film/atonement/

film1 = input('\nEnter Letterboxd film: ')

outputfile = open('Output/'+film1+'-collection-connection-output.txt','w')

# Compare with every film in our collection
# Status update:
print('\nReading in Amanda\'s and Alex\'s film collection.')
outputfile.write('\nReading in Amanda\'s and Alex\'s film collection.')


# The base url of our film collection:
url = 'https://letterboxd.com/moogic/list/moogics-dvd-collection/detail/'
# Grab source code for the first page:
r = requests.get(url)
source = r.text
time.sleep(wait_time_secs)
# Find the number of pages
pages = int(getstrings('last','/moogic/list/moogics-dvd-collection/detail/page/','/">',source))
# Loop through all pages and grab all the film titles:
pageflag = 0
# Initialize results:
films = []
years = []
# Start on page 1, get the films and years:
films = films+getstrings('all','data-film-slug="','"',source)
years = years+getstrings('all','/films/year/','/">',source)
# Now loop through the rest of the pages:
if pageflag == 0:
	for page in range(pages-1):
		# Start on page 2:
		page = str(page + 2)
		# Grab source code of the page:
		r = requests.get(url+'page/'+page+'/')
		source = r.text
		time.sleep(wait_time_secs)
		# Get films and years:
		films = films+getstrings('all','data-film-slug="','"',source)
		years = years+getstrings('all','/films/year/','/">',source)
# Make year values integers:
years = [int(item) for item in years]
# Make sure the lengths match:
if len(films) != len(years):
	sys.exit('ERROR - in function "MAIN" - Number of films does not match number of years')

# Status update:
print('\nNumber of films in collection: '+str(len(films)))
outputfile.write('\nNumber of films in collection: '+str(len(films)))

# Read in actors and films to ignore
ignorefilms = []
ignoreactors = []
with open('Films-to-ignore.txt') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter='\n')
	for row in csv_reader:
		ignorefilms = ignorefilms+[row[0]]
with open('Actors-to-ignore.txt') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter='\n')
	for row in csv_reader:
		ignoreactors = ignoreactors+[row[0]]

print('\nChecking all owned films that share at least one actor with '+film1)
outputfile.write('\n\nChecking all owned films that share at least one actor with '+film1)

allfilms = []
allactors = []
n = 0

for eachfilm in films:
	n = n+1
	print('\n'+str(n)+' / '+str(len(films))+' Checking '+eachfilm)
	outputfile.write('\n\n'+str(n)+' / '+str(len(films))+' Checking '+eachfilm)
	skipflag1 = 0
	for skipfilm in ignorefilms:
		if eachfilm == skipfilm:
			skipflag1 = 1
			print('Skipping '+eachfilm+' due to film Sheet match')
			outputfile.write('\nSkipping '+eachfilm+' due to film Sheet match')
	if film1 != eachfilm and skipflag1 == 0:
		filmcomparison = [film1,eachfilm]
		ratings = [0,0]
		filmcomparison,ratings,actors = getfilminfo(filmcomparison,ratings,['actors'])
		actors1 = []
		actors2 = []
		for i in range(len(filmcomparison)):
			if filmcomparison[i] == film1:
				actors1 = actors1+[actors[i]]
			else:
				actors2 = actors2+[actors[i]]
		matchflag = 0
		for i in range(len(actors2)):
			skipflag2 = 0
			for skipactor in ignoreactors:
				if actors2[i] == skipactor:
					skipflag2 = 1
					print('Skipping '+actors2[i]+' due to actor Sheet match')
					outputfile.write('\nSkipping '+actors2[i]+' due to actor Sheet match')
			if skipflag2 == 0:
				for j in range(len(actors1)):
					if actors2[i] == actors1[j]:
						skipflag3 = 0
						for k in range(len(actors2)):
							for skipactor in ignoreactors:
								if actors2[k] == skipactor:
									for l in range(len(actors1)):
										if l != j and actors2[k] == actors1[l]:
											skipflag3 = 1
											skippedactor = actors2[k]
						if skipflag3 == 0:
							allfilms = allfilms+[eachfilm]
							allactors = allactors+[actors2[i]]
						else:
							print(actors2[i]+' is in '+eachfilm+' but skipping due to '+skippedactor+' being in it')
							outputfile.write('\n'+actors2[i]+' is in '+eachfilm+' but skipping due to '+skippedactor+' being in it')

# Print break line
print('\n**************************************************')
outputfile.write('\n\n**************************************************')

# Check special cases: a film with more than one actor connection

# Get unique film names
# Array to put unique film names
uniquefilms = []
# Run through all films
for film in allfilms:
	# For the first film, we know it's unique, so add it to uniquefilms array
	if len(uniquefilms) == 0:
		uniquefilms = uniquefilms+[film]
	# Otherwise we need to check
	else:
		# Flag to check if films have been added to uniquefilms array yet
		flag = 0
		# Run through the films already added to uniquefilms array
		for filmcheck in uniquefilms:
			# If the current film is already in the uniquefilms array, set flag
			if filmcheck == film:
				flag = 1
		# If the flag was never set, it's a unique film, so add it to the uniquefilms array
		if flag == 0:
			uniquefilms = uniquefilms+[film]

# Array to keep track of special films
specialfilms = []
# Run through unique films:
for film in uniquefilms:
	# Variable to count the number of actors in the film
	filmcount = 0
	# Run through all films:
	for filmcheck in allfilms:
		# Count them
		if filmcheck == film:
			filmcount = filmcount+1
	# Check if the film has multiple actors
	if filmcount > 1:
		specialfilms = specialfilms+[film]

# If there are special films
if len(specialfilms) > 0:
	# Print them and their actors
	print('\nSpecial films with multiple connecting actors!')
	outputfile.write('\n\nSpecial films with multiple connecting actors!')
	# Run through special films
	for film in specialfilms:
		# Print film name
		print('\n'+film)
		outputfile.write('\n\n'+film)
		# Run through all films
		for i in range(len(allfilms)):
			# Check if films match
			if allfilms[i] == film:
				# If they do, print the actor
				print('-- '+allactors[i])
				outputfile.write('\n-- '+allactors[i])

# Now to list everything alphabetically by actor name
print('\nAll connections alphabetically by actor')
outputfile.write('\n\nAll connections alphabetically by actor')

# Sort both actors and films alphabetically by actor name
# The format for numsort:
# numsort(arraytosort,arraytomatch,isstring,highestfirst)
# so isstring=1 because we're sorting strings
# and highestfirst=0 because for strings "highest" means Z
sortedactors,sortedfilms = numsort(allactors,allfilms,1,0)

# GOAL: Print all sorted actors and films, skipping the special ones
# GOAL: Also only print the actor once, and then all their films
# Array to keep track of printed actors
printedactors = []
# Run through sorted actors
for i in range(len(sortedactors)):
	# If there are any special films
	if len(specialfilms) > 0:
		# Run through them and check if the sorted film needs to be skipped
		# Flag to indicate a match
		flag = 0
		# Run through special films
		for film in specialfilms:
			# If there's a match, set flag
			if film == sortedfilms[i]:
				flag = 1
		# Only print if flag not set
		if flag == 0:
			# Only print actor's name once
			# If first printed actor, good to go
			if len(printedactors) == 0:
				print('\n'+sortedactors[i])
				print('-- '+sortedfilms[i])
				outputfile.write('\n\n'+sortedactors[i])
				outputfile.write('\n-- '+sortedfilms[i])
				# Add actor to list of printed actors
				printedactors = printedactors+[sortedactors[i]]
			# Otherwise check if actor printed already
			else:
				# Flag to indicate already printed
				flag2 = 0
				# Run through printedactors
				for actorcheck in printedactors:
					# If there is a match, set the flag
					if actorcheck == sortedactors[i]:
						flag2 = 1
				# If not printed yet, print out actor
				if flag2 == 0:
					print('\n'+sortedactors[i])
					print('-- '+sortedfilms[i])
					outputfile.write('\n\n'+sortedactors[i])
					outputfile.write('\n-- '+sortedfilms[i])
					# Add actor to list of printed actors
					printedactors = printedactors+[sortedactors[i]]
				# If actor already printed, just print the film
				else:
					print('-- '+sortedfilms[i])
					outputfile.write('\n-- '+sortedfilms[i])
	# If there are no special films, print all of them
	else:
		# Only print actor's name once
		# If first printed actor, good to go
		if len(printedactors) == 0:
			print('\n'+sortedactors[i])
			print('-- '+sortedfilms[i])
			outputfile.write('\n\n'+sortedactors[i])
			outputfile.write('\n-- '+sortedfilms[i])
			# Add actor to list of printed actors
			printedactors = printedactors+[sortedactors[i]]
		# Otherwise check if actor printed already
		else:
			# Flag to indicate already printed
			flag2 = 0
			# Run through printedactors
			for actorcheck in printedactors:
				# If there is a match, set the flag
				if actorcheck == sortedactors[i]:
					flag2 = 1
			# If not printed yet, print out actor
			if flag2 == 0:
				print('\n'+sortedactors[i])
				print('-- '+sortedfilms[i])
				outputfile.write('\n\n'+sortedactors[i])
				outputfile.write('\n-- '+sortedfilms[i])
				# Add actor to list of printed actors
				printedactors = printedactors+[sortedactors[i]]
			# If actor already printed, just print the film
			else:
				print('-- '+sortedfilms[i])
				outputfile.write('\n-- '+sortedfilms[i])

# Print a blank line at the end because that's what I like to do
print('')
outputfile.write('\n')

# Close output file
outputfile.close()
