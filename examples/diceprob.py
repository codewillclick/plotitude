#!/usr/bin/env python

def versus(a,b):
	t = a * b
	n = min(a,b)
	x = max(a,b)
	g = a if a > b else 0
	
	lose = (n**2-n)/2
	win = lose + n*(x-n)
	tie = n
	
	return \
		map(lambda a:float(a)/t, [win,lose,tie]) \
		if a > b else \
		map(lambda a:float(a)/t, [lose,win,tie])
	

if __name__ == '__main__':
	import re
	import sys
	import itertools as it
	
	def to_range(s):
		m = re.match(r'^(\d+)-(\d+)$',s)
		if m:
			return int(m.group(1)), int(m.group(2))
		m = re.match(r'^(\d+)$',s)
		if m:
			return int(m.group(1)), int(m.group(1))
		raise Exception('Does not match "a" or "a-b"')
	
	sep = ','
	buffered = False
	a = to_range(sys.argv[-2])
	b = to_range(sys.argv[-1])
	if '-s' in sys.argv:
		sep = sys.argv[sys.argv.index('-s')+1]
	if '-b' in sys.argv:
		buffered = True
	
	def these(a,b):
		for i in xrange(a[0],a[1]+1):
			for j in xrange(b[0],b[1]+1):
				r = versus(i,j)
				yield (i,j,r[0],r[1],r[2])
	
	def those(a,b):
		yield sep.join(['a','b','win','lose','tie'])
		for r in these(a,b):
			yield sep.join(map(str,r))
	
	if not buffered:
		for s in those(a,b):
			print s
	else:
		buf = []
		for s in those(a,b):
			buf.append(s)
		print '\n'.join(buf)

