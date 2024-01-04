#!/bin/bash

for s in *.spec ; do
    cat $s | sed -e 's/frontera/stampede3/' \
	> stampede3_specfiles/$s
done
