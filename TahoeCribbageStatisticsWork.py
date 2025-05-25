# TahoeCribbageStatisticsWork.py

import numpy as np
import random

# Routine to count the number of each suit in a hand, for computing flushes:
def countsuits(hand):
	nD = 0
	nC = 0
	nH = 0
	nS = 0
	for i in range(len(hand)):
		if hand[i] == 'AD' or hand[i] == '2D' or hand[i] == '3D' or hand[i] == '4D' or hand[i] == '5D' or hand[i] == '6D' or hand[i] == '7D' or hand[i] == '8D' or hand[i] == '9D' or hand[i] == '10D' or hand[i] == 'JD' or hand[i] == 'QD' or hand[i] == 'KD':
			nD = nD+1
		elif hand[i] == 'AC' or hand[i] == '2C' or hand[i] == '3C' or hand[i] == '4C' or hand[i] == '5C' or hand[i] == '6C' or hand[i] == '7C' or hand[i] == '8C' or hand[i] == '9C' or hand[i] == '10C' or hand[i] == 'JC' or hand[i] == 'QC' or hand[i] == 'KC':
			nC = nC+1
		elif hand[i] == 'AH' or hand[i] == '2H' or hand[i] == '3H' or hand[i] == '4H' or hand[i] == '5H' or hand[i] == '6H' or hand[i] == '7H' or hand[i] == '8H' or hand[i] == '9H' or hand[i] == '10H' or hand[i] == 'JH' or hand[i] == 'QH' or hand[i] == 'KH':
			nH = nH+1
		elif hand[i] == 'AS' or hand[i] == '2S' or hand[i] == '3S' or hand[i] == '4S' or hand[i] == '5S' or hand[i] == '6S' or hand[i] == '7S' or hand[i] == '8S' or hand[i] == '9S' or hand[i] == '10S' or hand[i] == 'JS' or hand[i] == 'QS' or hand[i] == 'KS':
			nS = nS+1
	return nD,nC,nH,nS

# Main Routine, print starting info:
print('')
print('Statistics Work for Tahoe Cribbage')
print('')
print('By Alex Spacek')
print('July 2021 - June 2022')
print('')

# Flush Odds work:
print('Flush Odds')
print('')
print('Computing odds with simulations.')
print('')
deck = ['AD','2D','3D','4D','5D','6D','7D','8D','9D','10D','JD','QD','KD','AC','2C','3C','4C','5C','6C','7C','8C','9C','10C','JC','QC','KC','AH','2H','3H','4H','5H','6H','7H','8H','9H','10H','JH','QH','KH','AS','2S','3S','4S','5S','6S','7S','8S','9S','10S','JS','QS','KS']
print(str(len(deck))+' cards in the deck.')
print('')
TahoePointPerCardHand = 1
TahoePointForUpcardHand = 1
TahoePointPerCardCrib = 1
print('Tahoe points per card hand = '+str(TahoePointPerCardHand))
print('Tahoe points for upcard hand = '+str(TahoePointForUpcardHand))
print('Tahoe points per card crib = '+str(TahoePointPerCardCrib))
print('')

