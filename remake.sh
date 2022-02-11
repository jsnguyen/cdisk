#!/bin/bash

PREPATH=$(eval echo ~$USER)
MMRDIR="${PREPATH}/landing/code/mean_motion_resonance"
FARGODIR="${PREPATH}/landing/programs/fargo3d"

cd ${MMRDIR}

echo "Copying planet configs to ${FARGODIR}/planets/ ..."
cp mmr_1_2.cfg ${FARGODIR}/planets
cp mmr_1_2_4.cfg ${FARGODIR}/planets
cp mmr_1_2_4_8.cfg ${FARGODIR}/planets

echo "Copying \"visctensor_cyl.c\" to ${FARGODIR}/src/ ..."
cp visctensor_cyl.c "${FARGODIR}/src/"

echo "Generating par file..."
python3 generate_par.py $1

echo "Copying mmr/ to setups..."
cp -r mmr "${FARGODIR}/setups"

cd ${FARGODIR}

make clean

make SETUP=mmr RESCALE=0 UNITS=0 PARALLEL=1
