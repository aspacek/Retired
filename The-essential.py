######################
## The-essential.py ##
######################

##
## Written by Alex Spacek
## March 2025
## Last updated: March 2025
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

import requests

import time

import locale

from pathlib import Path

from shutil import copyfile

import os

sys.path.insert(0, "../Overrated-underrated-check")
from Getlistfilms import getlistfilms

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

# URL of New York Times Book of Movies: The Essential 1,000 Films to See (2019 edition)
url1 = 'https://letterboxd.com/chloeslate/list/the-new-york-times-book-of-movies-the-essential/'

# URL of 1001 Movies You Must See Before You Die (2024 Edition)
url2 = 'https://letterboxd.com/gubarenko/list/1001-movies-you-must-see-before-you-die-2024/'

# Need to read in names and rating of all rated films
# Use getlistinfo; don't need ratings
getratings = 0
films1 = getlistfilms(url1,getratings)
films2 = getlistfilms(url2,getratings)

print('\nNumber of films:')
print('NYT Essential 1,000: '+str(len(films1)))
print('1001 Movies: '+str(len(films2)))

# Find films in both lists
filmsinboth = []
for film1 in films1:
	for film2 in films2:
		if film1 == film2:
			filmsinboth = filmsinboth+[film1]

print('\nFilms in both lists: '+str(len(filmsinboth)))
print('')
for i in range(len(filmsinboth)):
	print(str(i+1)+' '+filmsinboth[i])
print('')
