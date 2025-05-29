################################
## The-nonsensical-toplist.py ##
################################

##
## Written by Alex Spacek
## December 2020
## Last updated: February 2025
##

############################################################################
############################################################################

##
## Imports
##

import requests

# sys module - reads in input values
#            - exits program on error
import sys

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

# Verbose?
# 0 = no
# 1 = print some details of run out
# 2 = print all details of run out
verbose = 1

# The points:
points = [200,160,130,110,100,90,80,70,60,50,45,40,35,30,25,20,18,16,14,12,10,9,8,7,6,5,4,3,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

# All of the lists that will be used:
alltime = 2025-1900
url = []
weight = []
# 0
# James Rolfe’s Top 30 Favorite Films (2010)
url = url+['https://boxd.it/PVyC']
weight = weight+[(2010-1900)/alltime*(1/4)]
# 1
# James Rolfe’s Top 50 Favorite Films (2017)
url = url+['https://boxd.it/14yz8']
weight = weight+[(2017-1900)/alltime*(3/4)]
# 2
# Sean Chandler’s Top 10 Favorite Movies (2018)
url = url+['https://boxd.it/2HmFq']
weight = weight+[(2018-1900)/alltime*(1/4)]
# 3
# William Wyler’s 10 Greatest Films Of All Time
url = url+['https://boxd.it/1in8o']
weight = weight+[(1977-1900)/alltime]
# 4
# Sight And Sound Magazine’s 10 Best Movies (1972)
url = url+['https://boxd.it/1in7q']
weight = weight+[(1972-1900)/alltime*(1/3)]
# 5
# Sight And Sound Magazine’s 10 Best Movies (1962)
url = url+['https://boxd.it/1in6s']
weight = weight+[(1962-1900)/alltime*(1/3)]
# 6
# Sight And Sound Magazine’s 10 Best Movies (1952)
url = url+['https://boxd.it/1in5a']
weight = weight+[(1952-1900)/alltime*(1/3)]
# 7
# Orson Welles’ 12 Best Movies Of All Time
url = url+['https://boxd.it/1ifla']
weight = weight+[(1977-1900)/alltime]
# 8
# Arthur Knight’s 10 Best Movies Of All Time
url = url+['https://boxd.it/1in3y']
weight = weight+[(1977-1900)/alltime]
# 9
# Jack Lemmon’s 10 “Second-Greatest” Films Of All Time
url = url+['https://boxd.it/1in9G']
weight = weight+[(1977-1900)/alltime]
# 10
# Luis Bunuel’s 9 Best Movies Of All Time
url = url+['https://boxd.it/1in2K']
weight = weight+[(1977-1900)/alltime]
# 11
# Sean Chandler’s Top 20 Favorite Movies (2020)
url = url+['https://boxd.it/4AU4M']
weight = weight+[(2020-1900)/alltime*(3/4)]
# 12
# WatchMojo’s Top 20 Greatest Movies of All Time
url = url+['https://boxd.it/8PLUK']
weight = weight+[(2020-1900)/alltime]
# 13
# Moogic’s Favorite Films Of All Time, Ranked
url = url+['https://boxd.it/Urna']
weight = weight+[1.0]
# 14
# Letterboxd 50 All-Time Most Consistently Highest Rated Films
url = url+['https://boxd.it/2PnDc']
weight = weight+[1.0]
# 15
# Top 100 Highest Rated Films By My Letterboxd Friends
url = url+['https://boxd.it/52xxi']
weight = weight+[1.0]
# 16
# Walter Matthau’s 10 Favorite Comedies Of All Time
url = url+['https://boxd.it/cqxrK']
weight = weight+[1/5*(1983-1900)/alltime]
# 17
# Jane Fonda’s 4 Best Motion Pictures Of All Time
url = url+['https://boxd.it/cqj0A']
weight = weight+[(1980-1900)/alltime]
# 18
# Grace Kelly’s 5 Best Motion Pictures Of All Time
url = url+['https://boxd.it/cqj4M']
weight = weight+[(1980-1900)/alltime]
# 19
# John Wayne’s 5 Best Motion Pictures Of All Time
url = url+['https://boxd.it/cqjaK']
weight = weight+[(1980-1900)/alltime]
# 20
# Robert Duvall’s 10 Favorite Movies Of All Time
url = url+['https://boxd.it/cqxBU']
weight = weight+[(1983-1900)/alltime]
# 21
# Sean Connery’s 10 Favorite Movies Of All Time
url = url+['https://boxd.it/cqDQc']
weight = weight+[(1983-1900)/alltime]
# 22
# Richard D. Zanuck’s 10 Favorite Movies Of All Time
url = url+['https://boxd.it/cqEbE']
weight = weight+[(1983-1900)/alltime]
# 23
# Irwin Allen’s 10 Favorite Movies Of All Time
url = url+['https://boxd.it/cqEmC']
weight = weight+[(1983-1900)/alltime]
# 24
# Roger Corman’s 10 Favorite Movies Of All Time
url = url+['https://boxd.it/cqEx6']
weight = weight+[(1983-1900)/alltime]

# Sight & Sound 2012 Poll - Top 5 Films Of Each Decade
url2 = 'https://boxd.it/13Hli'

url3 = []
points3 = []
# 0
# Sean Chandler’s 10 Movies Everyone Must Watch
url3 = url3+['https://boxd.it/5AgG6']
points3 = points3+[(points[0]+points[1]+points[2]+points[3]+points[4]+points[5]+points[6]+points[7]+points[8]+points[9])/10*(2020-1900)/alltime*(1/2)]
# 1
# Sean Chandler’s 5 Perfect Movies
url3 = url3+['https://boxd.it/5Ah8O']
points3 = points3+[(points[0]+points[1]+points[2]+points[3]+points[4])/5*(2020-1900)/alltime*(1/2)]

url4 = []
bonus = []
# 0
# Moogic’s Favorite Film From Every Year
url4 = url4+['https://boxd.it/13lT8']
bonus = bonus+[points[9]]
# 1
# The Essential 490 (Films/Movies) (to See/You Must See) (Before You Die)
url4 = url4+['https://boxd.it/47jFe']
bonus = bonus+[points[14]]
#2
# Critically Popular Films - Money, Awards, and Critical Acclaim
url4 = url4+['https://boxd.it/anM7G']
bonus = bonus+[points[11]]

# Read in all films and compute scores:
films = []
scores = []
# Run through all list urls:
for i in range(len(url)):
	if verbose >= 1:
		print('\n'+url[i])
	# Grab source code for the first page:
	r = requests.get(url[i])
	source = r.text
	if verbose == 2:
		print ('***** source *****')
		print (source)
		print ('*****')
	# Find the number of pages
	pagecheck = list(findstrings('/page/',source))
	if pagecheck == []:
		pages = 1
	else:
		pages = int(getstrings('last','/page/','/">',source))
	if verbose >= 1:
		print('pages = '+str(pages))
	# Loop through all pages and grab all the film titles:
	films_temp = []
	# Start on page 1, get the films:
	text_blocks = getstrings('all','<li class="poster-container','</li>',source)
	if verbose == 2:
		print('***** text_blocks *****')
		print(text_blocks)
		print('*****')
	for block in text_blocks:
		films_temp = films_temp+[getstrings('first','data-film-slug="','"',block)]
	if verbose >= 1 and pages == 1:
		print('***** film_temp *****')
		print(films_temp)
		print ('*****')
	# Now loop through the rest of the pages:
	if pages > 1:
		for page in range(pages-1):
			# Start on page 2:
			page = str(page + 2)
			# Grab source code of the page:
			r = requests.get(url[i]+'page/'+page+'/')
			source = r.text
			if verbose == 2:
				print ('***** source *****')
				print (source)
				print ('*****')
			# Get films:
			text_blocks = getstrings('all','<li class="poster-container','</li>',source)
			if verbose == 2:
				print('***** text_blocks *****')
				print(text_blocks)
				print('*****')
			for block in text_blocks:
				films_temp = films_temp+[getstrings('first','data-film-slug="','"',block)]
		if verbose >= 1:
			print('***** film_temp *****')
			print(films_temp)
			print ('*****')
	# Correct points or films for current list:
	points_temp = [val for val in points]
	if i == 0:
		points_temp.insert(6,points[6])
		points_temp.insert(6,points[6])
	elif i == 1:
		points_temp.insert(5,points[5])
		points_temp.insert(5,points[5])
		points_temp.insert(37,points[35])
		points_temp.insert(44,points[41])
		points_temp.insert(46,points[42])
		points_temp.insert(46,points[42])
	elif i == 2:
		points_temp.insert(0,points[0])
		points_temp.insert(0,points[0])
		points_temp.insert(10,points[8])
	elif i == 4:
		points_temp[5] = points[4]
		points_temp[8] = points[7]
		points_temp[10] = points[9]
	elif i == 5:
		points_temp[4] = points[3]
		points_temp[6] = points[5]
		points_temp[7] = points[5]
	elif i == 6:
		points_temp[2] = points[1]
		points_temp[5] = points[4]
		points_temp[7] = points[6]
		points_temp[8] = points[6]
		points_temp[10] = points[9]
		points_temp[11] = points[9]
	elif i == 8:
		points_temp.insert(1,points[1])
		points_temp.insert(1,points[1])
	elif i == 12:
		films_temp = films_temp[0:20]
	# Loop through films, compute scores, add to film's previous score or add new film to list if needed:
	if verbose >= 1:
		print('len(films_temp) = '+str(len(films_temp)))
		print('*****')
	for j in range(len(films_temp)):
		if j < len(points_temp):
			if verbose >= 1:
				print('i '+str(i)+' j '+str(j)+' '+films_temp[j])
			scores_temp = points_temp[j]*weight[i]
			priorflag = 0
			for k in range(len(films)):
				if films_temp[j] == films[k]:
					scores[k] = scores[k]+scores_temp
					priorflag = 1
			if priorflag == 0:
				films = films+[films_temp[j]]
				scores = scores+[scores_temp]
	print('*****')
	for j in range(len(films)):
		print(films[j]+' '+str(scores[j]))

# Compute extra points for all films:
# First, the S&S 2012 list:
# Grab source code for the first page:
r = requests.get(url2)
source = r.text
# Find the number of pages
pagecheck = list(findstrings('/page/',source))
if pagecheck == []:
	pages = 1
else:
	pages = int(getstrings('last','/page/','/">',source))
# Loop through all pages and grab all the film titles:
films_temp = []
# Start on page 1, get the films:
text_blocks = getstrings('all','<li class="poster-container','</li>',source)
for block in text_blocks:
	films_temp = films_temp+[getstrings('first','data-film-slug="','"',block)]
# Now loop through the rest of the pages:
if pages > 1:
	for page in range(pages-1):
		# Start on page 2:
		page = str(page + 2)
		# Grab source code of the page:
		r = requests.get(url2+'page/'+page+'/')
		source = r.text
		# Get films:
		text_blocks = getstrings('all','<li class="poster-container','</li>',source)
		for block in text_blocks:
			films_temp = films_temp+[getstrings('first','data-film-slug="','"',block)]
# Compute scores:
if verbose >= 1:
	print(url2)
	print(len(films_temp))
newpoints = [points[0]/9,points[1]/9,points[2]/9,points[3]/9,points[4]/9]
excluded = [0,1,2,3,4,6,7,8,9,11,12,13,14,61,62,63,64]
for i in range(len(films_temp)):
	excludeflag = 0
	for j in range(len(excluded)):
		if i == excluded[j]:
			excludeflag = 1
	if excludeflag == 0:
		if verbose >= 1:
			print('i '+str(i)+' '+films_temp[i])
		scores_temp = newpoints[i%5]
		priorflag = 0
		for j in range(len(films)):
			if films_temp[i] == films[j]:
				scores[j] = scores[j]+scores_temp
				priorflag = 1
		if priorflag == 0:
			films = films+[films_temp[i]]
			scores = scores+[scores_temp]

# Next, the Sean Chandler unranked lists:
for i in range(len(url3)):
	# Grab source code for the first page:
	r = requests.get(url3[i])
	source = r.text
	# Find the number of pages
	pagecheck = list(findstrings('/page/',source))
	if pagecheck == []:
		pages = 1
	else:
		pages = int(getstrings('last','/page/','/">',source))
	# Loop through all pages and grab all the film titles:
	films_temp = []
	# Start on page 1, get the films:
	text_blocks = getstrings('all','<li class="poster-container','</li>',source)
	for block in text_blocks:
		films_temp = films_temp+[getstrings('first','data-film-slug="','"',block)]
	# Now loop through the rest of the pages:
	if pages > 1:
		for page in range(pages-1):
			# Start on page 2:
			page = str(page + 2)
			# Grab source code of the page:
			r = requests.get(url3[i]+'page/'+page+'/')
			source = r.text
			# Get films:
			text_blocks = getstrings('all','<li class="poster-container','</li>',source)
			for block in text_blocks:
				films_temp = films_temp+[getstrings('first','data-film-slug="','"',block)]
	# Loop through films, compute scores, add to film's previous score or add new film to list if needed:
	if verbose >= 1:
		print(url3[i])
		print(len(films_temp))
	for j in range(len(films_temp)):
		if verbose >= 1:
			print('i '+str(i)+' j '+str(j)+' '+films_temp[j])
		scores_temp = points3[i]
		priorflag = 0
		for k in range(len(films)):
			if films_temp[j] == films[k]:
				scores[k] = scores[k]+scores_temp
				priorflag = 1
		if priorflag == 0:
			films = films+[films_temp[j]]
			scores = scores+[scores_temp]

# Next, all of the bonus points:
for i in range(len(url4)):
	# Grab source code for the first page:
	r = requests.get(url4[i])
	source = r.text
	# Find the number of pages
	pagecheck = list(findstrings('/page/',source))
	if pagecheck == []:
		pages = 1
	else:
		pages = int(getstrings('last','/page/','/">',source))
	# Loop through all pages and grab all the film titles:
	films_temp = []
	# Start on page 1, get the films:
	text_blocks = getstrings('all','<li class="poster-container','</li>',source)
	for block in text_blocks:
		films_temp = films_temp+[getstrings('first','data-film-slug="','"',block)]
	# Now loop through the rest of the pages:
	if pages > 1:
		for page in range(pages-1):
			# Start on page 2:
			page = str(page + 2)
			# Grab source code of the page:
			r = requests.get(url4[i]+'page/'+page+'/')
			source = r.text
			# Get films:
			text_blocks = getstrings('all','<li class="poster-container','</li>',source)
			for block in text_blocks:
				films_temp = films_temp+[getstrings('first','data-film-slug="','"',block)]
	# Loop through films and apply boosts to films already in the main list:
	if verbose >= 1:
		print(url4[i])
		print(len(films_temp))
	for j in range(len(films_temp)):
		if verbose >= 1:
			print('i '+str(i)+' j '+str(j)+' '+films_temp[j])
		scores_temp = bonus[i]
		for k in range(len(films)):
			if films_temp[j] == films[k]:
				scores[k] = scores[k]+scores_temp

# Sort everything by score:
films_sorted = [fnam for fnum, fnam in sorted(zip(scores,films))]
films_sorted.reverse()
scores_sorted = [val for val in scores]
scores_sorted.sort()
scores_sorted.reverse()

# Print out results:
print('')
for i in range(len(films_sorted)):
	print('{:3d} - {} - {:6.4f}'.format(i+1,films_sorted[i],scores_sorted[i]))
print('')
