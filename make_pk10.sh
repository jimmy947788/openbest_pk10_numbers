#!/bin/bash

VER=$1
make clean
if [ "$VER" == debug ];
then
	make lotterykind=pk10 ver=debug
else
	make lotterykind=pk10
fi
