#!/bin/bash

VER=$1
make clean
if [ "$VER" == debug ];
then
	make lotterykind=llX5 ver=debug
else
	make lotterykind=llX5
fi
