#!/usr/bin/python

# The purpose of this script is to refine to unique sequences given a 
# FASTA/UniRef dataset.
#
# HOWTO: (python) build_unique_uniref100.py path_to_uniref
#
# Author: James Matsumura

import sys, os

unirefFile =  str(sys.argv[1]) 
origUnirefFile = open(unirefFile, 'r') 
outFile = open('./unique_uniref100.fasta', 'w')
relevantUnirefEntry = False 
uniqueIds = set()

for line in origUnirefFile:

	if(line.startswith('>')):
		if(line in uniqueIds):
			relevantUnirefEntry = False
			next
		else:
			uniqueIds = uniqueIds | {line}
			outFile.write(line)
			relevantUnirefEntry = True

	elif(relevantUnirefEntry):
		outFile.write(line)
