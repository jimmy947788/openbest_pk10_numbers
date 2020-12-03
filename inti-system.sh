#!/bin/bash

# apt search nvidia-driver


apt-get install net-tools hwinfo vim clinfo ocl-icd-libopencl1 opencl-headers ocl-icd-opencl-dev lsb-core nvidia-driver-455 python3-pip -y

sudo -H pip3 install Flask
sudo -H pip3 install pandas
sudo -H pip3 install pyopencl