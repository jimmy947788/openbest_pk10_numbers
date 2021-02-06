#!/bin/bash

# apt search nvidia-driver


apt-get install net-tools hwinfo vim clinfo ocl-icd-libopencl1 opencl-headers ocl-icd-opencl-dev lsb-core nvidia-driver-455 python3-pip libjson-c-dev -y 
apt-get install valgrind #指標抓漏工具

sudo -H pip3 install Flask
sudo -H pip3 install pandas
sudo -H pip3 install pyopencl

#SWAP加到10G
# https://shazi.info/ubuntu-16-04-%E5%BB%BA%E7%AB%8B-swap-file-%E8%AA%BF%E6%A0%A1-swap/

# 更新linux kernel 5
sudo dpkg -i  kernel-5.9.16/*.deb
