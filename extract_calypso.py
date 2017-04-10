# Script when given a CSV set of annotations, will pull the relevant columns 
# from a CSV counts file.

import argparse,re

parser = argparse.ArgumentParser(description='Script to generate a subset of 16S counts data given a list of sample IDs in annotation lines.')
parser.add_argument('-annotation', type=str, required=True, help='Name of the annotation file.')
parser.add_argument('-counts', type=str, required=True, help='Name of the counts file.')
parser.add_argument('-output', type=str, required=True, help='Name of the output file.')
args = parser.parse_args()

samples,relevant_positions = ([] for i in range(2))

# Go through the annotation file and grab the relevant IDs.
with open(args.annotation,'r') as annotation:
    for line in annotation:
        if not line.startswith('sample'):
            samples.append(line.split(',')[0])

final_file = "" # should be cheap enough to store this all in memory
last_header = "OTU"

with open(args.output,'w') as out:

    with open(args.counts,'r') as counts:
        for line in counts:

            line = line.strip()

            if len(line.replace(',',"")) == 0:
                continue

            if line.split(',')[1] == 'Header':
                elements = line.split(",")
                if elements[0] != last_header:
                    for x in range(0,len(samples)-1):
                        final_file += ","
                    final_file += "\n"
                    last_header = elements[0]

                final_file += "{0},Header,{1}\n".format(elements[0],(',').join(samples))
            
                if last_header == "OTU":
                    for sample in samples:
                        relevant_positions.append(elements.index(sample))

            else:
                elements = re.search(r'^.*[a-zA-Z]+\s?(.*)',line).group(1).split(',')
                header = re.search(r'^(.*[a-zA-Z]+)\s?',line).group(1)
                curr_str = ""
                for position in relevant_positions:
                    if curr_str == "":
                        curr_str += "{0} ".format(header)                        
                    else:
                        if curr_str[-1].isdigit():
                            curr_str += ",{0}".format(elements[position])
                        else:
                            curr_str += "{0}".format(elements[position])

                curr_str += "\n"
                final_file += curr_str


    out.write(final_file)
