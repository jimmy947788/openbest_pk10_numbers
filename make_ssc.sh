#!/bin/bash

VER=$1
if [ "$VER" == debug ];
then
	make lotterykind=ssc ver=debug
else
	make lotterykind=ssc
fi
