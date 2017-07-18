#!/usr/bin/env python

import sys
import time
import random

mn,mx,count = map(int,sys.argv[1:4])
seed = sys.argv[4] if len(sys.argv) > 4 else time.time()

random.seed(seed)

print 'x,y'
for i in xrange(count):
	print ','.join(map(str,[random.randint(mn,mx),random.randint(mn,mx)]))

