#!/bin/bash

function usage() {
    echo "Usage: $0 "
    echo "    [ -c g/i : limit to one family ] [ -v 123 : compiler specific version ]"
    echo "    [ -j jcount] [ -m (for mpi) ]"
    echo "    [ -p installed_package_name ] [ -q other_than_default_version ]"
    echo "    [ -r (rpm install only) ]"
    echo "    specname"
}

if [ $# -eq 0 -o $1 = "-h" ] ; then
    usage && exit 0
fi

mpi=
packagename=
version=
compfamily=
compversion=
jcount=8
rpmonly=
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
        shift && packagename=$1 && shift
        echo "Install for package name <<$packagename>>"
    elif [ $1 = "-q" ] ; then
        shift && version=$1 && shift
        echo "Install for package version <<$version>>"
    elif [ $1 = "-r" ] ; then
	rpmonly=1 && shift
    else
	echo "ERROR unrecognized option $1" && exit 1
    fi
done

##
## package name and installed name
##
specname=$1
# strip in ase of auto-complete
specname=${specname%%.spec}
if [ -z "${packagename}" ] ; then
    packagename=$specname
fi
echo "Installing package=$packagename from specfile=$specname"

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
                   | awk '/^'${packagename}' / {print "pcheck="$1" version="$2" release="$3 }' \
           )
    if [ -z "${cmdline}" ] ; then
        echo "ERROR not finding <<${packagename}>> in versions.txt"
        exit 1
    fi
    ## echo $cmdline
    eval $cmdline
    if [ "${pcheck}" != "${packagename}" ] ; then
        echo "ERROR got line for <<${pcheck}>> instead of <<${packagename}>>"
        exit 1
    fi
    if [ -z "${version}" ] ; then
        echo "ERROR could not extract version for <<${packagename}>>" && exit 1
    fi
    echo "Found version <<${version}>> in versions.txt"
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
if [ -z "${rpmonly}" ] ; then 
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
            echo "building ${packagename}/${version} with compiler=${cmp}"
            ./build_rpm.sh -${cmp} -l \
			   $( if [ ! -z "$mpi" ] ; then echo -${mpi} ; fi ) \
			   ${specfile}
	else
            echo "Skip compiler/version <<$compfamily/$compversion>>"
	fi
    done
fi

for p in ../RPMS/x86_64/tacc-${packagename}-*package-${version}-${release}* ; do
    rpm -i --force --nodeps $p
done
for p in ../RPMS/x86_64/tacc-${packagename}-*modulefile-${version}-${release}* ; do
    rpm -i --force --nodeps $p
done

ls -l \
  ../RPMS/x86_64/tacc-${packagename}-*package-${version}-${release}* \
  ../RPMS/x86_64/tacc-${packagename}-*modulefile-${version}-${release}*
