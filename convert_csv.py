#!/usr/bin/python
#
# Script to reorganize a CSV file and combine rows based on a shared
# column 8. 
#
# HOW TO RUN: python convert_csv.py original.csv new.csv
#
# Author: James Matsumura

import sys, re

# String value of a dollar to convert to just an int
def get_num(number):
	number = number.replace(',','') # remove commas
	number = number[2:-1]
	return int(number)

# Pass the row being built that needs some empty entries added
def add_blanks(row,num):
	for i in range(num):
		row.append('')
	return row

o = open(sys.argv[1], 'r')
n = open(sys.argv[2], 'w')

curr_pers = "" # track the previous individual
curr_val,original_val,prev_val = (0 for i in range(3)) # track the previous amount for that individual
n_entry = [] # build a new row

for line in o:

	line = line.strip('\n')
	elements = line.split('\t')

	if elements[7] != curr_pers: # New individual build the base of the row

		if curr_pers != "": # Not the first entry
			for i in range(7):
				n_entry.append('')

			n.write("{0}\n".format((",").join(n_entry)))
			n_entry = []
			curr_val,original,prev_val = (0 for i in range(3))

		original_val += get_num(elements[15])
		curr_pers = elements[7]

		n_entry.append(elements[0])
		n_entry = add_blanks(n_entry,2)
		n_entry.append(elements[7])
		n_entry.append(elements[8])
		n_entry.append(elements[9])
		n_entry = add_blanks(n_entry,1)
		n_entry.append(elements[11])
		n_entry.append(elements[13])
		n_entry.append(elements[16])
		n_entry = add_blanks(n_entry,1)
		n_entry.append(str(get_num(elements[15])))
		n_entry = add_blanks(n_entry,3)

	else: # current individual
		if elements[4] == "Payroll - Annual Bonus Accrual":
			n_entry.append(str(get_num(elements[15])))

		else:
			n_entry.append(elements[9])
			n_entry.append(elements[16])
			n_entry = add_blanks(n_entry,1)
			if prev_val == 0:
				curr_val = get_num(elements[15]) - original_val
				prev_val = curr_val
			else:
				curr_val = get_num(elements[15]) - prev_val - original_val
			n_entry.append(str(curr_val))
			n_entry = add_blanks(n_entry,3)

# Have to do one last time for the last entry
n_entry = add_blanks(n_entry,7)

n.write("{0}\n".format((",").join(n_entry)))
n_entry = []

o.close()
n.close()

