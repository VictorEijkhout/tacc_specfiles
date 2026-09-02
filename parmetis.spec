Summary: Parmetis install

# Give the package a base name
%define pkg_base_name parmetis
%define MODULE_VAR    PPARMETIS

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 0
%define micro_version 3

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

Release: 4
License: GPL
Vendor: https://github.com/scibuilder/parmetis
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{pkg_version}.tgz

%define debug_package %{nil}
%define _build_id_links none
## global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

# new horizon settings
%global __brp_check_rpaths %{nil}
%define __brp_mangle_shebangs %{nil}
%undefine _annotated_build
%global build_cflags   -O2
%global build_cxxflags -O2
%global build_fflags   -O2
%global build_ldflags  %{nil}


%package %{PACKAGE}
Summary: Parmetis local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Parmetis local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
Forest support library
%description %{MODULEFILE}
Forest support library

%prep

%setup -n %{pkg_base_name}-%{version}

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

export PARMETIS_DIR=`pwd`

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
  
export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/RPMtheNextGeneration
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/RPMtheNextGeneration
export MAKEINCLUDES=${VICTOR}/make-support-files

module --latest load cmake

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

LS6 module load python/3.12
export PATH=/admin/build/admin/rpms/frontera/SPECS/RPMtheNextGeneration/MrPackMod:${PATH}
export PYTHONPATH=/admin/build/admin/rpms/frontera/SPECS/RPMtheNextGeneration:${PYTHONPATH}

pushd ${VICTOR}/makefiles/%{pkg_base_name}

HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    BUILDDIRROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIR=$RPM_BUILD_ROOT/%{MODULE_DIR} \
mpm.py -t -j 20 install

popd

################ end of new stuff

chmod -R g+rX,o+rX %{INSTALL_DIR}
cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
## cp -r doc src test $RPM_BUILD_ROOT/%{INSTALL_DIR}/

rm -rf /tmp/build-${pkg_version}*

umount %{INSTALL_DIR}

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

%files %{PACKAGE}
  %defattr(-,root,install,-)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(-,root,install,-)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Sep 01 2026 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: defattr root,install
* Mon Jul 27 2026 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: use mpm
* Wed Feb 07 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 2 : just to be sure
* Thu Nov 30 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 1 : initial install with this structure
