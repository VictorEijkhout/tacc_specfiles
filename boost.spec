#
# Boost by Victor, as opposed to Si Liu
#
# ./build_rpm.sh -i191 -l boost-new
# ./build_rpm.sh -i231 -l boost-new
# ./build_rpm.sh -g91 -l boost-new
# ./build_rpm.sh -g132 -l boost-new

Summary: Boost install

# Give the package a base name
%define pkg_base_name boost
%define MODULE_VAR    BOOST

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 84
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%include rpm-dir.inc
%include compiler-defines.inc
## %include mpi-defines.inc

########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc-home1.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release: 3%{?dist}
License: GPL
Vendor: https://github.com/cburstedde/boost
#Source1: boost-setup.sh
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{version}.tgz

%define debug_package %{nil}
%define _build_id_links none
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: Boost local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Boost local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
Forest support library
%description %{MODULEFILE}
Forest support library

%prep

%setup -n boost-%{version}

#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc
%include compiler-defines.inc
## %include mpi-defines.inc
module purge
%include compiler-load.inc
## %include mpi-load.inc

export BOOST_DIR=`pwd`

#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

# %if "%{comp_fam}" == "gcc"
#   module load mkl
#   export BLASOPTIONS="-Wl,--start-group $MKLROOT/lib/intel64/libmkl_intel_lp64.so $MKLROOT/lib/intel64/libmkl_sequential.so $MKLROOT/lib/intel64/libmkl_core.so -Wl,--end-group -lpthread -lm"
#   export BLASFLAG=
# %else
#   export BLASOPTIONS=
#   export BLASFLAG=-mkl
# %endif

################ new stuff

export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/victor_scripts
export MAKEINCLUDES=${VICTOR}/make-support-files

pushd ${VICTOR}/makefiles/boost

## module load petsc/3.18

## get rid of that PACKAGEROOT
make configure build JCOUNT=10 \
    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIRSET=$RPM_BUILD_ROOT/%{MODULE_DIR}

popd

################ end of new stuff

cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
## cp -r doc example src test $RPM_BUILD_ROOT/%{INSTALL_DIR}/

umount %{INSTALL_DIR}

# cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
# help( [[
# The BOOST modulefile defines the following environment variables:
# TACC_BOOST_DIR, TACC_BOOST_LIB, and TACC_BOOST_INC 
# for the location of the BOOST %{version} distribution, 
# libraries, and include files, respectively.

# Version %{pkg_version}
# ]] )

# whatis( "Name: Boost 'p4-est of octrees'" )
# whatis( "Version: %{version}-${ext}" )
# whatis( "Version-notes: ${boostversion}" )
# whatis( "Category: library, mathematics" )
# whatis( "URL: https://github.com/cburstedde/boost" )
# whatis( "Description: octree support for dealii" )

# local             boost_dir =     "%{INSTALL_DIR}"

# prepend_path("LD_LIBRARY_PATH", pathJoin(boost_dir,"lib") )
# prepend_path("PATH", pathJoin(boost_dir,"bin") )

# setenv(          "BOOST_DIR",             boost_dir)
# setenv(          "TACC_BOOST_DIR",        boost_dir)
# setenv(          "TACC_BOOST_BIN",        pathJoin(boost_dir,"bin"))
# setenv(          "TACC_BOOST_INC",        pathJoin(boost_dir,"include"))
# setenv(          "TACC_BOOST_LIB",        pathJoin(boost_dir,"lib"))

# EOF

# cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${version} << EOF
# #%Module1.0#################################################
# ##
# ## version file for Boost %version
# ##

# set     ModulesVersion      "${modulefilename}"
# EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Mar 04 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: up to 1.84, adding system
* Fri Jan 05 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 2 : up to 1.83
* Tue Mar 21 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release 1.81.0
