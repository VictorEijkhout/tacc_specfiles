#!/bin/bash

mkdir -p ls6_specfiles
for s in *.spec ; do
    ## restore CUDAFLAG -c
    cat $s \
	| sed \
	    -e 's/frontera/ls6/' \
	    -e 's/PETSCCUDAFLAG//' \
	    -e '/noreloc/s/name-defines.*$/name-defines-noreloc-scratch.inc/' \
	    -e '/FRONTERA/d' \
	    -e '/LS6/s/LS6 //' \
	    -e /cuda-defines/d \
	    -e 's/GCCDEF/13/' \
	    -e 's/GCCMIN/9/' \
	    -e 's/CMAKEMIN/3.21/' \
	> ls6_specfiles/$s
done

cat install.sh \
    | sed -e 's/frontera/ls6/' -e 's/COMPILERS/i241,j21_12 i253,j21_17 i19,j19_0 g112,j19_0 g132,j21_12/' \
    > ls6_specfiles/install.sh

cd ls6_specfiles
chmod +x install.sh
