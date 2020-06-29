#!/bin/bash

currentPath="$(pwd)"
#printf "current path : %s\n" $currentPath

#echo "$currentPath"/kernels/kernel_program.cl
"$currentPath"/bin/calc_opencode_amount \
    --kernel-program "$currentPath"/kernels/kernel_program.cl \
    --opencode-answer "$currentPath"/data/opencode_table.csv \
    --beton-amount "$currentPath"/data/beton_amount_20200619062.csv \
    --beton-amount-with-odds "$currentPath"/data/beton_amount_with_odds_20200619062.csv 