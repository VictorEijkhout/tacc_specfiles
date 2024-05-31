Summary: Aspect install

# Give the package a base name
%define pkg_base_name aspect
%define MODULE_VAR    ASPECT

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 5
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%define aspectdealversion 9.5.2

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
License: GPLv2
Group: Development/Numerical-Libraries
Source: %{pkg_base_name}-%{pkg_version}.tgz
URL: http://www.aspect.org/
Vendor: TAMU
Packager: TACC -- eijkhout@tacc.utexas.edu

%define debug_package %{nil}
%define _build_id_links none
## global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Aspect is an open source finite element package
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: Aspect is an open source finite element package
Group: Development/Numerical-Libraries

%description
%description %{PACKAGE}

%description %{MODULEFILE}

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
%include compiler-load.inc
%include mpi-load.inc

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
  
module load cmake 
module load dealii/%{aspectdealversion} \
module load metis
module load trilinos/%{aspecttrilinosversion}
module load mumps netcdf phdf5

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

## get rid of that PACKAGEROOT
make small big JCOUNT=20 \
    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIRSET=$RPM_BUILD_ROOT/%{MODULE_DIR}

popd

################ end of new stuff

cp -r contrib   data    unit_tests \
    benchmarks  doc  source    VERSION \
    CITATION     CODE_OF_CONDUCT.md  cookbooks  LICENSE          tests \
    %{INSTALL_DIR}
cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/

umount %{INSTALL_DIR}

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

##
## end of configure install section
##

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
* Mon Feb 04 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 2 : new setup, 2.5 0
* Fri Jul 30 2021 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release of 2.2.0
