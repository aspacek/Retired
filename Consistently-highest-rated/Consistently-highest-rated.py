###################################
## Consistently-highest-rated.py ##
###################################

##
## Written by Alex Spacek
## August 2020
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

# numpy module - compute average and standard deviation
import numpy as np

# time module - lets us wait
import time

import requests

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from pathlib import Path

sys.path.insert(0, "../../Letterboxd/General-league-routines")
from Findstrings import findstrings
from Getstrings import getstrings

############################################################################
############################################################################

##
## Main Routine
##

# How long to wait between Letterboxd page reads, in seconds
wait_time_secs = 15
# Read in all films:
# The base url:
url = 'https://letterboxd.com/dave/list/official-top-250-narrative-feature-films/'
# Grab source code for the first page:
r = requests.get(url)
source = r.text
time.sleep(wait_time_secs)
# Find the number of pages
pages = int(getstrings('last','/dave/list/official-top-250-narrative-feature-films/page/','/">',source))
# Loop through all pages and grab all the film titles:
if pages > 1:
	pageflag = 1
else:
	pageflag = 0
# Initialize results:
films = []
# Start on page 1, get the films:
films = films+getstrings('all','data-film-slug="','"',source)
# Now loop through the rest of the pages:
if pageflag == 1:
	for page in range(pages-1):
		# Start on page 2:
		page = str(page + 2)
		# Grab source code of the page:
		r = requests.get(url+'page/'+page+'/')
		source = r.text
		time.sleep(wait_time_secs)
		# Get films:
		films = films+getstrings('all','data-film-slug="','"',source)

