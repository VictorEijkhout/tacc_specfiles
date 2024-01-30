#!/bin/bash

mkdir -p frontera_specfiles
for s in *.spec ; do
    cat $s \
	> frontera_specfiles/$s
done

cat install.sh \
> frontera_specfiles/install.sh
