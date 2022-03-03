#!/bin/bash

PREPATH=$(eval echo ~$USER)
CDIDIR="${PREPATH}/landing/code/cdisk"
FARGODIR="${PREPATH}/landing/programs/fargo3d"

cd ${CDIDIR}

echo "Copying planet configs to ${FARGODIR}/planets/ ..."
cp cdi.cfg ${FARGODIR}/planets

echo "Copying \"visctensor_cyl.c\" to ${FARGODIR}/src/ ..."
cp visctensor_cyl.c "${FARGODIR}/src/"

echo "Generating par file..."
python3 generate_par.py $1

echo "Copying cdi/ to setups..."
cp -r cdi "${FARGODIR}/setups"

cd ${FARGODIR}

#make clean

make SETUP=cdi RESCALE=0 UNITS=0 PARALLEL=1
