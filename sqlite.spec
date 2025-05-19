#
# sqlite.spec
# Victor Eijkhout
#

Summary: Interface Generator

# Give the package a base name
%define pkg_base_name sqlite
%define MODULE_VAR    SQLITE

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 49
%define micro_version 2

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
## .%{minor_version}

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

Release:   4
License:   BSD
Group:     Development/Tools
URL:       https://www.sqlite.org/
Packager:  TACC - eijkhout@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tgz

# Turn off debug package mode
%define debug_package %{nil}
%define _build_id_links none
%define dbg           %{nil}


%package %{PACKAGE}
Summary: Blas alternative
Group: Numerical library
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
ICL wrapper for C++ around BLAS

%description
ICL wrapper for C++ around BLAS


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
  
mkdir -p %{INSTALL_DIR}
rm -rf %{INSTALL_DIR}/*
mount -t tmpfs tmpfs %{INSTALL_DIR}

## module load

################ new stuff

export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/victor_scripts
export MAKEINCLUDES=${VICTOR}/make-support-files

pushd ${VICTOR}/makefiles/sqlite

## get rid of that PACKAGEROOT
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

  # Copy installation from tmpfs to RPM directory
  ls %{INSTALL_DIR}
  cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/

  rm -rf /tmp/build-${pkg_version}*

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
  
# # Write out the modulefile associated with the application
# cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
# local help_message = [[

# This module provides the SQLITE environment variables:
# TACC_SQLITE_DIR, TACC_SQLITE_LIB, TACC_SQLITE_INC

# There are examples programs in \$TACC_SQLITE_DIR/examples

# Version %{version}
# ]]

# help(help_message,"\n")

# whatis("Name: SQLITE")
# whatis("Version: %{version}")
# whatis("Category: ")
# whatis("Keywords: library, numerics, BLAS")
# whatis("URL: https://github.com/flame/sqlite")
# whatis("Description: BLAS-like Library Instantiation Software")

# local sqlite_dir="%{INSTALL_DIR}"

# setenv("TACC_SQLITE_DIR",sqlite_dir)
# setenv("TACC_SQLITE_LIB",pathJoin(sqlite_dir,"lib"))
# setenv("TACC_SQLITE_INC",pathJoin(sqlite_dir,"include"))

# append_path("LD_LIBRARY_PATH",pathJoin(sqlite_dir,"lib"))

# EOF
  
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
* Sun May 18 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: 3.49.2
* Tue Sep 17 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: 3.46.1
* Tue Sep 10 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: just because
* Mon Jun 12 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
