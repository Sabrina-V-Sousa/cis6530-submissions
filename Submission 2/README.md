## Safety Notice

### WARNING: This folder contains real malicious payloads collected for academic analysis only.

Do NOT execute these files on a host machine.
All samples must be handled in an isolated malware analysis environment (e.g., virtual machine with no network or controlled simulation network).

## Safe Handling Expectations 
- Do not double-click or run samples.
- Store samples only in compressed form.
- Use password-protected archives if extracting (recommended and current password: *infected*).
- Use snapshots before analysis.
- Do not upload samples to public file-sharing sites.
- Samples are intended for static analysis (strings, hashing, disassembly) and controlled sandbox execution (Hybrid Analysis / Any.Run / local VM)

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

## Collection Methodology 
Samples were obtained from public malware repositories and sandbox platforms, including:
- MalwareBazaar
- Hybrid Analysis
- VirusTotal (hash-based reference only)
- Vendor threat reports (ESET, Kaspersky, Mandiant, CrowdStrike)

Only samples referenced in publicly documented APT activity sites were included.

Samples were excluded if:
- Attribution to an APT group was ambiguous
- Source did not provide verifiable indicators
- File was not retrievable from a trusted, ethical and opensource repository
- Sample was redundant with an existing payload

The following groups in group set 4 had either no open source malware samples or only had redundant malware samples that were already downloaded for another group:
- G0122 Silent Librarian
- G0024 Putter Panda
- G0106 Rocke
- G0128 ZIRCONIUM
- G0017 DragonOK
- G0031 Dust Storm
- G0079 DarkHydrus
- G0072 Honeybee
- G0071 Orangeworm

Process:
1. Identified APT groups from public threat intelligence sources.
2. Extracted file hashes and indicators from vendor reports.
3. Located corresponding samples in public malware repositories.
4. Verified linkage using:
   - Hash matching
   - Behavioral similarity (C2 patterns, persistence, execution flow)
   - Campaign references where available
5. Labeled each sample using:
   - APT group name
   - File hash (MD5/SHA256)  
     ex:  
     /Executable Malware/  
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/Blacktech-G0098/  
         &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/malware name/  
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\<hash\>.exe  
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;metadata.txt  

Each sample has metadata to allow for reproducability:
- APT group name
- File type (Executable Malware / Other Payload)
- Hash (SHA256)
- Source reference (URL or report name)
- Campaign name when available
