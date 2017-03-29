

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
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from scipy import stats, integrate
import matplotlib.pyplot as plt
import seaborn as sns

parser = argparse.ArgumentParser(description='Script to generate a scatter plot comparing global alignment based ID and reference based ID.')
parser.add_argument('-input', type=str, required=True, help='Location of second_ids_v_coverage.tsv.')
parser.add_argument('-month', type=str, required=True, help='Month [01,02,...12].')
parser.add_argument('-output', type=str, required=True, help='Name of the outputfile.')
args = parser.parse_args()

acc = []

# Just extract the coverage ratio
with open(args.input,'r') as infile:
    for line in infile:

        if line.startswith("#"):
            continue
        line = line.rstrip()
        ele = line.split(':')

        starttime = int(ele[9])
        endtime = int(ele[10])
        if starttime == 0 or endtime == 0:
            continue
 
        month = str(datetime.fromtimestamp(endtime)).split(' ')[0].split('-')[1]

        # If the right month, include the accuracy
        if month != args.month:
            continue
            
        # If failed, skip
        if int(ele[11]) == 1:
            continue

        # If no mem_free, leave
        if 'mem_free' not in line:
            continue

        maxvmem = int(ele[-3].split('.')[0])
        mem_req = re.search(r'mem_free=([a-zA-Z0-9]+)',line).group(1)
        g_or_m = mem_req[-1]

        if not mem_req[-1].isdigit():
            mem = int(mem_req[:-1])

            if g_or_m.upper() == "G":
                mem = mem*1000000000
            elif g_or_m.upper() == "M":
                mem = mem*1000000
        
        acc.append(("{0:.2f}").format(maxvmem/mem*100))


df = pd.DataFrame(acc,columns=['Accuracy'])
splot = sns.boxplot(df[['Accuracy']],showfliers=False)
splot.set(ylim=(-5,600))

fig = splot.get_figure()
fig.savefig(args.output)