Summary: Adios2 install

# Give the package a base name
%define pkg_base_name adios2
%define MODULE_VAR    ADIOS2

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 11
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

Release: 4
License: GPL
Vendor: https://github.com/ornladios/ADIOS2
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{pkg_version}.tgz

%define debug_package %{nil}
%define _build_id_links none
## global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: Adios2 local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Adios2 local binary install
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

export ADIOS2_DIR=`pwd`

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
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export MAKEINCLUDES=${VICTOR}/make-support-files

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

LS6 module load python/3.12
export PATH=/admin/build/admin/rpms/frontera/SPECS/rpmtng/MrPackMod:${PATH}
export PYTHONPATH=/admin/build/admin/rpms/frontera/SPECS/rpmtng:${PYTHONPATH}

pushd ${VICTOR}/makefiles/%{pkg_base_name}

module -t list | sort | tr '\n' ' '
module --latest load cmake 
module load phdf5
module -t list | sort | tr '\n' ' '

HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
       PACKAGEVERSION=%{pkg_version} \
       PACKAGEROOT=/tmp \
       BUILDDIRROOT=/tmp \
       SRCPATH=${SRCPATH} \
       INSTALLPATH=%{INSTALL_DIR} \
       MODULEDIR=$RPM_BUILD_ROOT/%{MODULE_DIR} \
mpm.py -c Configuration.cpu -t -j 20 install

popd

################ end of new stuff

chmod -R g+rX,o+rX %{INSTALL_DIR}/
cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r examples $RPM_BUILD_ROOT/%{INSTALL_DIR}/

rm -rf /tmp/build-${pkg_version}*

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
* Tue Feb 10 2026 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: using mpm
* Mon Jul 14 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: rebuild with fortran enabled
* Sat Nov 23 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: 2.10.2
* Thu Sep 26 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 1 : first release 

