#!/bin/bash

function usage() {
    echo "Usage: $0 "
    echo "    [ -c gcc/intel : limit to one family ]"
    echo "    [ -m (for mpi) ]"
    echo "    [ -p (for actual name) ] specname"
}

if [ $# -eq 0 ] ; then
    usage && exit 0
fi

mpi=
name=
compfamily=
while [ $# -gt 1 ] ; do
    if [ $1 = "-h" ] ; then
        usage && return 0;
    elif [ $1 = "-c" ] ; then 
	shift && compfamily=$1 && shift 
    elif [ $1 = "-m" ] ; then
        mpi=1 && shift
    elif [ $1 = "-p" ] ; then
        shift && name=$1 && shift
    fi
done

##
## package name and installed name
##
specname=$1
if [ -z "${name}" ] ; then
    name=$specname
fi
echo "Installing package=$name from specfile=$specname"

specdir=/admin/build/admin/rpms/frontera/SPECS
if [ ! -d "${specdir}" ] ; then
    echo "ERROR no specfile dir <<${specdir}>>" && exit 1
fi
cd ${specdir}
taccfiles=${specdir}/victor_scripts/tacc_specfiles/

##
## determine version and release frm the versions.txt file
##
cmdline=$( cat ${taccfiles}/versions.txt \
               | awk '/'${name}' / {print "pcheck="$1" version="$2" release="$3 }'
       )
eval $cmdline
if [ -z "${version}" ] ; then
    echo "ERROR could not extract version for <<${name}>>" && exit 1
fi

##
## find the spec file
##
specfile=${taccfiles}/frontera_specfiles/${specname}.spec
if [ ! -f "${specfile}" ] ; then
    echo "ERROR could not find spec file <<${specfile}>>" && exit 1
fi

##
## build the rpm for all available compiler
##
for config in COMPILERS ; do
    cmp=${config%%,*}
    cmpfam=${cmp%%/*}
    mpi=${config##*,}
    if [ -z ${compfamily} -o ${cmpfam} = ${compfamily} ] ; then 
	echo "building ${name}/${version} with compiler=${cmp}"
	./build_rpm.sh -${cmp} -l \
            $( if [ ! -z "$mpi" ] ; then echo -${mpi} ; fi ) \
            ${specfile}
    fi
done

for p in ../RPMS/x86_64/tacc-${name}-*package-${version}-${release}* ; do
    rpm -i --force --nodeps $p
done
for p in ../RPMS/x86_64/tacc-${name}-*modulefile-${version}-${release}* ; do
    rpm -i --force --nodeps $p
done

ls -l \
  ../RPMS/x86_64/tacc-${name}-*package-${version}-${release}* \
  ../RPMS/x86_64/tacc-${name}-*modulefile-${version}-${release}*
