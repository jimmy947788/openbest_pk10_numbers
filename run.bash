#!/bin/bash

#currentPath="$(pwd)"
#printf "current path : %s\n" $currentPath
WORKFOLDER="/home/matrix/openbest_pk10_numbers"

SERVICE="calc_opencode_amount"
if ps ax | grep -v grep | grep $SERVICE > /dev/null
then
    echo "$SERVICE is running"
else
    echo "$SERVICE stopped"
    #"$currentPath"/bin/calc_opencode_amount \
    #    --work-folder "$currentPath" \
    #    --kernel-program /bin/kernel_program.cl
    "$WORKFOLDER"/bin/calc_opencode_amount \
        --work-folder  "$WORKFOLDER" \
        --kernel-program /bin/kernel_program.cl
fi