# Regular Cribbage Simulations:
print('Regular Cribbage')
print('')
ntrials = 1000000 # 1 million
print('ntrials = '+str(ntrials))
print('')
print('Drawing 6 random cards, seeing how many 4-card flushes we get.')
print('Also checking with upcard.')
print('Also discarding 2 random cards from each hand into crib to check for flushes with upcard.')
print('')
flush1 = 0
flush1up = 0
flush2 = 0
flush2up = 0
flush2crib = 0
for i in range(ntrials):
	# Create deck:
	newdeck = [val for val in deck]
	# Shuffle deck:
	random.shuffle(newdeck)
	# Deal out cards:
	hand1 = [newdeck[0],newdeck[2],newdeck[4],newdeck[6],newdeck[8],newdeck[10]]
	hand2 = [newdeck[1],newdeck[3],newdeck[5],newdeck[7],newdeck[9],newdeck[11]]
	# Randomly get upcard:
	newerdeck = newdeck[12:]
	upcard = random.choice(newerdeck)
	# Check if hand1 has a flush:
	nD1,nC1,nH1,nS1 = countsuits(hand1)
	if nD1 >= 4:
		flush1 = flush1+1
		if upcard[1] == 'D':
			flush1up = flush1up+1
	elif nC1 >= 4:
		flush1 = flush1+1
		if upcard[1] == 'C':
			flush1up = flush1up+1
	elif nH1 >= 4:
		flush1 = flush1+1
		if upcard[1] == 'H':
			flush1up = flush1up+1
	elif nS1 >= 4:
		flush1 = flush1+1
		if upcard[1] == 'S':
			flush1up = flush1up+1
	# Check if hand2 has a flush:
	nD2,nC2,nH2,nS2 = countsuits(hand2)
	if nD2 >= 4:
		flush2 = flush2+1
		if upcard[1] == 'D':
			flush2up = flush2up+1
	elif nC2 >= 4:
		flush2 = flush2+1
		if upcard[1] == 'C':
			flush2up = flush2up+1
	elif nH2 >= 4:
		flush2 = flush2+1
		if upcard[1] == 'H':
			flush2up = flush2up+1
	elif nS2 >= 4:
		flush2 = flush2+1
		if upcard[1] == 'S':
			flush2up = flush2up+1
	# Discard 2 random cards from each hand into the crib of player 2:
	card1a = random.choice(hand1)
	flag = 0
	while flag == 0:
		card1b = random.choice(hand1)
		if card1b != card1a:
			flag = 1
	card2a = random.choice(hand2)
	flag = 0
	while flag == 0:
		card2b = random.choice(hand2)
		if card2b != card2a:
			flag = 1
	crib2 = [card1a,card1b,card2a,card2b]
	# Check if crib2 has a flush:
	nDc,nCc,nHc,nSc = countsuits(crib2)
	if nDc == 4:
		if upcard[1] == 'D':
			flush2crib = flush2crib+1
	elif nCc == 4:
		if upcard[1] == 'C':
			flush2crib = flush2crib+1
	elif nHc == 4:
		if upcard[1] == 'H':
			flush2crib = flush2crib+1
	elif nSc == 4:
		if upcard[1] == 'S':
			flush2crib = flush2crib+1

# Print Regular Cribbage results:
print('Hand 1 flushes = {} = {:.4f} %'.format(flush1,flush1/ntrials*100))
print('Hand 1 upcard flushes = {} = {:.4f} % = {:.4f} % of flushes'.format(flush1up,flush1up/ntrials*100,flush1up/flush1*100))
print('')
print('Hand 2 flushes = {} = {:.2f} %'.format(flush2,flush2/ntrials*100))
print('Hand 2 upcard flushes = {} = {:.4f} % = {:.4f} % of flushes'.format(flush2up,flush2up/ntrials*100,flush2up/flush2*100))
print('')
print('Crib 2 flushes = {} = {:.4f} %'.format(flush2crib,flush2crib/ntrials*100))
print('')
normal1ptavg = (flush1*4+flush1up)/ntrials
print('Hand 1 avg flush points per hand assuming always going for flush = {:.6f}'.format(normal1ptavg))
normal2ptavg = (flush2*4+flush2up)/ntrials
print('Hand 2 avg flush points per hand assuming always going for flush = {:.6f}'.format(normal2ptavg))
normalcptavg = flush2crib*5/ntrials
print('Crib 2 avg flush points per hand assuming random discards = {:.6f}'.format(normalcptavg))
print('')

