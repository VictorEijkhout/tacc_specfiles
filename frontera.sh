#!/bin/bash

mkdir -p frontera_specfiles
for s in *.spec ; do
    cat $s \
	> frontera_specfiles/$s
done

cat install.sh \
| sed -e 's/COMPILERS/i191 i231 g91 g132/' -e 's/MPI/19_9/' \
> frontera_specfiles/install.sh
chmod +x frontera_specfiles/install.sh
