Summary: Netcdf install

# Give the package a base name
%define pkg_base_name netcdf
%define MODULE_VAR    NETCDF

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 9
%define micro_version 2

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
## corresponding fortran version
%define pkgf_version 4.6.1

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
Vendor: https://github.com/Unidata/netcdf
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{pkg_version}.tgz

%define debug_package %{nil}
%define _build_id_links none
## global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: Netcdf local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Netcdf local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
Forest support library
%description %{MODULEFILE}
Forest support library

%prep

%setup -n netcdf-%{version}

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

module load cmake
module load hdf5
#/1.14

##
## first install the C version
##
pushd ${VICTOR}/makefiles/%{pkg_base_name}

## get rid of that PACKAGEROOT
make \
    seq JCOUNT=10 \
    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIRSET=%{MODULE_DIR}

popd

##
## now install the Fortran version
##
tar fxz /admin/build/admin/rpms/frontera/SOURCES/netcdf-fortran-%{pkgf_version}.tgz
pushd ${VICTOR}/makefiles/netcdff

NETCDF_MODDIR=%{MODULE_DIR}/../
echo "Is there a netcdf module in <<${NETCDF_MODDIR}>> ?"
ls ${NETCDF_MODDIR}
ls ${NETCDF_MODDIR}/netcdf
# should we use the module dir, not in build root?
module use $RPM_BUILD_ROOT/%{MODULE_DIR}/../
module load netcdf/%{pkg_version}

make \
    seq JCOUNT=10 \
    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    PACKAGE=netcdf-fortran PACKAGEVERSION=%{pkgf_version} NOMODULE=1 \
    PACKAGEROOT=/tmp \
    SRCPATH=${SRCPATH}/netcdf-fortran-%{pkgf_version} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIRSET=%{MODULE_DIR}

popd

################ end of new stuff

cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
## cp -r doc src test $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r %{MODULE_DIR}/* $RPM_BUILD_ROOT/%{MODULE_DIR}/

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
* Wed Oct 30 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 5: trying to fix fortran
* Thu Aug 22 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: C and Fortran versions
* Wed Jan 13 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: hdf5 version is going up
* Tue Jan 09 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 2 : seq and par separated out
