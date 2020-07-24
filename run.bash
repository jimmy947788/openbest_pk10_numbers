#!/bin/bash

currentPath="$(pwd)"
#printf "current path : %s\n" $currentPath

#echo "$currentPath"/kernels/kernel_program.cl
"$currentPath"/bin/calc_opencode_amount \
    --kernel-program "$currentPath"/bin/kernel_program.cl \
    --opencode-answer-table "$currentPath"data\opencode_table_1.csv,"$currentPath"data\opencode_table_2.csv