#!/bin/bash

VER=$1
if [ "$VER" == debug ];
then
	make lotterykind=pk10 ver=debug
else
	make lotterykind=pk10
fi
