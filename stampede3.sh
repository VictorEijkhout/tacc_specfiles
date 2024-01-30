#!/bin/bash

mkdir -p stampede3_specfiles
for s in *.spec ; do
    cat $s \
	| sed -e 's/frontera/stampede3/' -e '/noreloc/s/name-defines.*$/name-defines-noreloc.inc/' \
	> stampede3_specfiles/$s
done

cat install.sh \
| sed -e 's/fontera/stampede3/' -e 's/COMPILERS/i240 g132/' \
> stampede3/install.sh
chmod +x stampede3/install.sh