# Tahoe Cribbage Simulations:
print('Tahoe Cribbage')
print('')
ntrials = ntrials
print('ntrials = '+str(ntrials))
print('')
print('Drawing 9 random cards, seeing how many 7-card flushes we get.')
print('Also checking with upcard.')
print('Also putting 3 cards from deck into crib,')
print('and discarding 2 random cards from each hand into crib to check for flushes with upcard.')
print('')
flush1 = 0
flush1up = 0
flush2 = 0
flush2up = 0
flush2crib = 0
for i in range(ntrials):
	# Create deck:
	newdeck = [val for val in deck]
	# Shuffle deck:
	random.shuffle(newdeck)
	# Deal out cards:
	hand1 = [newdeck[0],newdeck[2],newdeck[4],newdeck[6],newdeck[8],newdeck[10],newdeck[12],newdeck[14],newdeck[16]]
	hand2 = [newdeck[1],newdeck[3],newdeck[5],newdeck[7],newdeck[9],newdeck[11],newdeck[13],newdeck[15],newdeck[17]]
	# Deal 3 cards to crib:
	crib2 = [newdeck[18],newdeck[19],newdeck[20]]
	# Randomly get upcard:
	newerdeck = newdeck[21:]
	upcard = random.choice(newerdeck)
	# Check if hand1 has a flush:
	nD1,nC1,nH1,nS1 = countsuits(hand1)
	if nD1 >= 7:
		flush1 = flush1+1
		if upcard[1] == 'D':
			flush1up = flush1up+1
	elif nC1 >= 7:
		flush1 = flush1+1
		if upcard[1] == 'C':
			flush1up = flush1up+1
	elif nH1 >= 7:
		flush1 = flush1+1
		if upcard[1] == 'H':
			flush1up = flush1up+1
	elif nS1 >= 7:
		flush1 = flush1+1
		if upcard[1] == 'S':
			flush1up = flush1up+1
	# Check if hand2 has a flush:
	nD2,nC2,nH2,nS2 = countsuits(hand2)
	if nD2 >= 7:
		flush2 = flush2+1
		if upcard[1] == 'D':
			flush2up = flush2up+1
	elif nC2 >= 7:
		flush2 = flush2+1
		if upcard[1] == 'C':
			flush2up = flush2up+1
	elif nH2 >= 7:
		flush2 = flush2+1
		if upcard[1] == 'H':
			flush2up = flush2up+1
	elif nS2 >= 7:
		flush2 = flush2+1
		if upcard[1] == 'S':
			flush2up = flush2up+1
	# Discard 2 random cards from each hand into the crib of player 2:
	card1a = random.choice(hand1)
	flag = 0
	while flag == 0:
		card1b = random.choice(hand1)
		if card1b != card1a:
			flag = 1
	card2a = random.choice(hand2)
	flag = 0
	while flag == 0:
		card2b = random.choice(hand2)
		if card2b != card2a:
			flag = 1
	crib2 = crib2+[card1a,card1b,card2a,card2b]
	# Check if crib2 has a flush:
	nDc,nCc,nHc,nSc = countsuits(crib2)
	if nDc == 7:
		if upcard[1] == 'D':
			flush2crib = flush2crib+1
	elif nCc == 7:
		if upcard[1] == 'C':
			flush2crib = flush2crib+1
	elif nHc == 7:
		if upcard[1] == 'H':
			flush2crib = flush2crib+1
	elif nSc == 7:
		if upcard[1] == 'S':
			flush2crib = flush2crib+1

# Print Tahoe Cribbage results:
print('Hand 1 flushes = {} = {:.4f} %'.format(flush1,flush1/ntrials*100))
print('Hand 1 upcard flushes = {} = {:.4f} % = {:.4f} % of flushes'.format(flush1up,flush1up/ntrials*100,flush1up/flush1*100))
print('')
print('Hand 2 flushes = {} = {:.4f} %'.format(flush2,flush2/ntrials*100))
print('Hand 2 upcard flushes = {} = {:.4f} % = {:.4f} % of flushes'.format(flush2up,flush2up/ntrials*100,flush2up/flush2*100))
print('')
print('Crib 2 flushes = {} = {:.6f} %'.format(flush2crib,flush2crib/ntrials*100))
print('')
tahoe1ptavg = (flush1*7+flush1up)/ntrials
newtahoe1ptavg = (flush1*7*TahoePointPerCardHand+flush1up*TahoePointForUpcardHand)/ntrials
print('Hand 1 avg flush points per hand assuming always going for flush = {:.6f}'.format(tahoe1ptavg))
print('Adjusted value = {:.6f}'.format(newtahoe1ptavg))
tahoe2ptavg = (flush2*7+flush2up)/ntrials
newtahoe2ptavg = (flush2*7*TahoePointPerCardHand+flush2up*TahoePointForUpcardHand)/ntrials
print('Hand 2 avg flush points per hand assuming always going for flush = {:.6f}'.format(tahoe2ptavg))
print('Adjusted value = {:.6f}'.format(newtahoe2ptavg))
tahoecptavg = flush2crib*8/ntrials
newtahoecptavg = flush2crib*8*TahoePointPerCardCrib/ntrials
print('Crib 2 avg flush points per hand assuming random discards = {:.7f}'.format(tahoecptavg))
print('Adjusted value = {:.7f}'.format(newtahoecptavg))
print('')
print('Comparisons:')
print('Hand 1 normal avg / Tahoe avg = {:.2f}'.format(normal1ptavg/tahoe1ptavg))
print('Hand 2 normal avg / Tahoe avg = {:.2f}'.format(normal2ptavg/tahoe2ptavg))
print('Crib 2 normal avg / Tahoe avg = {:.2f}'.format(normalcptavg/tahoecptavg))
print('')
print('Hand 1 normal avg / Tahoe adjusted avg = {:.2f}'.format(normal1ptavg/newtahoe1ptavg))
print('Hand 2 normal avg / Tahoe adjusted avg = {:.2f}'.format(normal2ptavg/newtahoe2ptavg))
print('Crib 2 normal avg / Tahoe adjusted avg = {:.2f}'.format(normalcptavg/newtahoecptavg))
print('')

