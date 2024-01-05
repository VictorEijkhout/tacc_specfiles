Summary: Netcdf install

# ./build_rpm.sh -i231 -j21_9 -l netcdf-new
# ./build_rpm.sh -i191 -j19_9 -l netcdf-new
# ./build_rpm.sh -g91 -j19_9 -l netcdf-new

# Give the package a base name
%define pkg_base_name netcdf
%define MODULE_VAR    NETCDF

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 9
%define micro_version 2

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

Release: 1%{?dist}
License: GPL
Vendor: https://github.com/cburstedde/netcdf
#Source1: netcdf-setup.sh
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: netcdf-%{pkg_version}.tgz

%define debug_package %{nil}
%define _build_id_links none
## %global _missing_build_ids_terminate_build 0
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
%include mpi-defines.inc
module purge
%include compiler-load.inc
%include mpi-load.inc

export NETCDF_DIR=`pwd`

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

pushd ${VICTOR}/makefiles/%{pkg_base_name}

module load cmake
module load phdf5/1.14
env | grep HDF5_

## get rid of that PACKAGEROOT
make configure build JCOUNT=10 \
    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIRSET=$RPM_BUILD_ROOT/%{MODULE_DIR}

popd

################ end of new stuff

cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
## cp -r doc src test $RPM_BUILD_ROOT/%{INSTALL_DIR}/

umount %{INSTALL_DIR}

# cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
# help( [[
# The NETCDF modulefile defines the following environment variables:
# TACC_NETCDF_DIR, TACC_NETCDF_LIB, and TACC_NETCDF_INC 
# for the location of the NETCDF %{version} distribution, 
# libraries, and include files, respectively.

# Version %{pkg_version}
# ]] )

# whatis( "Name: Netcdf 'p4-est of octrees'" )
# whatis( "Version: %{version}-${ext}" )
# whatis( "Version-notes: ${netcdfversion}" )
# whatis( "Category: library, mathematics" )
# whatis( "URL: https://github.com/cburstedde/netcdf" )
# whatis( "Description: octree support for dealii" )

# local             netcdf_dir =     "%{INSTALL_DIR}"

# prepend_path("LD_LIBRARY_PATH", pathJoin(netcdf_dir,"lib") )
# prepend_path("PATH", pathJoin(netcdf_dir,"bin") )

# setenv(          "NETCDF_DIR",             netcdf_dir)
# setenv(          "TACC_NETCDF_DIR",        netcdf_dir)
# setenv(          "TACC_NETCDF_BIN",        pathJoin(netcdf_dir,"bin"))
# setenv(          "TACC_NETCDF_INC",        pathJoin(netcdf_dir,"include"))
# setenv(          "TACC_NETCDF_LIB",        pathJoin(netcdf_dir,"lib"))

# EOF

# cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${version} << EOF
# #%Module1.0#################################################
# ##
# ## version file for Netcdf %version
# ##

# set     ModulesVersion      "${modulefilename}"
# EOF

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
* Tue Mar 21 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 1 using new makefile structure
