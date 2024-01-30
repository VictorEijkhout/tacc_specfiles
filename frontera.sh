#!/bin/bash

mkdir -p frontera_specfiles
for s in *.spec ; do
    cat $s \
	> frontera_specfiles/$s
done