# Tahoe Cribbage Simulations - Only 5 Cards Required:
print('Tahoe Cribbage - Only 5 Cards Required')
print('')
ntrials = ntrials
print('ntrials = '+str(ntrials))
print('')
print('Drawing 9 random cards, seeing how many >=5-card flushes we get.')
print('Also checking with upcard.')
print('Also putting 3 cards from deck into crib,')
print('and discarding 2 random cards from each hand into crib to check for flushes with upcard.')
print('')
nflush1 = 0
flush1 = 0
flush1up = 0
nflush2 = 0
flush2 = 0
flush2up = 0
nflush2crib = 0
flush2crib = 0
for i in range(ntrials):
	# Create deck:
	newdeck = [val for val in deck]
	# Shuffle deck:
	random.shuffle(newdeck)
	# Deal out cards:
	hand1 = [newdeck[0],newdeck[2],newdeck[4],newdeck[6],newdeck[8],newdeck[10],newdeck[12],newdeck[14],newdeck[16]]
	hand2 = [newdeck[1],newdeck[3],newdeck[5],newdeck[7],newdeck[9],newdeck[11],newdeck[13],newdeck[15],newdeck[17]]
	# Deal 3 cards to crib:
	crib2 = [newdeck[18],newdeck[19],newdeck[20]]
	# Randomly get upcard:
	newerdeck = newdeck[21:]
	upcard = random.choice(newerdeck)
	# Check if hand1 has a flush:
	nD1,nC1,nH1,nS1 = countsuits(hand1)
	if nD1 >= 5:
		nflush1 = nflush1+1
		if nD1 < 7:
			flush1 = flush1+nD1
		else:
			flush1 = flush1+7
		if upcard[1] == 'D':
			flush1up = flush1up+1
	elif nC1 >= 5:
		nflush1 = nflush1+1
		if nC1 < 7:
			flush1 = flush1+nC1
		else:
			flush1 = flush1+7
		if upcard[1] == 'C':
			flush1up = flush1up+1
	elif nH1 >= 5:
		nflush1 = nflush1+1
		if nH1 < 7:
			flush1 = flush1+nH1
		else:
			flush1 = flush1+7
		if upcard[1] == 'H':
			flush1up = flush1up+1
	elif nS1 >= 5:
		nflush1 = nflush1+1
		if nS1 < 7:
			flush1 = flush1+nS1
		else:
			flush1 = flush1+7
		if upcard[1] == 'S':
			flush1up = flush1up+1
	# Check if hand2 has a flush:
	nD2,nC2,nH2,nS2 = countsuits(hand2)
	if nD2 >= 5:
		nflush2 = nflush2+1
		if nD2 < 7:
			flush2 = flush2+nD2
		else:
			flush2 = flush2+7
		if upcard[1] == 'D':
			flush2up = flush2up+1
	elif nC2 >= 5:
		nflush2 = nflush2+1
		if nC2 < 7:
			flush2 = flush2+nC2
		else:
			flush2 = flush2+7
		if upcard[1] == 'C':
			flush2up = flush2up+1
	elif nH2 >= 5:
		nflush2 = nflush2+1
		if nH2 < 7:
			flush2 = flush2+nH2
		else:
			flush2 = flush2+7
		if upcard[1] == 'H':
			flush2up = flush2up+1
	elif nS2 >= 5:
		nflush2 = nflush2+1
		if nS2 < 7:
			flush2 = flush2+nS2
		else:
			flush2 = flush2+7
		if upcard[1] == 'S':
			flush2up = flush2up+1
	# Discard 2 random cards from each hand into the crib of player 2:
	card1a = random.choice(hand1)
	flag = 0
	while flag == 0:
		card1b = random.choice(hand1)
		if card1b != card1a:
			flag = 1
	card2a = random.choice(hand2)
	flag = 0
	while flag == 0:
		card2b = random.choice(hand2)
		if card2b != card2a:
			flag = 1
	crib2 = crib2+[card1a,card1b,card2a,card2b]
	# Check if crib2 has a flush:
	nDc,nCc,nHc,nSc = countsuits(crib2)
	if nDc >= 5:
		if upcard[1] == 'D':
			nflush2crib = nflush2crib+1
			if nDc < 7:
				flush2crib = flush2crib+nDc
			else:
				flush2crib = flush2crib+7
	elif nCc >= 5:
		if upcard[1] == 'C':
			nflush2crib = nflush2crib+1
			if nCc < 7:
				flush2crib = flush2crib+nCc
			else:
				flush2crib = flush2crib+7
	elif nHc >= 5:
		if upcard[1] == 'H':
			nflush2crib = nflush2crib+1
			if nHc < 7:
				flush2crib = flush2crib+nHc
			else:
				flush2crib = flush2crib+7
	elif nSc >= 5:
		if upcard[1] == 'S':
			nflush2crib = nflush2crib+1
			if nSc < 7:
				flush2crib = flush2crib+nSc
			else:
				flush2crib = flush2crib+7

