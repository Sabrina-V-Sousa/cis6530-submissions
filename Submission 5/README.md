## Safety Notice

### WARNING: This folder contains real malicious payloads collected for academic analysis only.

Do NOT execute these files on a host machine.
All samples must be handled in an isolated malware analysis environment.

The password to decrypt the .7z folder is `infected`

This folder contains the extracted opcodes for the malicious executables and the scripts used to generate them.


## Usage Instructions

Required packages: os, sys, numpy, pandas, matplotlib, itertools, tensorflow, sklearn, seaborn, openpyxl

Input requirements: have opcode files sorted in group subfolders in folder 'ExtractedOpcodes' for training as follows 
    /ExtractedOpcodes/  
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Group 1/  
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sample1.opcode  
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sample2.opcode  
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Group 2/  
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sample3.opcode  
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sample4.opcode  

The 'ExtractedOpcodes' folder should be in the current working directory at the same level as the scripts.

For pre-processing run:
`python3 opcode_preprocessing.py`  

This creates dataset.csv

For creating the deep convolutional neural network and classifying opcodes run:
`python3 deep_learning_classification.py`  

This creates `results` folder for the main deep convolutional neural network model with `metrics.txt`, `metrics.xlsx`, and `confusion_matrix_CNN.png`

It also creates similar files in a subfolder in results of the cross-validation results which tests sub-samples in `results/cross_validation`

## Requirements for Downloading Repository
#### This repository contains large files and requires the use of Git Large File Storage (LFS)  
Download here: https://git-lfs.com/ 

Installation for Linux Machines:  
- execute in the terminal  
  `tar -xvf git-lfs-linux-amd64-v3.7.1.tar.gz`  
- in the created folder *git-lfs-v3.7.1* run  
  `sudo ./install.sh`  
- then  
  `git lfs install`
- Passwords to decrypt the .7z folders are
  `infected`