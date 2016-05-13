#!/usr/bin/python

# The purpose of this script is to isolate a particular subset of 
# UniProt (SwissProt) entries that meet various criteria. The main
# criteria targets are GO terms/evidence and organism type. Once 
# these are identified then stats need to be collected for number
# of GO terms linked to a particular accession. Since all this 
# data will be iterated over at once, perform data extraction and 
# count calculation in one fell swoop
#
# HOWTO:
# ./calc_uniprot_stats.py path_to_sprot_file 
#
# Author: James Matsumura

import sys, os, re, gzip

sprotFile =  str(sys.argv[1]) 
# organismName =  str(sys.argv[2]) hardcode for now since there can be problems
# with regex when passing certain characters common to organism names

bacteriaOnlyFile = gzip.open(sprotFile, 'rb') # large files, use compression
statFile = open('./uniprot_withev_stats.txt', 'w')

# Only want to find those with experimental evidence backing the annotation.
# Use: http://geneontology.org/page/guide-go-evidence-codes
evidenceCodes = ('EXP','IDA','IPI', 'IMP', 'IGI', 'IEP')
# The annotations here are formatted in such a way that GO terms will be found
# following the DR (database cross-reference) tag. Thus, only need to look 
# through the following tag lines: AC, OS (organism), DR, footer.
relevantTags  = ('OS', 'DR')

footerFound = False
accessionFound = False
organismFound = False

regexForAccession = r"^AC\s+(.*);"
regexForOS = r"^OS\s+Escherichia coli \(strain K12\)"
regexForGO = r"^DR\s+GO;.*" 
regexForGOev = r"^DR.*;.*;.*;\s(.*):" 
regexForFooter = r"^\/\/"
uniqueIds = set()
count = 0

for line in bacteriaOnlyFile:

	if (footerFound == True): # reinitialize values for next record
		accessionFound = False
		footerFound = False
		organismFound = False
		count = 0

	elif(accessionFound == True):
		if(re.search(regexForFooter, line)):
			footerFound = True

		elif(organismFound == True and re.search(regexForGO, line)):

			count += 1
			ev = re.search(regexForGOev, line)
			evVal = ev.group(1)
			if(evVal in evidenceCodes):

				# It appears that each accession tag can have
				# multiple accessions tied to it. These all go
				# to the same representative in the UniProt site,
				# but, going to include them all. 
				if(';' in foundAccession):
					multiAccessions = foundAccession.split('; ')
					for x in multiAccessions: # iterate over this ~2-3 len list
						if x not in uniqueIds:
							uniqueIds = uniqueIds | {x}
							statFile.write(x+'\t'+str(count)+'\n')

				elif(foundAccession not in uniqueIds): 
					uniqueIds = uniqueIds | {foundAccession}
					statFile.write(foundAccession+'\t'+str(count)+'\n')

		elif(re.search(regexForOS, line)):
			organismFound = True

		else:
			next

	else:
		findAccession = re.search(regexForAccession, line)
		if(findAccession):
			foundAccession = findAccession.group(1)
			accessionFound = True