# Read in data
scores = []
options = Options()
options.binary_location = '/Applications/Firefox.app/Contents/MacOS/firefox'
service_obj = Service("/opt/local/bin/geckodriver") 
driver = webdriver.Firefox(service=service_obj, options=options)
datapath = Path('Saved-data.csv')
for i in range(len(films)):
	print('\n'+films[i])
	# First check if film data already exists:
	alreadydone = 0
	if datapath.exists():
		# See if film data is already available:
		oldfilm = []
		oldscore = []
		with open('Saved-data.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				oldfilm = oldfilm+[row[0]]
				oldscore = oldscore+[row[1]]
		# oldscore are floats:
		oldscore = [float(item) for item in oldscore]
		# Check if current film is listed:
		for j in range(len(oldfilm)):
			if oldfilm[j] == films[i]:
				alreadydone = 1
				scores = scores+[oldscore[j]]
	if alreadydone == 0:
		stars = [0 for num in range(10)]
		checkit = 0
		errorcount = 0
		while checkit == 0:
			if errorcount == 100:
				sys.exit('ERROR - in function "MAIN" of "Consistently-highest-rated.py" - Checked 100 times for the ratings of '+films[i]+' and found that at least one of the ratings bins was 0 every time.')
			driver.get('https://letterboxd.com/film/'+films[i]+'/')
			html = driver.find_element("id","html")
			text = html.text
			noratingscheck1 = list(findstrings(' half-★ rating',text))
			noratingscheck2 = list(findstrings(' ★ rating',text))
			noratingscheck3 = list(findstrings(' ★½ rating',text))
			noratingscheck4 = list(findstrings(' ★★ rating',text))
			noratingscheck5 = list(findstrings(' ★½ rating',text))
			noratingscheck6 = list(findstrings(' ★★★ rating',text))
			noratingscheck7 = list(findstrings(' ★½ rating',text))
			noratingscheck8 = list(findstrings(' ★★★★ rating',text))
			noratingscheck9 = list(findstrings(' ★★★★½ rating',text))
			noratingscheck10 = list(findstrings(' ★★★★★ rating',text))
			checkit = 1
			if noratingscheck1 == []:
				print('-- NO 1/2 STAR RATINGS')
				checkit = 0
				errorcount = errorcount+1
			elif noratingscheck2 == []:
				print('-- NO 1 STAR RATINGS')
				checkit = 0
				errorcount = errorcount+1
			elif noratingscheck3 == []:
				print('-- NO 1 1/2 STAR RATINGS')
				checkit = 0
				errorcount = errorcount+1
			elif noratingscheck4 == []:
				print('-- NO 2 STAR RATINGS')
				checkit = 0
				errorcount = errorcount+1
			elif noratingscheck5 == []:
				print('-- NO 2 1/2 STAR RATINGS')
				checkit = 0
				errorcount = errorcount+1
			elif noratingscheck6 == []:
				print('-- NO 3 STAR RATINGS')
				checkit = 0
				errorcount = errorcount+1
			elif noratingscheck7 == []:
				print('-- NO 3 1/2 STAR RATINGS')
				checkit = 0
				errorcount = errorcount+1
			elif noratingscheck8 == []:
				print('-- NO 4 STAR RATINGS')
				checkit = 0
				errorcount = errorcount+1
			elif noratingscheck9 == []:
				print('-- NO 4 1/2 STAR RATINGS')
				checkit = 0
				errorcount = errorcount+1
			elif noratingscheck10 == []:
				print('-- NO 5 STAR RATINGS')
				checkit = 0
				errorcount = errorcount+1
		split1 = text.split(" half-★ rating",1)[0]
		split2 = split1.split("★\n",1)[-1]
		stars[0] = int(split2.replace(',', ''))
		split1 = text.split(" ★ rating",1)[0]
		split2 = split1.split(")\n",1)[-1]
		stars[1] = int(split2.replace(',', ''))
		split1 = text.split(" ★½ rating",1)[0]
		split2 = split1.split(")\n",2)[-1]
		stars[2] = int(split2.replace(',', ''))
		split1 = text.split(" ★★ rating",1)[0]
		split2 = split1.split(")\n",3)[-1]
		stars[3] = int(split2.replace(',', ''))
		split1 = text.split(" ★★½ rating",1)[0]
		split2 = split1.split(")\n",4)[-1]
		stars[4] = int(split2.replace(',', ''))
		split1 = text.split(" ★★★ rating",1)[0]
		split2 = split1.split(")\n",5)[-1]
		stars[5] = int(split2.replace(',', ''))
		split1 = text.split(" ★★★½ rating",1)[0]
		split2 = split1.split(")\n",6)[-1]
		stars[6] = int(split2.replace(',', ''))
		split1 = text.split(" ★★★★ rating",1)[0]
		split2 = split1.split(")\n",7)[-1]
		stars[7] = int(split2.replace(',', ''))
		split1 = text.split(" ★★★★½ rating",1)[0]
		split2 = split1.split(")\n",8)[-1]
		stars[8] = int(split2.replace(',', ''))
		split1 = text.split(" ★★★★★ rating",1)[0]
		split2 = split1.split(")\n",9)[-1]
		stars[9] = int(split2.replace(',', ''))
		print(str(stars[0])+' '+str(stars[1])+' '+str(stars[2])+' '+str(stars[3])+' '+str(stars[4])+' '+str(stars[5])+' '+str(stars[6])+' '+str(stars[7])+' '+str(stars[8])+' '+str(stars[9]))
		# Combine all ratings into single array:
		ratings = []
		ratings = ratings+[0.5 for num in range(stars[0])]
		ratings = ratings+[1.0 for num in range(stars[1])]
		ratings = ratings+[1.5 for num in range(stars[2])]
		ratings = ratings+[2.0 for num in range(stars[3])]
		ratings = ratings+[2.5 for num in range(stars[4])]
		ratings = ratings+[3.0 for num in range(stars[5])]
		ratings = ratings+[3.5 for num in range(stars[6])]
		ratings = ratings+[4.0 for num in range(stars[7])]
		ratings = ratings+[4.5 for num in range(stars[8])]
		ratings = ratings+[5.0 for num in range(stars[9])]
		# Compute average - standard deviation for the film:
		avg = np.average(ratings)
		stddev = np.std(ratings)
		# Record the score:
		scores = scores+[avg-stddev]
		# Write films and scores to file:
		with open('Saved-data.csv', mode='w') as outfile:
			csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for j in range(i+1):
				csvwriter.writerow([films[j],scores[j]])

driver.quit()

# Sort everything by score:
original = [num+1 for num in range(len(films))]
soriginal = [fnam for fnum, fnam in sorted(zip(scores,original))]
soriginal.reverse()
sfilms = [fnam for fnum, fnam in sorted(zip(scores,films))]
sfilms.reverse()
scores.sort()
scores.reverse()

# Print out results:
print('')
for i in range(len(sfilms)):
	print('{:3d} - {:3d} - {:3d} - {} - {:6.4f}'.format(i+1,soriginal[i],soriginal[i]-(i+1),sfilms[i],scores[i]))
print('')
