#!/usr/bin/python
#
# This script is used to refine the output from Sybil's list_protein_clusters.cgi 
# and will map unique polypeptide names to DB accessions.
#
# HOW TO RUN: append_to_map.py /path/to/map_file /path/to/out_file 
#
# Author: James Matsumura

import sys, re

path_to_map = str(sys.argv[1]) # specify map file
path_to_input = str(sys.argv[2]) # specify list_protein_clusters.cgi output to use
path_to_out = str(sys.argv[3]) # specify out file

m = open(path_to_map, 'r')
i = open(path_to_input, 'r')
o = open(path_to_out, 'w')

map = {}

regex_for_id = r"\d+\s+(.*)"

for line in m:
	if line.startswith('uniquename'):
		continue	
	else:
		line = line.replace('\n', '')
		elements = line.split('\t')

		if len(elements) == 2:
			protein = elements[0]
			locus = elements[1]
			map[protein] = locus

m.close()

for line in i:
	line = line.replace('\n', '')
	elements = line.split('\t')

	if len(elements) == 3:
		mapped_id = re.search(regex_for_id, elements[0])
		mapped_locus = map[mapped_id.group(1)]
		print(mapped_locus)
		o.write(line + '\t' + mapped_locus  + '\n')

	else:
		o.write(line + '\n')

i.close()
o.close()
