#!/usr/bin/python
#
# Script to compare Neo4j outputs and remove those with duplicate values
#
# HOW TO RUN: /path/to/true_nodes /path/to/false_nodes
#
# Author: James Matsumura

import sys, re

t = open(sys.argv[1], 'r')
f = open(sys.argv[2], 'r')
o = open('./ids_to_remove.txt', 'w')

unique_checksums = set()
true_id = set()

for line in t:
	line = line.strip('\n')
	elements = line.split(',')
	unique_checksums = unique_checksums | {elements[1]}
	true_id = true_id | {elements[0]}

for line in f:
	line = line.strip('\n')
	elements = line.split(',')
	if elements[1] in unique_checksums and elements[0] not in true_id:
		o.write(elements[0]+"\n")

t.close()
f.close()
o.close()