# Print Tahoe Cribbage 5-Card Flush results:
print('Hand 1 flushes = {} = {:.4f} %'.format(nflush1,nflush1/ntrials*100))
print('Hand 1 upcard flushes = {} = {:.4f} % = {:.4f} % of flushes'.format(flush1up,flush1up/ntrials*100,flush1up/nflush1*100))
print('')
print('Hand 2 flushes = {} = {:.4f} %'.format(nflush2,nflush2/ntrials*100))
print('Hand 2 upcard flushes = {} = {:.4f} % = {:.4f} % of flushes'.format(flush2up,flush2up/ntrials*100,flush2up/nflush2*100))
print('')
print('Crib 2 flushes = {} = {:.6f} %'.format(nflush2crib,nflush2crib/ntrials*100))
print('')
tahoe1ptavg = (flush1+flush1up)/ntrials
newtahoe1ptavg = (flush1*TahoePointPerCardHand+flush1up*TahoePointForUpcardHand)/ntrials
print('Hand 1 avg flush points per hand assuming always going for flush = {:.6f}'.format(tahoe1ptavg))
print('Adjusted value = {:.6f}'.format(newtahoe1ptavg))
tahoe2ptavg = (flush2+flush2up)/ntrials
newtahoe2ptavg = (flush2*TahoePointPerCardHand+flush2up*TahoePointForUpcardHand)/ntrials
print('Hand 2 avg flush points per hand assuming always going for flush = {:.6f}'.format(tahoe2ptavg))
print('Adjusted value = {:.6f}'.format(newtahoe2ptavg))
tahoecptavg = (flush2crib+1)/ntrials
newtahoecptavg = (flush2crib+1)*TahoePointPerCardCrib/ntrials
print('Crib 2 avg flush points per hand assuming random discards = {:.7f}'.format(tahoecptavg))
print('Adjusted value = {:.7f}'.format(newtahoecptavg))
print('')
print('Comparisons:')
print('Hand 1 normal avg / Tahoe avg = {:.2f}'.format(normal1ptavg/tahoe1ptavg))
print('Hand 2 normal avg / Tahoe avg = {:.2f}'.format(normal2ptavg/tahoe2ptavg))
print('Crib 2 normal avg / Tahoe avg = {:.2f}'.format(normalcptavg/tahoecptavg))
print('')
print('Hand 1 normal avg / Tahoe adjusted avg = {:.2f}'.format(normal1ptavg/newtahoe1ptavg))
print('Hand 2 normal avg / Tahoe adjusted avg = {:.2f}'.format(normal2ptavg/newtahoe2ptavg))
print('Crib 2 normal avg / Tahoe adjusted avg = {:.2f}'.format(normalcptavg/newtahoecptavg))
print('')
