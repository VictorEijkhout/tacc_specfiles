#!/bin/bash

for s in *.spec ; do
    cat $s \
	| sed -e 's/frontera/stampede3/' -e '/noreloc/s/name-defines.*$/name-defines-noreloc.inc/' \
	> stampede3_specfiles/$s
done