#!/bin/bash

# exit on error
set -e

PREPATH=$(eval echo ~$USER)
FARGODIR="${PREPATH}/landing/programs/fargo3d"
NCPU=32

cd ${FARGODIR}

echo "Using ${NCPU} cores"
mpirun -np ${NCPU} ./fargo3d setups/cdi/cdi.par
