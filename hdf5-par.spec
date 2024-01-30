Summary: Hdf5 install

# ./build_rpm.sh -i191 -j19_9 -l hdf5-par
# ./build_rpm.sh -i231 -j21_9 -l hdf5-par
# ./build_rpm.sh -g91 -j19_9 -l hdf5-par
					
# Give the package a base name
%define pkg_base_name phdf5
%define MODULE_VAR    PHDF5

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 14
%define micro_version 3

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

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

Release: 4%{?dist}
License: GPL
Vendor: https://portal.hdfgroup.org
#Source1: hdf5-setup.sh
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: hdf5-%{pkg_version}.tar.gz

%define debug_package %{nil}
%define _build_id_links none
## %global _missing_build_ids_terminate_build 0
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
%include mpi-defines.inc
module purge
%include compiler-load.inc
%include mpi-load.inc

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

module load cmake zlib

## get rid of that PACKAGEROOT
make par JCOUNT=20 \
    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIRSET=$RPM_BUILD_ROOT/%{MODULE_DIR}

popd

################ end of new stuff

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
* Mon Aug 07 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: now with fortran enabled
* Tue Mar 21 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 3 using new makefile structure
