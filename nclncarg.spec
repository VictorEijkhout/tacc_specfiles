#
# nclncarg.spec
# Victor Eijkhout
#

Summary: Nclncarg

# Give the package a base name
%define pkg_base_name nclncarg
%define MODULE_VAR    NCLNCARG

# Create some macros (spec file variables)
%define major_version git2024
## define minor_version 3
## define micro_version 1

%define pkg_version %{major_version}
## {minor_version} 
## {minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc

########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc-home1.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1
License:   BSD
Group:     Development/Tools
URL:       https://github.com/madler/nclncarg
Packager:  TACC - eijkhout@tacc.utexas.edu
Source0:    %{pkg_base_name}-%{pkg_version}.tgz
Source1:    ncl_gcc.sh
Source2:    nclncarg_configure.sh

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%define _build_id_links none

%package %{PACKAGE}
Summary: Nclncarg
Group: Support
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: Nclncarg
Group: Support
%description modulefile
Nclncarg

%description
Nclncarg


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_version}

export CC=${TACC_CC}
export CFLAGS="-O2 -ansi -std=c99 -fopenmp -fPIC"
export CCOPTIONS="-O2 -ansi -std=c99 -fopenmp -fPIC"

export CXX=${TACC_CXX}
export CXXFLAGS="-O2 -ansi -std=c99 -fopenmp -fPIC"
export CPPFLAGS="-DNDEBUG"

export FC=${TACC_FC}
export FFLAGS="-O2 -fPIC -fopenmp -fallow-argument-mismatch"

export F90=${TACC_FC}
export F90FLAGS="-O2 -fPIC -fopenmp -fallow-argument-mismatch"

export NCARG=$(pwd)

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

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
# Load Compiler
%include compiler-load.inc

# Insert further module commands

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
  
module load hdf5/1.10 netcdf/4.9.1 udunits

mkdir -p %{INSTALL_DIR}
rm -rf %{INSTALL_DIR}/*
mount -t tmpfs tmpfs %{INSTALL_DIR}

##
## For once we spell it out
##
if [ ! -d ngmath ] ; then
    echo "We are not in the source directory" && exit 1
fi
make clean || echo >/dev/null
source ncl_${TACC_CC}.sh
export NCARG=${pwd}
echo "Creating local configuration"
./nclncarg_configure.sh
echo "Making"
make Everything


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
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
  %endif

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

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

#---------------------------------------
%changelog
#---------------------------------------
#
* Tue May 28 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
