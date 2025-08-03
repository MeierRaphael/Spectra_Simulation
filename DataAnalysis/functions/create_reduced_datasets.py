import csv
import ast
from collections import defaultdict

def x_from_each_index_length(input_file, output_file, numb_rows, numb_spins):
    # Dictionary to collect up to x rows for each Index length
    samples = defaultdict(list)

    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        for row in reader:
            try:
                index_list = ast.literal_eval(row['Index'])
                if isinstance(index_list, list):
                    length = len(index_list)
                    if 1 <= length <= numb_spins and len(samples[length]) < numb_rows:
                        samples[length].append(row)
            except (ValueError, SyntaxError):
                continue  # Skip rows with invalid Index format

    # Write collected rows to new CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for length in range(1, numb_spins+1):
            for row in samples[length]:
                writer.writerow(row)



import csv
import ast

def all_with_few_spins(input_file, output_file, numb_spins):

    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            try:
                if 'n_spins' in row and row['n_spins'].isdigit():
                    current_n_spins = int(row['n_spins'])
                else:
                    index_list = ast.literal_eval(row['Index'])
                    if not isinstance(index_list, list):
                        continue  # Skip if 'Index' isn't a list
                    current_n_spins = len(index_list)

                if current_n_spins == numb_spins:
                    writer.writerow(row)

            except (ValueError, SyntaxError):
                continue  # Skip rows with invalid 'Index' (like 10a, 10b)


