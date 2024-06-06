#!/bin/bash

####
#### stupid shell script that emulates
#### an interactive setup run.
#### this has to be invoked 
#### from the source directory
####

echo "================ VLE set environment"
export CC=gcc
export CFLAGS='-O2 -ansi -std=c99 -fopenmp -fPIC'
export CCOPTIONS='-O2 -ansi -std=c99 -fopenmp -fPIC'
export FC=gfortran
export FFLAGS='-O2 -fPIC -fopenmp -fallow-argument-mismatch -fallow-invalid-boz'
export FCOPTIONS='-O2 -fPIC -fopenmp -fallow-argument-mismatch -fallow-invalid-boz'
export F90=gfortran
export F90FLAGS='-O2 -fPIC -fopenmp'
export CXX=g++
export CXXFLAGS='-O2 -ansi -std=c99 -fopenmp -fPIC'
export CPPFLAGS='-DNDEBUG'

# echo "================ VLE edit Linux settings"
# sed -i ncl-git/config/LINUX \
#     -e "/FcOptions/s/\$/ -O2 -fallow-argument-mismatch -fallow-invalid-boz/"
# echo "---------------- checking:"
# grep FcOptions ncl-git/config/LINUX
# echo "---------------- <<<<"

echo "================ VLE fix boz files"
find . -name \*.f \
     -exec sed -i -e "/Z'/s?/ Z'\([0-9A-F]+\)'?/ int(Z'\1')?p" {} \; 


echo "================ VLE build Site.Local"
rm -f config/Site.local

for d in /usr/lib64 ${TACC_NETCDF_LIB} ${TACC_HDF5_LIB} ${TACC_UDUNITS_LIB} \
    /usr/include/X11 /usr/include/freetype2 ${TACC_NETCDF_INC} ${TACC_HDF5_INC} ${TACC_UDUNITS_INC} ; do 
    if [ ! -d "${d}" ] ; then 
	echo "Non-existing directory <<$d>>" && exit 1
    fi
done


for line in \
    "" \
    "" \
    "y,do build" \
    "${STOCKYARD}/ncl/installation-${TACC_SYSTEM},install location" \
    "${STOCKYARD}/ncl/tmp,tmp location" \
    "n,no netcdf4" \
    "n,no hdf4" \
    "n,no hdf4 in raster" \
    "n,no triangle" \
    "n,netcdf has no netcdf4 support" \
    "y,netcdf has opendap support" \
    "n,do not build GDAL support" \
    "n,do not build EEMD support" \
    "y,build udunits support" \
    "n,do not build Vis5d support" \
    "n,do not build HDF-EOS2 support" \
    "y,build HDF5 support" \
    "n,do not build HDF-EOS5 support" \
    "n,do not build GRIB2 support" \
    "${TACC_NETCDF_LIB} ${TACC_HDF5_LIB} ${TACC_UDUNITS_LIB} /usr/lib64,lib search" \
    "/usr/include/X11 /usr/include/freetype2 ${TACC_NETCDF_INC} ${TACC_HDF5_INC} ${TACC_UDUNITS_INC},inc search" \
    "n,no changes" \
    "y,yes save configuration" \
    ; \
do
    line=${line%,*}
    echo $line
done | \
./Configure  -v
    ## 2>&1 | tee ${STOCKYARD/ncl/configure.log

echo "Now do: make Everything"
