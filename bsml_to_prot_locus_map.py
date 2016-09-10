#!/usr/bin/python
#
# The purpose of this script is to map protein ids to cluster sequences
# given the output of a clovr run. The final file produced will be tab-delimited
# with two columns, the first being a locus tag and the second a cluster sequence.
#
# This script accepts two files:
#
# 1) path to a file containing the list of relevant BSML files to obtain
# protein IDs and locus tags
#
# 2) path to a file to essentially overwrite with the first column containing
# protein IDs and the second column containing the protein cluster sequence
#
# HOW TO RUN: bsml_to_prot_locus_map.py bsml.list map.file
#
# Note that the file generated will be found in the directory this script is called
# from and will be called final_map.tsv
#
# Author: James Matsumura

import sys, re, gzip

path_to_bsml_list = str(sys.argv[1]) # specify list_protein_clusters.cgi output to use
path_to_map = str(sys.argv[2]) # specify map file

i = open(path_to_bsml_list, 'r')
m = open(path_to_map, 'r')
o = open('./final_map.tsv', 'w')

map = {}

regex_for_locus = r'identifier="(.*)"\sid='
regex_for_protid = r'id="(.*)"'

locus = ''
protid = ''
found_cds = False
found_locus = False


# iterate over each bsml file within the bsml list
for line in i:

    line = line.replace('\n', '')

    c = gzip.open(line, 'rb')

    for x in c: # iterate over each individual  bsml file
    
        if 'Feature class="CDS"' in line: # locus+polypeptide is near
            found_cds = True	

        elif found_cds == True: # extract locus within CDS region
            if 'NCBILocus' in line:
                locus = re.search(regex_for_locus, line).group(1)
                found_locus = True

        # build map and reset all
        elif 'Feature class="polypeptide"' in line and found_locus == True: 
            protid = re.search(regex_for_protid, line).group(1)
            map[protid] = locus
            locus = ''
            protid = ''
            found_cds = False
            found_locus = False

    c.close()

i.close()

# build the final desired map file
for line in m:

	line = line.replace('\n', '')
	elements = line.split('\t')

	if len(elements) == 2:
		mapped_id = elements[0] # for clarity
        cluster_seq = elements[1]
		mapped_locus = map[mapped_id]
		o.write(mapped_locus + '\t' + cluster_seq  + '\n')

	else:
		o.write(line + '\n')

m.close()
o.close()