
# Script to parse through metagenomic sample OTU relative counts and output a
# OTU table with absolute counts. 

import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description='Script to convert a metadata file split across multiple tabs in XLS format into a single TSV file.')
parser.add_argument('-input_otu', type=str, required=True, help='Location of an OTU counts file.')
parser.add_argument('-outfile', type=str, required=True, help='Name of the output CSV file.')
args = parser.parse_args()

def convert_rel_to_abs(rel_count_list):

    for idx in range(0,len(rel_count_list)):

        count = rel_count_list[idx]

        if 'e-' in count:
            count = "{:.8f}".format(float(count))

        rel_count_list[idx] = str(int(float(count) * 1000000))

    return rel_count_list

def build_otu_entry(otu_row,rank_int,rank_name,rank_prefix):
    
    rank = otu_row[0].split('|')[rank_int].replace(rank_prefix,'')
    converted_counts = convert_rel_to_abs(otu_row[1:])
    return [rank_name,rank] + converted_counts

def write_rank_out(output_file,header_list,rank,rank_list):
    with open(output_file,'a') as out:
        header_list[0] = rank
        out.write("{0}\n".format(('\t').join(header_list)))

        for entry in rank_list:
            out.write("{0}\n".format(('\t').join(entry)))

header,phylum,clas,order = ([] for i in range(4))

with open(args.input_otu,'r') as otu:

    for line in otu:

        elements = line.strip().split('\t')

        if elements[0] == 'sample':
            header = elements
            header.insert(1,'Header')

        elif '__' in elements[0]:

            if elements[0].count('|') == 1:
                phylum.append(build_otu_entry(elements,1,"Phylum","p__"))

            elif elements[0].count('|') == 2:
                clas.append(build_otu_entry(elements,2,"Class","c__"))

            elif elements[0].count('|') == 3:
                order.append(build_otu_entry(elements,3,"Order","o__"))


# Careful because this file APPENDS, so if you're trying to run this script 
# multiple times you need to reset it after each attempt in order to avoid data 
# duplication.
write_rank_out(args.outfile,header,"Phylum",phylum)
write_rank_out(args.outfile,header,"Class",clas)
write_rank_out(args.outfile,header,"Order",order)

