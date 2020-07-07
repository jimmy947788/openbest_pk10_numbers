#!/bin/bash

currentPath="$(pwd)"
#printf "current path : %s\n" $currentPath

#echo "$currentPath"/kernels/kernel_program.cl
"$currentPath"/bin/calc_opencode_amount \
    --kernel-program "$currentPath"/kernels/kernel_program.cl \
    --opencode-answer "$currentPath"/data/opencode_table_all.csv 