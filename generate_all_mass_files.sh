#!/bin/bash

for d in /home/jsn/landing/data/pds70c_*/; do
    echo ${d}
    python3 generate_mass_files.py ${d}
done
