# When given a TSV set of metadata from QIITA, converts it into Calypso's V6 
# format.

import argparse

parser = argparse.ArgumentParser(description='Script to generate a V6 formatted file for Calypso given a QIITA TSV sample metadata file.')
parser.add_argument('-annotation', type=str, required=True, help='Name of the annotation file.')
parser.add_argument('-output', type=str, required=True, help='Name of the output file.')
args = parser.parse_args()

metadata = ""
entries = [] # build a list to make output with

with open(args.annotation,'r') as metafile:
    for line in metafile:
        if metadata == "": # first line
            metadata = line.strip().split('\t')

        else:
            curr_data = line.strip().split('\t')
            req_fields = [curr_data[0],curr_data[0],curr_data[0],'1']
            entries.append(req_fields+curr_data)

with open(args.output,'w') as outfile:
    outfile.write("sample ID\tlabel\tIndvidual\tinclude\t{0}\n".format(('\t').join(metadata)))

    for x in range(0,len(entries)):
        entries[x][0] = "S{0}".format(x)
        outfile.write("{0}\n".format(('\t').join(entries[x])))
