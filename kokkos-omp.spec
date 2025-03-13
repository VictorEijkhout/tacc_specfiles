# KOKKOS specfile
# Victor Eijkhout 2024

Summary: Kokkos install, new setup

# Give the package a base name
%define pkg_base_name kokkos
%define MODULE_VAR    KOKKOS

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 5
%define micro_version 01

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc

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

Release:   5%{?dist}
License:   BSD-like
Group:     Development/Numerical-Libraries
URL:       https://github.com/kokkos/kokkos
Packager:  TACC - eijkhout@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tgz

# Turn off debug package mode
%define debug_package %{nil}
%define _build_id_links none
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: Kokkos local binary install
Group: System Environment/Base
%description modulefile
This is the long description for the modulefile RPM...

%description
Kokkos is a portal CPU/GPU programming model

#---------------------------------------
%prep
#---------------------------------------

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
## %include mpi-defines.inc
## module purge
%include compiler-load.inc
echo "loaded gnu compiler CXX=`which g++`"

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

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

pushd ${VICTOR}/makefiles/kokkos

module load cmake

## get rid of that PACKAGEROOT
make cpu JCOUNT=10 \
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

  rm -rf /tmp/build-${pkg_version}*

umount %{INSTALL_DIR}
  
%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}-omp.lua 

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

# ########################################
# ## Fix Modulefile During Post Install ##
# ########################################
# %post %{PACKAGE}
# export PACKAGE_POST=1
# %include post-defines.inc
# %post %{MODULEFILE}
# export MODULEFILE_POST=1
# %include post-defines.inc
# %preun %{PACKAGE}
# export PACKAGE_PREUN=1
# %include post-defines.inc
# ########################################
# ############ Do Not Remove #############
# ########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Mar 13 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 5: adding sycl
* Fri Aug 16 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: 4.4.00
* Mon Jan 29 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 3 : omp & cuda versions
* Tue Oct 03 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: version 4, new spec make structure
* Fri Apr 01 2022 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
