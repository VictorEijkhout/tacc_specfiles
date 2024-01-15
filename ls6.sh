#!/bin/bash

mkdir -p ls6_specfiles
for s in *.spec ; do
    cat $s \
	| sed -e 's/frontera/ls6/' -e '/noreloc/s/name-defines.*$/name-defines-noreloc-scratch.inc/' \
	> ls6_specfiles/$s
done
