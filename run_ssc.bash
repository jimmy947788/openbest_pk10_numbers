#!/bin/bash

#currentPath="$(pwd)"
#printf "current path : %s\n" $currentPath
#WORKFOLDER="$currentPath"

WORKFOLDER="/home/matrix/openbest_pk10_numbers"
LOTTERY_KIND="ssc"

SERVICE="optimize_opencode -k $LOTTERY_KIND"
if ps ax | grep -v grep | grep "$SERVICE" > /dev/null
then
    echo "$SERVICE is running"
else
    echo "$SERVICE stopped"
    "$WORKFOLDER"/bin/$SERVICE
fi

tmp0=$(nvidia-smi -i 0 | grep "Default" | awk '{print $3}') #溫度
tmp1=$(nvidia-smi -i 1 | grep "Default" | awk '{print $3}') #溫度
if [ -z "$tmp0" ] && [ -z "$tmp1" ]
then
    #echo "tmp0=$tmp0, tmp1=$tmp1"
    reboot
fi

# 用GDB啟動
#sudo gdb bin/optimize_opencode -k ssc

# 用valgrind啟動 抓漏
#sudo valgrind ./bin/optimize_opencode -k ssc
#sudo valgrind --leak-check=full --show-leak-kinds=all --verbose --log-file=Valgrind.log ./bin/optimize_opencode -k ssc