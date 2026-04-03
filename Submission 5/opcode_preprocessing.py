import os
import pandas as pd

'''
CIS 6530 Assignment Submission 4
Preprocessing Script for Machine Learning Script
by Sabrina Sousa and Adam Orchard

Uses opcodes in currentfolder/ExtractedOpcodes/

usage: python3 opcode_preprocessing.py
'''

# setup directories --------------------------------------------------

BASE_DIR = os.path.join(os.getcwd(), "ExtractedOpcodes")

# load data --------------------------------------------------

opcode_data = []
opcode_count = 0

print('Extracting Opcode File Data From:', BASE_DIR)
for apt_group in os.listdir(BASE_DIR):

    apt_path = os.path.join(BASE_DIR, apt_group)
    
    if not os.path.isdir(apt_path):
        continue
    
    if opcode_count == 1:
        # previous apt_group had only 1 entry, copy data for minimum 2 groups per class in train_test_split
        opcode_data.append(opcode_data[len(opcode_data) - 1])

    opcode_count = 0
    for file in os.listdir(apt_path):

        if file.endswith(".opcode"):

            file_path = os.path.join(apt_path, file)
            # extract opcodes
            with open(file_path) as f:
                opcodes = f.read().split()

            # join extracted opcodes as a string
            opcode_string = " ".join(opcodes)
            opcode_data.append({
                "label": apt_group,
                "opcode": opcode_string
            })

            opcode_count = opcode_count + 1

if opcode_count == 1:
    # last apt_group had only 1 entry, copy data for minimum 2 groups per class in train_test_split
    opcode_data.append(opcode_data[len(opcode_data) - 1])

# data extraction --------------------------------------------------

df = pd.DataFrame(opcode_data)

df.to_csv("dataset.csv", index=False)

print("Dataset shape:", df.shape)
print(df["label"].value_counts())

print("\nDone. Dataset created as 'dataset.csv'/")