Summary: Parmetis install

# Give the package a base name
%define pkg_base_name parmetis
%define MODULE_VAR    PPARMETIS

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 0
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

Release: 2%{?dist}
License: GPL
Vendor: https://github.com/scibuilder/parmetis
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{pkg_version}.tgz

%define debug_package %{nil}
%define _build_id_links none
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: Parmetis local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Parmetis local binary install
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

export PARMETIS_DIR=`pwd`

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

module load cmake

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

    pushd ${VICTOR}/makefiles/%{pkg_base_name}

    ## get rid of that PACKAGEROOT
    export    BUILDDIRROOT=/tmp/%{pkg_base_name}
    make configure build JCOUNT=20 \
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
* Wed Feb 07 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 2 : just to be sure
* Thu Nov 30 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 1 : initial install with this structure
