# HDF5 sequential sepcfile
# Victor Eijkhout

####
#### spec file for 1.14.3
#### as a non-default version
#### while we are up to 1.14.4
#### already
####
#### install.sh -p hdf5 -q 1.14.3 hdf5-1.14.3-seq
####
#### DO NOT UPDATE THIS SPEC FILE; WORK WITH hdf5-seq.spec FOR FUTURE UPDATES
####

Summary: Hdf5 install

# Give the package a base name
%define pkg_base_name hdf5
%define MODULE_VAR    HDF5

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 14
%define micro_version 3

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

Release: 5%{?dist}
License: GPL
Vendor: https://portal.hdfgroup.org
#Source1: hdf5-setup.sh
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{pkg_version}.tgz

%define debug_package %{nil}
%define _build_id_links none
## global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Hdf5 local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Hdf5 local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
Forest support library
%description %{MODULEFILE}
Forest support library

%prep

%setup -n hdf5-%{version}

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

export HDF5_DIR=`pwd`

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
  
mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/victor_scripts
export MAKEINCLUDES=${VICTOR}/make-support-files

pushd ${VICTOR}/makefiles/hdf5

module load cmake
module load zlib

## get rid of that PACKAGEROOT
make seq JCOUNT=20 \
    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIRSET=$RPM_BUILD_ROOT/%{MODULE_DIR}

popd

################ end of new stuff

#
# weird fix for difference between
# autotools and cmake install
#
pushd %{INSTALL_DIR}/lib
  ls
  ln -s libhdf_5hl_fortran.so libhdf5hl_fortran.so
  ln -s libhdf_5hl_fortran.so.310 libhdf5hl_fortran.so.310
popd

cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
## cp -r doc src test $RPM_BUILD_ROOT/%{INSTALL_DIR}/

umount %{INSTALL_DIR}

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
* Sat May 04 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 5 : re-instate 1.14.3

