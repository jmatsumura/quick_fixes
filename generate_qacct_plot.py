

# This script is supplementary to the pipeline and allows one to generate
# a scatterplot that compares the percent identity obtained by global alignment
# versus the percent ID of the reference bases correctly accounted for. This
# takes the output from second_threaded_assess_alignment.py.
#
# Run the script using a command like this:
# python generate_repeat_plot.py -i aa_out.tsv
#
# Author: James Matsumura

import argparse,re
from collections import OrderedDict,defaultdict
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from scipy import stats, integrate
import matplotlib.pyplot as plt
import seaborn as sns

parser = argparse.ArgumentParser(description='Script to generate a scatter plot comparing global alignment based ID and reference based ID.')
parser.add_argument('-input', type=str, required=True, help='Location of Location of second_ids_v_coverage.tsv.')
parser.add_argument('-outfile', type=str, required=True, help='Name of the outputfile.')
parser.add_argument('-outgraph', type=str, required=True, help='Name of the output graph.')
args = parser.parse_args()

ppl,days = (defaultdict(list) for i in range(2))

# Just extract the coverage ratio
with open(args.input,'r') as infile:
    for line in infile:

        if line.startswith("#"):
            continue

        line = line.rstrip()
        ele = line.split(':')

        starttime = int(ele[9])
        endtime = int(ele[10])

        # Skip entries that don't have the correct characteristics like...
        month_day = str(datetime.fromtimestamp(endtime)).split(' ')[0].split('-',1)[1]

        if starttime == 0 or endtime == 0: # start or end times of 0
            continue
            
        if int(ele[11]) == 1: # it failed
            continue

        if 'mem_free' not in line: # no mem_free specified
            continue

        person = ele[3]

        maxvmem = int(ele[-3].split('.')[0])
        mem_req = re.search(r'mem_free=([a-zA-Z0-9]+)',line).group(1)
        g_or_m = mem_req[-1]

        if mem_req == 0 or maxvmem == 0:
            continue

        if not mem_req[-1].isdigit():
            mem = int(mem_req[:-1])

            if g_or_m.upper() == "G":
                mem = mem*1000000000
            elif g_or_m.upper() == "M":
                mem = mem*1000000
        
        days[month_day].append("{0}:{1}".format(mem,maxvmem))

        ppl[person].append(mem)
        ppl[person].append(maxvmem)

sorted_ppl = OrderedDict(sorted(ppl.items()))

with open(args.outfile,'w') as out:
    for person,vals in sorted_ppl.items():

        blocked = [] # track how much mem is requested vs used

        for m in range(0,len(vals),2):
            blocked.append(int(vals[m])-int(vals[m+1]))
            
        stdev = np.std(blocked)
        stdev = (stdev/1000000000) # change to GB
        out.write("{0}\t{1:.5f}\t{2:.5f}\n".format(person,sum(blocked)/len(blocked)/1000000000,stdev))

tot_mem,tot_vmem,avg_mem,avg_vmem = ([] for i in range(4))
for day in days:
    for vals in days[day]:
        tot_mem.append(int(vals.split(':')[0]))
        tot_vmem.append(int(vals.split(':')[1]))

    avg_mem.append(sum(tot_mem)/len(tot_mem))
    avg_vmem.append(sum(tot_vmem)/len(tot_vmem))
