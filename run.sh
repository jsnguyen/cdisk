#!/bin/bash

PREPATH=$(eval echo ~$USER)
FARGODIR="${PREPATH}/landing/programs/fargo3d"
NCPU=4

cd ${FARGODIR}

mpirun -np ${NCPU} ./fargo3d setups/mmr/mmr.par
