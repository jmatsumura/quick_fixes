
# Script to parse through metagenomic sample XLS files and condense them into
# a single V6 CSV file compatible with Calypso. 

import argparse, xlrd
from collections import defaultdict

parser = argparse.ArgumentParser(description='Script to convert a metadata file split across multiple tabs in XLS format into a single TSV file.')
parser.add_argument('-input_xls', type=str, required=True, help='Location of an XLS metadata file.')
parser.add_argument('-input_otu', type=str, required=True, help='Location of an OTU counts file.')
parser.add_argument('-outfile', type=str, required=True, help='Name of the output CSV file.')
args = parser.parse_args()

wb = xlrd.open_workbook(filename=args.input_xls)
sheets = wb.sheet_names()

data = defaultdict(list)
columns = ['sample id','label','individual','include']
total_metadata_cols = 0

possible_ids = []

with open(args.input_otu,'r') as otu:
    possible_ids = otu.readline().strip().split('\t')

possible_ids.pop(0)

for sheet in sheets:

    if sheet == "Antibiotics":
        continue

    current_sheet = wb.sheet_by_name(sheet)

    total_metadata_cols += current_sheet.ncols - 1

    for row_idx in range(0,current_sheet.nrows):
        # Extract column labels
        if row_idx == 0:
            for col_idx in range(1,current_sheet.ncols):
                columns.append(current_sheet.cell_value(row_idx,col_idx))


        else:
            for col_idx in range(1,current_sheet.ncols):
                data[current_sheet.cell_value(row_idx,0)].append(current_sheet.cell_value(row_idx,col_idx))


with open(args.outfile,'w') as output:

    output.write("{0}\n".format((',').join(columns)))

    paired_id = 0

    for key in data:

        if len(data[key]) == total_metadata_cols:
            
            paired_id += 1
            possible = False

            for val in possible_ids:
                if val.startswith(key):

                    pair_value = "P{0}".format(paired_id)
                    mandatory_data = [val,val,pair_value,"1"]
                    total_metadata = mandatory_data + data[key]
                    converted_metadata = [str(i) for i in total_metadata]
                    output.write((',').join(converted_metadata))
                    output.write("\n")
                    possible = True

            if possible == False:
                unique = "{0}{1}".format(key,paired_id)
                mandatory_data = [unique,unique,"NA","0"]
                mandatory_data += ["NA"] * (len(data[key]))
                output.write(','.join(mandatory_data))
                output.write("\n")
