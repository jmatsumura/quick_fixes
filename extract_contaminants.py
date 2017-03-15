#!/usr/bin/python
#
# Script to parse out the location of contaminants from a file
# with a format like:
#
#------------------
#abcdefghi...
#
#Trim:
#Sequence name, length, span(s), apparent source
#N103P20H1_10_1  34983   1..54,34959..34983      adaptor:NGB00735.1
#N103P20H1_23_1  31351   1..63   adaptor:NGB00735.1
#
# abcdefghi...
#------------------
#
# HOW TO RUN: python extract_contaminants.py contaminant_file output_file
#
# Author: James Matsumura

import sys, re

with open(sys.argv[1],'r') as input:

	contaminant_section = False
	contaminant_list = []

	for line in input:
		if line.startswith('Trim:'):
			contaminant_section = True
			contaminant_list = []

		elif contaminant_section == True and line.startswith('Sequence name'):
			pass

		# If we've found all the contaminants, leave
		elif contaminant_section == True and line.strip() =='':
			genome = contaminant_list[0].split('\t')[0].split('_')[0]
			with open("{0}/{1}".format(sys.argv[2],genome),'w') as out:
				for x in contaminant_list:
					out.write(x)
			contaminant_section = False

		elif contaminant_section == True:
			contaminant_list.append(line)
