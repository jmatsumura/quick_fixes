#!/usr/bin/python
# Script to build indices to help Justin's Neo4j converter work.
# Still needs to add new nodes in addition to adding logic to the
# conversion script as well. 

import sys, re

i = open(sys.argv[1], 'r') # couchdb dump json is the input
project = open('./projectList.txt', 'w')
study = open('./studyList.txt', 'w')
subject = open('./subjectList.txt', 'w')
visit = open('./visitList.txt', 'w')
sample = open('./sampleList.txt', 'w')
dnaprep16s = open('./16SDNAprepList.txt', 'w')
rawseqset16s = open('./16SrawseqsetList.txt', 'w')
trimmedseqset16s = open('./16StrimmedseqsetList.txt', 'w')

k = -1 # offset since first line of dump can be skipped
for doc in i: # iterate over couchdb dump and extract indices
	if '"node_type":"project"' in doc:
		project.write(str(k)+'\n')
	elif '"node_type":"study"' in doc:
		study.write(str(k)+'\n')
	elif '"node_type":"subject"' in doc:
		subject.write(str(k)+'\n')
	elif '"node_type":"visit"' in doc:
		visit.write(str(k)+'\n')
	elif '"node_type":"sample"' in doc:
		sample.write(str(k)+'\n')
	elif '"node_type":"16s_dna_prep"' in doc:
		dnaprep16s.write(str(k)+'\n')
	elif '"node_type":"16s_raw_seq_set"' in doc:
		rawseqset16s.write(str(k)+'\n')
	elif '"node_type":"16s_trimmed_seq_set"' in doc:
		trimmedseqset16s.write(str(k)+'\n')

	k += 1
