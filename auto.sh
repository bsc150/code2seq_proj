#!/bin/bash

# Creators: Nadav Dadush, Maya Wolff

# Step 1:
# Run analysis on coreutils files. (our_preprocess)
# Possible changes to preprocess can be done directly from bash_script.sh
bash bash_script.sh

# Step 2 (optional):
# Run postprocess on the output file.
# python3 postprocess output.txt

# Step 3:
# Create test, train, validation files (files created automatically will be located under "data/assembly/"
python3 divide.py output.txt

# Step 4:
# Activate the network
bash preprocess.sh
bash train.sh
