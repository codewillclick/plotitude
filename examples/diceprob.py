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

def maxprob(d,n,v):
	return pow(v,n)/float(pow(d,n))
def maxchance(d,n,v):
	v = float(v)
	return (v/d)**n - ((v-1)/d)**n
	#return maxprob(d,n,v)-maxprob(d,n,v-1)

if __name__ == '__main__':
	import re
	import sys
	import itertools as it
	
	def to_iterer(s):
		m = re.match(r'^(\d+)-(\d+)$',s)
		if m:
			def f():
				return xrange(int(m.group(1)), int(m.group(2)))
			return f
		m = re.match(r'^(\d+)$',s)
		if m:
			def f():
				return xrange(int(m.group(1)), int(m.group(1)))
			return f
		m = re.match(r'^((\d+,)+?\d+)$',s)
		if m:
			r = m.group(1).split(',')
			def f():
				return (int(s) for s in r)
			return f
		raise Exception('Does not match "a" or "a-b"')
	
	sep = ','
	buffered = False
	percent = False
	if '-s' in sys.argv:
		sep = sys.argv[sys.argv.index('-s')+1]
	if '-b' in sys.argv:
		buffered = True
	if '-p' in sys.argv:
		percent = True
	a = to_iterer(sys.argv[-2])
	b = to_iterer(sys.argv[-1])
	
	def these(a,b):
		# a,b return iterables.
		for i in a():
			for j in b():
				r = versus(i,j)
				yield (i,j,r[0],r[1],r[2])
	
	def thoseA(a,b):
		yield sep.join(['a','b','win','lose','tie'])
		for r in these(a,b):
			yield sep.join(map(str,r))
	
	def thoseB(a,b):
		yield sep.join(['a','b','win','lose','tie'])
		for a,b,win,lose,tie in these(a,b):
			yield sep.join((
				str(a),
				str(b),
				str(int(win*100))+'%',
				str(int(lose*100))+'%',
				str(int(tie*100))+'%'
			))
	
	those = thoseB if percent else thoseA
	
	if not buffered:
		for s in those(a,b):
			print s
	else:
		buf = []
		for s in those(a,b):
			buf.append(s)
		print '\n'.join(buf)

