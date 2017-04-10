
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
took_antibioitics = set()

with open(args.input_otu,'r') as otu:
    possible_ids = otu.readline().strip().split('\t')

possible_ids.pop(0)

# Build a set of lists corresponding to all samples from a given individual
samples = defaultdict(list)
for id in possible_ids:
    sample = id.split('_')[0]
    samples[sample].append(id)

# Build a list of indices to get the last date from each sample
end_samples = defaultdict(list)
for k,v in samples.items():
    dates = []
    for sample in v:
        dates.append(float(sample.split('_')[1]))

    end_samples[k].append("{0}_{1}".format(k,min(dates)))
    end_samples[k].append("{0}_{1}".format(k,max(dates)))


current_sheet = wb.sheet_by_name("Antibiotics")
total_metadata_cols += 1 # add another for antibioitics column

for row_idx in range(0,current_sheet.nrows):
    took_antibioitics.add(current_sheet.cell_value(row_idx,0))

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

            columns.append("Took Antibiotic")

        else:
            for col_idx in range(1,current_sheet.ncols):
                data[current_sheet.cell_value(row_idx,0)].append(current_sheet.cell_value(row_idx,col_idx))

with open(args.outfile,'w') as output:

    keep_us = set()
    output.write("{0}\n".format((',').join(columns)))
    paired_id = 0

    for key in data:

        if key in took_antibioitics:
            data[key].append("Yes")
        else:
            data[key].append("No")

        if len(data[key]) == total_metadata_cols:
            
            paired_id += 1

            for val in possible_ids:
                if val.startswith(key):

                    keep_or_not = 0

                    keep_us.add(val)

                    if val in end_samples[key]:
                        keep_or_not = 1

                    pair_value = "P{0}".format(paired_id)
                    mandatory_data = [val,val,pair_value,keep_or_not]
                    total_metadata = mandatory_data + data[key]
                    converted_metadata = [str(i) for i in total_metadata]
                    output.write((',').join(converted_metadata))
                    output.write("\n")


    for id in possible_ids:
        if id not in keep_us:
            mandatory_data = [id,id,id,"0"]
            mandatory_data += ["NA"] * (len(columns)-4)
            output.write((',').join(mandatory_data))
            output.write('\n')

