#
# zlib.spec
# Victor Eijkhout
#

Summary: Zlib

# Give the package a base name
%define pkg_base_name zlib
%define MODULE_VAR    ZLIB

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 3
%define micro_version 2

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
## .{minor_version}

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

Release:   3
License:   BSD
Group:     Development/Tools
URL:       https://github.com/madler/zlib
Packager:  TACC - eijkhout@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tgz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%define _build_id_links none

%package %{PACKAGE}
Summary: Zlib
Group: Support
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: Zlib
Group: Support
%description modulefile
Zlib

%description
Zlib


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
# BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
%endif 
# BUILD_MODULEFILE |
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
  
mkdir -p %{INSTALL_DIR}
rm -rf %{INSTALL_DIR}/*
mount -t tmpfs tmpfs %{INSTALL_DIR}

## no prereqs
## module load 

################ new stuff

export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export MAKEINCLUDES=${VICTOR}/make-support-files

LS6 module load python/3.12
export PATH=/admin/build/admin/rpms/frontera/SPECS/rpmtng/MrPackMod:${PATH}
export PYTHONPATH=/admin/build/admin/rpms/frontera/SPECS/rpmtng:${PYTHONPATH}

pushd ${VICTOR}/makefiles/zlib

HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    BUILDDIRROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIR=$RPM_BUILD_ROOT/%{MODULE_DIR} \
mpm.py -c Configuration -t -j 20 install

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
# BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
  %endif

#--------------------------
%endif 
# BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(0644,root,root,0755)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
%endif 
# BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 
#---------------------------

  %defattr(0644,root,root,0755)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

#--------------------------
%endif 
# BUILD_MODULEFILE |
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
* Tue Feb 17 2026 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: 1.3.2 with mpm
* Tue May 14 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: update to 1.3.1
* Mon May 15 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
