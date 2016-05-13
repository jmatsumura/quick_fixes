#!/usr/bin/python
#
# The purpose of this script is to count how many unique IDs are mapped
# to a single cluster and how common this occurence is. This needs to be 
# known before a map file is found for tying back a hit to a particular 
# reference annotation. 
#
# HOWTO: (python) calc_uniref_cluster_stats.py path_to_ids_mapfile 
#
# Author: James Matsumura

import sys, os, re, gzip
from collections import Counter, defaultdict

mapFile =  str(sys.argv[1]) 

inFile = gzip.open(mapFile, 'r') 
outStatFile = open('./uniref_cluster_stats.txt', 'w')

# build a list in first phase and count these values after it is done
accs_list = []

# Only want to find those with experimental evidence backing the annotation.
# Use: http://geneontology.org/page/guide-go-evidence-codes

for line in inFile:

	elements = line.split('\t')
	accs_list.append(elements[7])

accs = [{"acc": key, "cnt": value} for key, value in Counter(accs_list).items()]

for x in accs:
	s = x['cnt']
	outStatFile.write(x['acc'] + '\t' + str(s) + '\n')
