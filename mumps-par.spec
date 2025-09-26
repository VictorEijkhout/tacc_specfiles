# MUMPS parallel install
# Victor Eijkhout 2024

Summary: Mumps install

# Give the package a base name
%define pkg_base_name mumps
%define MODULE_VAR    MUMPS

# Create some macros (spec file variables)
%define major_version 5
%define minor_version 8
%define micro_version 1

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

Release: 2
License: GPL
Vendor: https://portal.hdfgroup.org
#Source1: mumps-setup.sh
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: mumps-%{pkg_version}.tgz

%define debug_package %{nil}
%define _build_id_links none
## global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: Mumps local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Mumps local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
Forest support library
%description %{MODULEFILE}
Forest support library

%prep

%setup -n mumps-%{version}

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

export MUMPS_DIR=`pwd`

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
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export MAKEINCLUDES=${VICTOR}/make-support-files

pushd ${VICTOR}/makefiles/mumps

module -t list | sort | tr '\n' ' '
module load metis parmetis ptscotch
if [ "${TACC_FAMILY_COMPILER}" = "gcc" ] ; then 
    module load mkl
fi
module -t list | sort | tr '\n' ' '

## get rid of that PACKAGEROOT
##
## Vista nvidia has a problem with Fortran:
## HDFFORTRAN=off
##
make par JCOUNT=20 \
    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    $( if [ "${TACC_FAMILY_COMPILER}" = "nvidia" ] ; then echo TESTING=OFF ; fi ) \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    BUILDDIRROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIRSET=$RPM_BUILD_ROOT/%{MODULE_DIR}

popd

################ end of new stuff

cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
## cp -r doc src test $RPM_BUILD_ROOT/%{INSTALL_DIR}/

  rm -rf /tmp/build-${pkg_version}*

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
* Thu Sep 25 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 2 : 5.8.1 shared
* Mon Jun 16 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 1 : first release
