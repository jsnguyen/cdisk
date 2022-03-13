#!/bin/bash

# exit on error
set -e

PREPATH=$(eval echo ~$USER)
CDIDIR="${PREPATH}/landing/code/cdisk"

#FARGODIR="${PREPATH}/landing/programs/fargo3d"

FD1="${PREPATH}/landing/programs/f3d1"
FD2="${PREPATH}/landing/programs/f3d2"
FD3="${PREPATH}/landing/programs/f3d3"
FD4="${PREPATH}/landing/programs/f3d4"

for FARGODIR in ${FD1} ${FD2} ${FD3} ${FD4}; do
    cd ${FARGODIR}
    make clean
    make SETUP=cdi RESCALE=0 UNITS=CGS PARALLEL=1
done
