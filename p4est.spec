Summary: P4est install

# ./build_rpm.sh -i231 -j21_9 -l p4est-new

# Give the package a base name
%define pkg_base_name p4est
%define MODULE_VAR    P4EST

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 8
%define micro_version 7
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

Release: 6
License: GPL
Vendor: https://github.com/cburstedde/p4est
#Source1: p4est-setup.sh
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{pkg_version}.tgz

%define debug_package %{nil}
%define _build_id_links none
## global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: P4est local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: P4est local binary install
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

#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

## module load
module --latest load cmake
module load python3/3.9
module -t list | sort | tr '\n' ' '

export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export MAKEINCLUDES=${VICTOR}/make-support-files

#
# MrPackMod
#
export PATH=/admin/build/admin/rpms/frontera/SPECS/rpmtng/MrPackMod:${PATH}
export PYTHONPATH=/admin/build/admin/rpms/frontera/SPECS/rpmtng:${PYTHONPATH}

pushd ${VICTOR}/makefiles/%{pkg_base_name}

if [ "${TACC_SYSTEM}" = "vista" -a "${TACC_FAMILY_COMPILER}" = "gcc" ] ; then
    export LDFLAGS=-lm
fi

## get rid of that PACKAGEROOT
HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIRSET=$RPM_BUILD_ROOT/%{MODULE_DIR} \
mpm.py -t -j 20 install

popd

################ end of new stuff

cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r doc example src test $RPM_BUILD_ROOT/%{INSTALL_DIR}/
# popd

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
* Wed Jan 07 2026 eijkhout <eijkhout@tacc.utexas.edu>
- release 6: add cmake prefix
* Mon May 12 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 5: 2.8.7, no petsc dependence
* Wed Mar 27 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: up to 2.8.6
* Tue Mar 21 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 3 using new makefile structure
* Mon Sep 30 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 2 for no known reason
* Mon Jun 03 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
