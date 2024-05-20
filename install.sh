#!/bin/bash

function usage() {
    echo "Usage: $0 "
    echo "    [ -c g/i : limit to one family ] [ -v 123 : compiler specific version ]"
    echo "    [ -j jcount] [ -m (for mpi) ]"
    echo "    [ -p installed_package_name ] [ -q other_than_default_version ]"
    echo "    specname"
}

if [ $# -eq 0 -o $1 = "-h" ] ; then
    usage && exit 0
fi

mpi=
name=
version=
compfamily=
compversion=
jcount=8
while [ $# -gt 1 ] ; do
    if [ $1 = "-h" ] ; then
        usage && return 0;
    elif [ $1 = "-c" ] ; then
        shift && compfamily=$1 && shift
        echo "Install only with compiler=<<${compfamily}>>"
    elif [ $1 = "-j" ] ; then
        shift && jcount=$1 && shift
        echo "Using threads: $jcount (ignored!)"
    elif [ $1 = "-v" ] ; then
        shift && compversion=$1 && shift
        echo "install only with version=<<${compversion}>>"
    elif [ $1 = "-m" ] ; then
        mpi=1 && shift
        echo "Install with MPI"
    elif [ $1 = "-p" ] ; then
        shift && name=$1 && shift
        echo "Install for package name <<$name>>"
    elif [ $1 = "-q" ] ; then
        shift && version=$1 && shift
        echo "Install for package version <<$version>>"
    else
	echo "ERROR unrecognized option $1" && exit 1
    fi
done

##
## package name and installed name
##
specname=$1
if [ -z "${name}" ] ; then
    name=$specname
fi
# strip in ase of auto-complete
specname=${specname%%.spec}
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
if [ -z "${version}" ] ; then
    cmdline=$( cat ${taccfiles}/versions.txt \
		   | awk '/^'${name}' / {print "pcheck="$1" version="$2" release="$3 }'
	   )
    eval $cmdline
    if [ -z "${version}" ] ; then
	echo "ERROR could not extract version for <<${name}>>" && exit 1
    fi
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
    cmpfam=${cmp%%[0-9]*} # single letter!
    cmpver=${cmp##*[a-z]}
    echo "compiler: $cmpfam+$cmpver"
    mpi=${config##*,}
    cdo=1 && cvr=1
    if [ ! -z "${compfamily}" ] ; then
        if [[ ! ${compfamily} =~ ${cmpfam} ]] ; then cdo=0; fi ; fi
    if [ ! -z "${compversion}" ] ; then
        if [[ ! ${cmpver} =~ ${compversion} ]] ; then cvr=0; fi ; fi
    if [ $cdo -eq 1 -a $cvr -eq 1 ] ; then
        echo "building ${name}/${version} with compiler=${cmp}"
        ./build_rpm.sh -${cmp} -l \
            $( if [ ! -z "$mpi" ] ; then echo -${mpi} ; fi ) \
            ${specfile}
    else
        echo "Skip compiler/version <<$compfamily/$compversion>>"
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
