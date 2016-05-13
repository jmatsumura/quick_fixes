#!/usr/bin/python

# The purpose of this script is to isolate the UniProt IDs in the custom UniRef file.
#
# HOWTO: (python) build_custom_uniref100.py path_to_custom_uniref_file
#
# Author: James Matsumura

import sys, os, re, gzip

mapFile =  str(sys.argv[1]) # let the user specify the uniref file

mappingFile = gzip.open(mapFile, 'rb') 
outFile = open('./found_uniprot_accs_in_uniref100.txt', 'w')

for line in mappingFile:
    elements = line.split('\t')
    print elements[0] + " " + elements[7]
