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

if [[ "${1}" == "1" ]]; then
    FDS=(${FD1})
fi

case ${1} in

  "1")
    FDS=(${FD1})
    ;;

  "2")
    FDS=(${FD2})
    ;;

  "3")
    FDS=(${FD3})
    ;;

  "4")
    FDS=(${FD4})
    ;;

  "all")
    FDS=(${FD1} ${FD2} ${FD3} ${FD4})
    ;;

  *)
    echo "Usage: ./run_multi.sh <1, 2, 3, 4, all>"
    exit
    ;;
esac


for FARGODIR in  ${FDS}; do

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
