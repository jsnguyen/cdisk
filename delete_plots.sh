#!/bin/bash

PREPATH=$(eval echo ~$USER)
cd "${PREPATH}/landing/code/cdisk/plots"

rm -f animation.gif
rm -f disk_mass.*
rm -f gasdens*.*
