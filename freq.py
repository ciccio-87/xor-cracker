#!/usr/bin/python

import sys
allfreqs = [0.]*256
filecount = 0
for line in sys.stdin:
	try:
		content = open(line.strip(),'r').read()
	except:
		sys.stderr.write('failed to open ' + line)
		continue
	filecount += 1
	freqs = [0.]*256
	total = 0
	for c in content:
		total += 1
		freqs[ord(c)] += 1

	for i in xrange(255):
		try:
			allfreqs[i] = (allfreqs[i] + (freqs[i] / total))/2
		except:
			pass

sys.stderr.write(str(filecount) + ' file scanned')

for i in xrange(255):
	#print chr(i) + '\t' + str(allfreqs[i])
	print '%.64f' % allfreqs[i]



