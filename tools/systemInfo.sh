#!/bin/bash
grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}' 
free | grep "Mem" | awk '{usage=($3)*100/($2)} END {print usage "%"}'
df | grep "sda1" | awk '{print$5}'

tmp0=$(nvidia-smi -i 0 | grep "Default" | awk '{print $3}') #溫度
watt0="$(nvidia-smi -i 0 | grep "Default" | awk '{print $5}'),$(nvidia-smi -i 0 | grep "Default" | awk '{print $7}')" #瓦數
vram0="$(nvidia-smi -i 0 | grep "Default" | awk '{print $9}'),$(nvidia-smi -i 0 | grep "Default" | awk '{print $11}')" # 記憶體
echo "$tmp0,$watt0,$vram0"

tmp1=$(nvidia-smi -i 1 | grep "Default" | awk '{print $3}') #溫度
watt1="$(nvidia-smi -i 1 | grep "Default" | awk '{print $5}'),$(nvidia-smi -i 1 | grep "Default" | awk '{print $7}')" #瓦數
vram1="$(nvidia-smi -i 1 | grep "Default" | awk '{print $9}'),$(nvidia-smi -i 1 | grep "Default" | awk '{print $11}')" # 記憶體
echo "$tmp1,$watt1,$vram1"