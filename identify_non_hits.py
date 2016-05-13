#!/usr/bin/python

# The purpose of this script is to isolate the UniProt IDs in the custom UniRef file.
#
# HOWTO: (python) build_custom_uniref100.py path_to_custom_uniref_file
#
# Author: James Matsumura

import sys, os, re, gzip

unirefFile =  str(sys.argv[1]) # let the user specify the uniref file

customUnirefFile = gzip.open(unirefFile, 'rb') 
outFile = open('./found_uniprot_accs_in_uniref100.txt', 'w')
regexForUnirefAccession = r"^>UniRef100\_(\w+)\s+.*"

for line in customUnirefFile:

	if(line.startswith('>')):
		# Some odd formatting in the UniRef file? need to 
		# actually check to make sure it's in proper format
		findEntry = re.search(regexForUnirefAccession, line)
		if(findEntry):
			foundEntry = findEntry.group(1)
			outFile.write(foundEntry+'\n')	
