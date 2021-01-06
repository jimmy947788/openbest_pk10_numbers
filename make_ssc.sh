#!/bin/bash

VER=$1
make clean
if [ "$VER" == debug ];
then
	make lotterykind=ssc ver=debug
else
	make lotterykind=ssc
fi
