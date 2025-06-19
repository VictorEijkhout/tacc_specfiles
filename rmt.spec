#
# Victor Eijkhout
#
# ./build_rpm.sh -g91 -j19_9 -l rmt
# ./build_rpm.sh -g132 -j21_9 -l rmt
# ./build_rpm.sh -i191 -j19_9 -l rmt
# ./build_rpm.sh -i231 -j21_9 -l rmt
#

Summary: A Nice little relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name rmt
%define MODULE_VAR    RMT

# Create some macros (spec file variables)
%define major_version git20231121
## %define minor_version 3
## %define micro_version 10

%define pkg_version %{major_version}
##.%{minor_version}.%{micro_version}

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

Release:   6%{?dist}
License:   GPL
Group:     System Environment/Base
URL:       https://gitlab.com/Uk-amor/RMT
Packager:  eijkhout@tacc.utexas.edu
# used to be cyrus
Source:    rmt-%{pkg_version}.tgz


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
RMT (R-matrix with time-dependence) is part of the UK-AMOR suite of codes for tackling problems in Atomic Molecular and Optical physics problems with the Rmatrix approach.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
RMT (R-matrix with time-dependence) is part of the UK-AMOR suite of codes for tackling problems in Atomic Molecular and Optical physics problems with the Rmatrix approach.

%description
RMT (R-matrix with time-dependence) is part of the UK-AMOR suite of codes for tackling problems in Atomic Molecular and Optical physics problems with the Rmatrix approach.

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

%setup -n rmt-git

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

module --latest load cmake
if [ "${TACC_SYSTEM}" = "vista" ] ; then
    module load nvpl
else
    if [ "${TACC_FAMILHY_COMPILER}" = "gcc" ] ; then 
	module load mkl
    else
	export MKLFLAG="-mkl"
    fi
fi

export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export MAKEINCLUDES=${VICTOR}/make-support-files

pushd ${VICTOR}/makefiles/rmt

## get rid of that PACKAGEROOT
make default_install JCOUNT=10 \
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
* Wed Oct 04 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: first build


