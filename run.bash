#!/bin/bash

#currentPath="$(pwd)"
#printf "current path : %s\n" $currentPath
#WORKFOLDER="$currentPath"

WORKFOLDER="/home/matrix/openbest_pk10_numbers"

SERVICE="optimize_opencode"
if ps ax | grep -v grep | grep $SERVICE > /dev/null
then
    echo "$SERVICE is running"
else
    echo "$SERVICE stopped"
    #"$currentPath"/bin/calc_opencode_amount \
    #    --work-folder "$currentPath" \
    #    --kernel-program /bin/kernel_program.cl
    "$WORKFOLDER"/bin/$SERVICE \
        --worker-folder  "$WORKFOLDER" \
        --kernel-program bin/kernel_program.cl
fi

tmp0=$(nvidia-smi -i 0 | grep "Default" | awk '{print $3}') #溫度
tmp1=$(nvidia-smi -i 1 | grep "Default" | awk '{print $3}') #溫度
if [ -z "$tmp0" ] && [ -z "$tmp1" ]
then
    #echo "tmp0=$tmp0, tmp1=$tmp1"
    reboot
fi

#sudo gdb bin/optimize_opencode
#r --worker-folder  "/home/matrix/openbest_pk10_numbers"  --kernel-program bin/kernel_program.cl