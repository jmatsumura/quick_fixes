#!/usr/bin/python
#
# Script to extract a files size given an endpoint and using pycurl.
#
# HOW TO RUN: get_file_size.py /path/to/csv /path/to/output
#
# Author: James Matsumura

import sys, re, pycurl

i = open(sys.argv[1], 'r')
o = open(sys.argv[2], 'w')
c = pycurl.Curl()

for line in i:
	line = line.strip('\n')
	elements = line.split(',')
	if elements[0] != "n.id":
		c.setopt(c.URL, elements[1])
		c.setopt(c.NOBODY, 1) # just pull the header
		c.perform()
		size = c.getinfo(c.CONTENT_LENGTH_DOWNLOAD) # extract size in bytes
		final_line = "%s,%s\n" % (line,size)
		o.write(final_line)
	else:
		o.write(line+'\n') 

i.close()
o.close()
