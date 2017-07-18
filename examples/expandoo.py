#!/usr/bin/env python

import math
import logging as L

def dist(t,r,enum,args):
	kx,ky = args[0:2]
	a = int(r[enum[kx]])
	b = int(r[enum[ky]])
	key = '_'.join(['dist',kx,ky])
	t[key] = math.sqrt(a*a + b*b)
	return ((key,t[key]),)

def flat(t,r,enum,args):
	kv = args[0]
	key = 'flat_' + kv
	t[key] = int(float(r[enum[kv]]))
	return ((key,t[key]),)


if __name__ == '__main__':
	import sys
	
	print "Shouldn't be running this as __main__, yo!"
	
