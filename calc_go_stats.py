# /usr/bin/python

# The purpose of this script is to isolate all GO annotations that have
# experimental evidence associated with them. Simply pass the path to a
# GO annotation file and this script will produce an output file with
# three columns: 1) UniProt accession 2) GO term 3) evidence code
#
# The script will then go on to process this file and perform a count
# of sorts for how many GO terms are linked per accession. While this is
# naive, it's intended to be. Both this file and the other generated here
# will be used for basic comparisons of how well UniProt catches GO
# annotations.
#
# The GO annotation file is formatted in such a way that it contains
# tab-delimited rows with the UniProt accession, GO term, and 
# evidence codes in the second, fifth, and seventh columns.
#
# HOWTO: (python) calc_go_stats.py path_to_go_annot 
#
# Author: James Matsumura

import sys, os, re
from collections import Counter, defaultdict

goAnnotFile =  str(sys.argv[1]) 

inFile = open(goAnnotFile, 'r') 
outFile = open('./relevant_go_annots.txt', 'w')
outStatFile = open('./go_stats.txt', 'w')

# build a list in first phase and count these values after it is done
accs_list = []

# Only want to find those with experimental evidence backing the annotation.
# Use: http://geneontology.org/page/guide-go-evidence-codes
evidenceCodes = ('EXP','IDA','IPI', 'IMP', 'IGI', 'IEP') 

for line in inFile:

	if(line.startswith('!')):
		next
	else:
		elements = line.split('\t')
		if(elements[6] in evidenceCodes):
			outFile.write(elements[1]+'\t'+elements[4]+'\t'+elements[6]+'\n')
			accs_list.append(elements[1])

accs = [{"acc": key, "cnt": value} for key, value in Counter(accs_list).items()]

for x in accs:
	s = x['cnt']
	outStatFile.write(x['acc'] + '\t' + str(s) + '\n')
