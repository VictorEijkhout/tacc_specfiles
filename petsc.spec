Summary: Petsc install

# Give the package a base name
%define pkg_base_name petsc
%define MODULE_VAR    PETSC

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 23
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

Release: 19
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
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/victor_scripts
export MAKEINCLUDES=${VICTOR}/make-support-files

pushd ${VICTOR}/makefiles/%{pkg_base_name}

module load cmake 
# module load python3
pip3 install numpy

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

export    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES 
export    PACKAGEVERSION=%{pkg_version} 
export     PACKAGEROOT=/tmp 
export    BUILDDIRROOT=/tmp
export    SRCPATH=${SRCPATH} 
export     INSTALLPATH=%{INSTALL_DIR} 
export    MODULEDIRSET=$RPM_BUILD_ROOT/%{MODULE_DIR}
export    BUILDDIRROOT=/tmp/%{pkg_base_name}
./install_all.sh PETSCCUDAFLAG -4 -j 20 -v %{pkg_version} 
popd

################ end of new stuff

find %{INSTALL_DIR} -name \*.py -exec sed -i -e 's?env python *$?env python3?' {} \; -print
cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
## cp -r doc src test $RPM_BUILD_ROOT/%{INSTALL_DIR}/

  rm -rf /tmp/build-${pkg_version}*

umount %{INSTALL_DIR}

## %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon May 12 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 19: 3.23.1
* Tue Apr 15 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 18: 3.23
* Wed Mar 05 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 17 adding superlu & strumpack
* Wed Jan 29 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 16 just for a S3 rebuild
* Tue Jan 07 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 15 to 3.22.2, cuda install
* Tue Dec 17 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 14 up to 3.22.1
* Mon Oct 07 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 13 up to 3.22.0
* Fri Sep 06 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 12 UNRELEASED up to 3.21.5
* Thu Aug 08 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 11: up to 3.21.4
* Tue Jul 16 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 10: no fftw with single, no hypre with complex
* Wed Jul 03 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 9: mumps works with complex after all
* Thu May 09 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 8: python3 fix
* Fri Apr 26 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 7: 3.21.1 fixes K&R packages
* Tue Apr 16 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 6: 3.21, fix scalar-type=complex
* Wed Mar 20 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 5 : use downloaded hypre
* Tue Mar 12 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 4 : up to 3.20.5, adding f08 versions
* Thu Feb 22 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: adding ptscotch and nohdf5
* Wed Feb 14 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 2 : up to 3.20.4
* Tue Jan 02 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: new setup, first install of 3.20
