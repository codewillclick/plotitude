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
	for v in xrange(1,d+1):
		p = maxprob(d,n,v)
		c = maxchance(d,n,v)
		yield d,n,v,p,c,x


# Just a little color...
# python dicemax.py | awk -F, '$2==2{printf "\033[93m"} $2==3{printf "\033[91m"} $2<=3{print} {printf "\033[0m"}' | column -s, -t | less -R

if __name__ == '__main__':
	
	def round_str(v,d=3):
		p = pow(10,3)
		check = 1./p
		if v < check:
			return '0.'+'0'*d
		return str(int(v*p)/float(p))
	
	sep = ','
	print sep.join(['d','n','v','mxprob','mxchance','halfsplit'])
	for d in (4,6,8,12,20):
		for n in xrange(1,d+1):
			print '\n'.join( (sep.join(
				[str(r[0]),str(r[1]),str(r[2]),round_str(r[3]),round_str(r[4]),str(r[5])]
			) for r in maxtable(d,n)) )

