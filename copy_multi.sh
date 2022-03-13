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

    cd ${CDIDIR}

    echo "Generating par file..."
    python3 generate_par.py $1

    echo "Copying planet configs to ${FARGODIR}/planets/ ..."
    cp cdi.cfg ${FARGODIR}/planets

    echo "Copying \"visctensor_cyl.c\" to ${FARGODIR}/src/ ..."
    cp visctensor_cyl.c "${FARGODIR}/src/"

    echo "Copying \"main.c\" to ${FARGODIR}/src/ ..."
    cp main.c "${FARGODIR}/src/"

    echo "Copying \"prototypes.h\" to ${FARGODIR}/src/ ..."
    cp prototypes.h "${FARGODIR}/src/"

    echo "Copying \"fondam.h\" to ${FARGODIR}/src/ ..."
    cp fondam.h "${FARGODIR}/src/"

    echo "Copying \"boundaries.txt\" to ${FARGODIR}/std/ ..."
    cp boundaries.txt "${FARGODIR}/std/"

    echo "Copying cdi/ to setups..."
    cp -r cdi "${FARGODIR}/setups"

done
