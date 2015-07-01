#!/usr/bin/python

import sys
import collections
import itertools
import string
import argparse

def cyclexor(message,key):
    return ''.join(chr(ord(c)^ord(k)) for c,k in itertools.izip(message, itertools.cycle(key)))

def coincidence(text, offset):
	c = 0
	for i in xrange(len(text)):
		if text[i] == text[(i + offset)%len(text)]:
			c += 1
	return c

def chisq(text, freq, allprintable):
	d = collections.Counter(text)
	res = []
	for j in xrange(len(freq)):
		c = 0
		s = [chr(j ^ ord(i)) for i in text]
		for x in s:
			if allprintable:
				p = True
				for i in s:
					if i not in string.printable:
						c = 10^6
						continue
			try:
				c += (d[x] - (freq[ord(x)] * len(text)) ** 2) / (freq[ord(x)] * len(text))
			except:
				continue
		res.append(c)
	return res

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'A simple XOR cracker.')
	parser.add_argument('-v', '--verbose', action = 'store_true', help = 'verbose mode')
	parser.add_argument('-m', '--min-length', type = int, dest = 'minlen', help = 'minimun key length', default = 1)
	parser.add_argument('-M', '--max-length', type = int, dest = 'maxlen', help = 'maximum key length', default = 16)
	parser.add_argument('-i', '--infile', type = str, metavar = 'infile', help = 'input file, stdin otherwise')
	parser.add_argument('-r', '--print-result', action = 'store_true', help = 'show plaintext, void if length only')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-f', '--freqfile', type = str, metavar = 'freqfile', help = 'frequency file, not needed for length only')
	group.add_argument('-l', '--length-only', action = 'store_true', help = 'just find key lenght')
	args = parser.parse_args()

	
	if args.freqfile:
		try:
			freqs = [float(x.strip()) for x in open(args.freqfile,'r').readlines()]
		except:
			sys.stderr.write('Troubles opening frequency file\n')
			sys.exit(1)
			
	if args.infile is not None:
		try:
			crypt = open(args.infile,'r').read()
		except:
			sys.stderr.write('Troubles opening input file\n')
			sys.exit(1)
	else:
		crypt = sys.stdin.read()
		
	cs = [0]*args.minlen
	for i in xrange(args.minlen,args.maxlen):
		cs.append(coincidence(crypt,i))
	winner = max(cs)
	wl = cs.index(winner)

	if args.verbose:
		for i in xrange(args.minlen,len(cs)):
			if cs[i] == winner:
				print '%i\t%i\t%.2f%%	--> Winner!' % (i, cs[i], float(cs[i])/len(crypt)*100)
				continue
			print '%i\t%i\t%.2f%%' % (i, cs[i], float(cs[i])/len(crypt)*100)
	print 'Most probable key length is ' + str(wl)

	if not args.length_only:
		print 'Now trying to guess the key'
		columns = map(list,zip(*[list(crypt[wl*i:wl*i+wl]) for i in xrange(0,len(crypt)/wl)]))
		if len(crypt) % wl: #remainder, distribute it
			rem = crypt[wl*(len(crypt)/wl)]
			for i in xrange(len(rem)):
				columns[i].append(rem[i])

		pwd = ''
		for j in columns:
			r = chisq(j,freqs,1)
			pwd += chr(r.index(min(r)))
		print 'Most probable kay is ' + pwd
		if args.print_result:
			print '\nPlaintext resulting from guessed key:\n\n' + cyclexor(crypt,pwd)



