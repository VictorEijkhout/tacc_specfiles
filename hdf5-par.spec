# HDF5 parallel install
# Victor Eijkhout 2024

Summary: Hdf5 install

# Give the package a base name
%define pkg_base_name phdf5
%define MODULE_VAR    PHDF5

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 0
%define micro_version 0

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
#Source1: hdf5-setup.sh
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: hdf5-%{pkg_version}.tgz

%define debug_package %{nil}
%define _build_id_links none
## global _missing_build_ids_terminate_build 0
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
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export MAKEINCLUDES=${VICTOR}/make-support-files

## fixed in nvidia 25.5
# if [ "${TACC_SYSTEM}" = "vista" ] ; then
#     ${VICTOR}/makefiles/hdf5/vista_fix.sh
# fi

pushd ${VICTOR}/makefiles/hdf5

module -t list | sort | tr '\n' ' '
module --latest load cmake
module load zlib
module -t list | sort | tr '\n' ' '

export PATH=/admin/build/admin/rpms/frontera/SPECS/rpmtng/MrPackMod:${PATH}
export PYTHONPATH=/admin/build/admin/rpms/frontera/SPECS/rpmtng:${PYTHONPATH}

## get rid of that PACKAGEROOT
##
## Vista nvidia has a problem with Fortran:
## HDFFORTRAN=off
##
HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    $( if [ "${TACC_FAMILY_COMPILER}" = "nvidia" ] ; then echo TESTING=OFF ; fi ) \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    BUILDDIRROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIR=$RPM_BUILD_ROOT/%{MODULE_DIR} \
mpm.py -t -j 20 -c Configuration.seq install

popd

################ end of new stuff

cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/

rm -rf /tmp/build-${pkg_version}*

umount %{INSTALL_DIR}

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 
  %endif

#--------------------------
%endif 
# BUILD_MODULEFILE |
#--------------------------


%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Dec 10 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: module version fix
* Fri Nov 21 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 1 : reset to 1 for v2
