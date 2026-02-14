Summary: Petsc install

# Give the package a base name
%define pkg_base_name petsc
%define MODULE_VAR    PETSC

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 22
#define micro_version 5

%define pkg_version %{major_version}.%{minor_version}
#{micro_version}

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

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

Release: 25
License: GPL
Vendor: https://portal.hdfgroup.org
#Source1: petsc-setup.sh
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{pkg_version}.tgz

# Turn off debug package mode
%define debug_package %{nil}
%define _build_id_links none
%define dbg           %{nil}
## global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0
# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%package %{PACKAGE}
Summary: Petsc local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Petsc local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
Forest support library
%description %{MODULEFILE}
Forest support library

%prep

%setup -n %{pkg_base_name}-%{version}

#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc
%include compiler-defines.inc
%include mpi-defines.inc
module purge
%include compiler-load.inc
%include mpi-load.inc

export PETSC_DIR=`pwd`

#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  #========================================
  # Insert Build/Install Instructions Here
  #========================================
  
export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export MAKEINCLUDES=${VICTOR}/make-support-files

pushd ${VICTOR}/makefiles/%{pkg_base_name}

module --latest load cmake
if [ "${TACC_SYSTEM}" = "ls6" -o "${TACC_SYSTEM}" = "vista" ] ; then
    module load cuda
fi
# module load python3
pip3 install numpy

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

if [ "${TACC_FAMILY_COMPILER}" = "gcc" ] ; then
  disablefortran=-f
fi

export    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES 
export    PACKAGEVERSION=%{pkg_version} 
export    PACKAGEROOT=/tmp 
export    BUILDDIRROOT=/tmp
export    SRCPATH=${SRCPATH} 
export     INSTALLPATH=%{INSTALL_DIR} 
export    MODULEDIRSET=$RPM_BUILD_ROOT/%{MODULE_DIR}
export    BUILDDIRROOT=/tmp/%{pkg_base_name}
./install_all.sh \
    -j 16 \
    PETSCCUDAFLAG -4 ${disablefortran} \
    -v %{pkg_version} 
popd

################ end of new stuff

find %{INSTALL_DIR} -name \*.py -exec sed -i -e 's?env python *$?env python3?' {} \; -print
cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
## cp -r doc src test $RPM_BUILD_ROOT/%{INSTALL_DIR}/

rm -rf /tmp/build-${pkg_version}*

umount %{INSTALL_DIR}

## %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

%files %{PACKAGE}
  %defattr(0644,root,root,0755)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(0644,root,root,0755)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Oct 14 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 25: 3.22 only for nv fortran

