# KOKKOS specfile
# Victor Eijkhout 2018


Summary: Kokkos, piggybacking on the PETSc install

# Give the package a base name
%define pkg_base_name kokkos
%define MODULE_VAR    KOKKOS

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 1
%define micro_version 00

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc
#%include name-defines-hidden.inc
#%include name-defines-noreloc.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1%{?dist}
License:   BSD-like
Group:     Development/Numerical-Libraries
URL:       http://graal.ens-lyon.fr/KOKKOS/
Packager:  TACC - eijkhout@tacc.utexas.edu
#Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define _build_id_links none
%define dbg           %{nil}


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
Kokkos is a solver library for distributed sparse linear system.

#---------------------------------------
%prep
#---------------------------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc
module purge

%include compiler-load.inc

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
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
rm -rf %{INSTALL_DIR}/*
mount -t tmpfs tmpfs %{INSTALL_DIR}

## no prereqs
## module load 

################ new stuff

export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/stampede3/SPECS/victor_scripts
export MAKEINCLUDES=${VICTOR}/make-support-files

pushd ${VICTOR}/makefiles/zlib

## get rid of that PACKAGEROOT
make configure build JCOUNT=10 \
    HOMEDIR=/admin/build/admin/rpms/stampede3/SOURCES \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIRSET=$RPM_BUILD_ROOT/%{MODULE_DIR}

popd

################ end of new stuff

  # Copy installation from tmpfs to RPM directory
  ls %{INSTALL_DIR}
  cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/

umount %{INSTALL_DIR}
  
ls $RPM_BUILD_ROOT/%{INSTALL_DIR}/

#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################
  
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 
#---------------------------

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

########################################
## Fix Modulefile During Post Install ##
########################################
%post %{PACKAGE}
export PACKAGE_POST=1
%include post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Oct 03 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: version 4, new spec make structure
* Fri Apr 01 2022 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
