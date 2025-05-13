# Give the package a base name
%define pkg_base_name ncview
%define MODULE_VAR    NCVIEW

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 1
%define micro_version 9

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
#%include name-defines-hidden.inc
#%include name-defines-hidden-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

#
# Spec file for Ncview
#
Summary:   Ncview is a netcdf viewer
Release:   3%{?dist}
License:   GPL
Group:     applications/io
Source:    ncview-%{version}.tar.gz
URL:       http://meteora.ucsd.edu/~pierce/ncview_home_page.html
Distribution: RedHat Linux
Vendor:    Unidata Program Center, UCAR
Packager:  TACC - eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define _build_id_links none
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Ncview is a program for viewing NetCDF files
Group: applications/io

%package %{MODULEFILE}
Summary: Ncview is a program for viewing NetCDF files
Group: applications/io

%description
%description %{PACKAGE}
Ncview is a GUI viewer for NetCDF (network Common Data Form) files
%description %{MODULEFILE}
Ncview is a GUI viewer for NetCDF (network Common Data Form) files

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_version}

#-----------------------
%endif 
# BUILD_PACKAGE 
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
%endif 
# BUILD_MODULEFILE 
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
# Load Compiler
%include compiler-load.inc
# Load MPI Library
#%include mpi-load.inc

module load hdf5 netcdf udunits

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

mkdir -p %{INSTALL_DIR}
rm -rf %{INSTALL_DIR}/*
mount -t tmpfs tmpfs %{INSTALL_DIR}

################ new stuff

module --latest load cmake
module load hdf5 netcdf udunits
export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/victor_scripts
export MAKEINCLUDES=${VICTOR}/make-support-files

pushd ${VICTOR}/makefiles/%{pkg_base_name}

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
  
# Copy installation from tmpfs to RPM directory
ls %{INSTALL_DIR}
cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/

  rm -rf /tmp/build-${pkg_version}*

umount %{INSTALL_DIR}

ls $RPM_BUILD_ROOT/%{INSTALL_DIR}/

#-----------------------  
%endif 
# BUILD_PACKAGE 
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
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for Ncview
##
 
set     ModulesVersion      "%{version}"
EOF


# Check the syntax of the generated lua modulefile only if a visible module
%if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
%endif

#--------------------------
%endif 
# BUILD_MODULEFILE 
#--------------------------

#------------------------
%if %{?BUILD_PACKAGE}
%files %{PACKAGE}
#------------------------

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
%endif 
# BUILD_PACKAGE 
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files %{MODULEFILE} 
#---------------------------

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

#--------------------------
%endif 
# BUILD_MODULEFILE 
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

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Jan 23 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 3 : new structure
* Tue Aug 30 2022 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: unreleased, unnecessary
* Mon Jul 15 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: Initial build.
