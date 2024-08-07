#
# Victor Eijkhout
#

Summary: A Nice little relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name fftw3
%define MODULE_VAR    FFTW3

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 3
%define micro_version 10

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
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

Release:   9%{?dist}
License:   GPL
Group:     System Environment/Base
URL:       http://www.fftw.org
Packager:  eijkhout@tacc.utexas.edu
# used to be cyrus
Source:    fftw-%{pkg_version}.tar.gz


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
FFTW is a C subroutine library for computing the discrete Fourier transform
(DFT) in one or more dimensions, of arbitrary input size, and of both real and
complex data (as well as of even/odd data, i.e. the discrete cosine/sine
transforms or DCT/DST). 

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
FFTW is a C subroutine library for computing the discrete Fourier transform
(DFT) in one or more dimensions, of arbitrary input size, and of both real and
complex data (as well as of even/odd data, i.e. the discrete cosine/sine
transforms or DCT/DST). 

%description
FFTW is a C subroutine library for computing the discrete Fourier transform
(DFT) in one or more dimensions, of arbitrary input size, and of both real and
complex data (as well as of even/odd data, i.e. the discrete cosine/sine
transforms or DCT/DST). 

#---------------------------------------
%prep
#---------------------------------------

%define debug_package %{nil}
%define _build_id_links none


#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# note: fftw, not pgk_base_name
%setup -n fftw-%{pkg_version}

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
# Load MPI Library
%include mpi-load.inc

# Insert further module commands

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

  #========================================
  # Insert Build/Install Instructions Here
  #========================================


mkdir -p %{INSTALL_DIR}
rm -rf %{INSTALL_DIR}/*
mount -t tmpfs tmpfs %{INSTALL_DIR}

################ new stuff

module load cmake
export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/victor_scripts
export MAKEINCLUDES=${VICTOR}/make-support-files

pushd ${VICTOR}/makefiles/%{pkg_base_name}

## get rid of that PACKAGEROOT
make single double JCOUNT=10 \
    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
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
%endif
# BUILD_PACKAGE |
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
  %endif
  # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(-,root,install,)
  %{INSTALL_DIR}

#-----------------------
  %endif
  # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 
#---------------------------

  %defattr(-,root,install,)
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

%changelog
* Wed Aug 07 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 9: single really fixed.
* Mon Aug 05 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 8: restore single
* Thu Aug 01 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 7: cmake prefix path
* Wed Oct 04 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 6: adding single precision
* Thu Sep 28 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 5: adding pkgconfig, moving to home1apps
* Mon May 15 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: new module setup
* Thu Jul 19 2022 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: up to 3.3.10, module now does prepend instead of append
* Mon Jul 13 2020 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: rebuild with new maintainer, latest intel 19

