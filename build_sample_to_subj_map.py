#!/usr/bin/python
#
# Script to take in a mapping file and add a row to an R dataframe in TSV format. 
#
# HOW TO RUN: /path/to/map_file /path/to/counts
#
# Author: James Matsumura

import sys, re

m = open(sys.argv[1], 'r')
n = open(sys.argv[2], 'r')
o = open('./mapped_matrix.counts', 'w')

mp = {}
f = []

for line in m:
	line = line.strip('\n')
	elements = line.split('\t')
	mp[elements[0]] = elements[1]

x = 0
y = 0
for line in n:
	if x == 0:
		e = line.split('\t')
		for z in e:
			if z in mp and not z == "":
				f.append(mp[z])
				y += 1
			else:
				f.append("NA")
		o.write(line)
	else:
		o.write(line)
	x += 1

print y
print len(f)
o.write(("\t").join(f))

m.close()
n.close()
o.close()
