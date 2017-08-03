#!/usr/bin/env python

import sys
from diceprob import *

def maxtable(d,n):
	x = 0.
	for v in xrange(1,d+1):
		x = maxprob(d,n,v)
		if x >= 0.5:
			x = int(v)
			break
	x2 = 0.
	for v in xrange(1,d+1):
		x2 = maxprob(d,n,v)
		if x2 >= 0.8:
			x2 = int(v)
			break
	for v in xrange(1,d+1):
		p = maxprob(d,n,v)
		c = maxchance(d,n,v)
		yield d,n,v,p,c,x,x2


# Just a little color...
# python dicemax.py | awk -F, '$2<=3{print}' | column -s, -t | awk '$2==2{printf "\033[93m"} $2==3{printf "\033[91m"} {print} {printf "\033[0m"}' | column -s, -t | less -RS

if __name__ == '__main__':
	
	def round_str(v,d=3):
		p = pow(10,3)
		check = 1./p
		if v < check:
			return '0.'+'0'*d
		return str(int(v*p)/float(p))
	
	sep = ','
	print sep.join(['d','n','v','mxprob','mxchance','split_1-2','split_7-8'])
	for d in (4,6,8,12,20):
		for n in xrange(1,d+1):
			print '\n'.join( (sep.join(
				[str(r[0]),str(r[1]),str(r[2]),round_str(r[3]),round_str(r[4]),str(r[5]),str(r[6])]
			) for r in maxtable(d,n)) )

