#!/bin/bash

currentPath="$(pwd)"
#printf "current path : %s\n" $currentPath

#echo "$currentPath"/kernels/kernel_program.cl
"$currentPath"/bin/calc_opencode_amount \
    --work-folder "$currentPath" \
    --kernel-program /bin/kernel_program.cl