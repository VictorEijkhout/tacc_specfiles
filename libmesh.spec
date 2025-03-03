Summary: Libmesh install

# Give the package a base name
%define pkg_base_name libmesh
%define MODULE_VAR    LIBMESH

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 8
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define python_version 3

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

Release: 3
License: GPLv2
Group: Development/Numerical-Libraries
Source: %{pkg_base_name}-%{pkg_version}.tgz
URL: https://github.com/libMesh
Vendor: CFDlab UT Austin
Packager: TACC -- eijkhout@tacc.utexas.edu

%define debug_package %{nil}
%define _build_id_links none
## global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Libmesh is a C++ Finite Element library
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: Libmesh is a C++ Finite Element library
Group: Development/Numerical-Libraries

%description
%description %{PACKAGE}
C++ FE
%description %{MODULEFILE}
C++ FE

%prep

%setup -n libmesh-%{version}

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

export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/victor_scripts
export MAKEINCLUDES=${VICTOR}/make-support-files

pushd ${VICTOR}/makefiles/%{pkg_base_name}

module load boost petsc phdf5

if [ "${TACC_SYSTEM}" = "vista" -a "${TACC_FAMILY_COMPILER}" = "gcc" ] ; then
    export LDFLAGS=-lm
fi

## get rid of that PACKAGEROOT
make configure build JCOUNT=10 \
    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    BUILDDIRROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIRSET=$RPM_BUILD_ROOT/%{MODULE_DIR}

popd

################ end of new stuff

cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r doc examples src tests $RPM_BUILD_ROOT/%{INSTALL_DIR}/
# popd

  rm -rf /tmp/build-${pkg_version}*

umount %{INSTALL_DIR}


%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}

#-----------------------
%endif
# BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

#--------------------------
%endif
# BUILD_MODULEFILE |
#--------------------------

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
* Wed Jan 29 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: 1.8.0-rc2
* Thu Dec 19 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: 1.8.0-rc1
* Tue Mar 09 2021 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
