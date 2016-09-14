#!/usr/bin/python
#
# The purpose of this script is to map protein ids to cluster sequences
# given the output of a CloVR run. The final file produced will mirror the output of
# muscle except it will be a single file with all polypeptide IDs replaced with Locus IDs.
#
# This script accepts three inputs when calling it:
#
# 1) path to a file containing the list of relevant BSML files to obtain
# protein IDs and locus tags
#
# 2) path to a file to essentially overwrite with the first column containing
# protein IDs and the second column containing the protein cluster sequence
#
# 3) path to the output file
#
# HOW TO RUN: bsml_to_prot_locus_map.py bsml.list map.file path_to_outfile.txt
#
# Author: James Matsumura

import sys, re, gzip

path_to_bsml_list = str(sys.argv[1]) # specify list_protein_clusters.cgi output to use
path_to_map_list = str(sys.argv[2]) # specify map file (usually under muscle/*_j_ortholog_clusters/~)
path_to_outfile = str(sys.argv[3]) # specify where the output is to go

i = open(path_to_bsml_list, 'r')
m = open(path_to_map_list, 'r')
o = open(path_to_outfile, 'w')

pl_map = {}
lg_map = {}

regex_for_locus = r'identifier="(.*)"\sid='
regex_for_protid = r'id="(.*)"'
regex_for_name = r'Name:\s(.*)\s+Len'
regex_for_final_map = r'(\w+\.\w+\.\d+\.\d)\s+(.*)'
regex_for_gpn = r'content="(.*)"'

locus = ''
protid = ''
gpn = ''
found_cds = False
found_locus = False


# iterate over each bsml file within the bsml list
for line in i:

	line = line.replace('\n', '')
	c = gzip.open(line, 'rb')

	for x in c: # iterate over each individual  bsml file
    
		if 'Feature class="CDS"' in x: # locus+polypeptide is near
			found_cds = True

		elif found_cds == True and found_locus == False: # extract locus within CDS region
			if 'gene_product_name' in x:
				gpn = re.search(regex_for_gpn, x).group(1)
			elif 'NCBILocus' in x:
				locus = re.search(regex_for_locus, x).group(1)
				lg_map[locus] = gpn
				found_locus = True

		# build map and reset all
		elif 'Feature class="polypeptide"' in x and found_locus == True: 
			protid = re.search(regex_for_protid, x).group(1)
			pl_map[protid] = locus
			locus = ''
			protid = ''
			gpn = ''
			found_cds = False
			found_locus = False

	c.close()

i.close()

cnt = 1

# build the final desired map file
for line in m:

	line = line.replace('\n', '')
	c = gzip.open(line, 'rb')
	locus_array = []

	for x in c:
		x = x.replace('\n', '')

		if re.match(regex_for_final_map, x): # replace body protids with locus IDs
			mapid = re.search(regex_for_final_map, x).group(1) # for clarity
			if mapid in pl_map:
				o.write(x.replace(mapid, pl_map[mapid]) + '\n')
			else:
				o.write(x + '\n')

		elif 'Name:' in x: # replace header section protids with locus IDs
			mapid = re.search(regex_for_name, x).group(1)
			mapid = mapid.replace(" ", "") # regex shoulud have caught this, no?
			if mapid in pl_map:
				newLine = x.replace(mapid, pl_map[mapid])
				locus_array.append(pl_map[mapid])
				o.write(newLine + '\n')
			else:
				o.write(x + '\n')
				print('Protein ID: ' + mapid + ' not found in BSML.')

		elif x.startswith('//'): # print a line to grep for cluster members
			o.write('cluster_' + str(cnt) + ' ' + '\t'.join(str(j) for j in locus_array))

			for x in locus_array:
				o.write(x + '\t' + lg_map[x] + '\n')

			o.write('\n\n//\n')
			cnt += 1

		else: # maintain format of original file
			o.write(x + '\n')

m.close()
o.close()
