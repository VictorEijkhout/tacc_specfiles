Summary: Mfem install

# Give the package a base name
%define pkg_base_name mfem
%define MODULE_VAR    MFEM

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 8
# define micro_version 1

%define pkg_version %{major_version}.%{minor_version}
# {micro_version}

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

%include cuda-defines.inc

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

Release: 5
License: GPL
Vendor: https://github.com/ornladios/MFEM
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{pkg_version}.tgz

%define debug_package %{nil}
%define _build_id_links none
## global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}-gpu
Summary: Mfem local binary install
Group: System Environment/Base
%package %{MODULEFILE}-gpu
Summary: Mfem local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}-gpu
Forest support library
%description %{MODULEFILE}-gpu
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

export MFEM_DIR=`pwd`

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

pushd ${VICTOR}/makefiles/%{pkg_base_name}

module -t list | sort | tr '\n' ' '
module --latest load cmake 
module load petsc phdf5 hypre metis adios2
if [ "${TACC_SYSTEM}" = "vista" ] ; then
    module load nvpl
else
    if [ "${TACC_FAMILY_COMPILER}" = "gcc" ] ; then 
	module load mkl
    else
	export MKLFLAG="-mkl"
    fi
fi
module load cuda
module -t list | sort | tr '\n' ' '

    ## get rid of that PACKAGEROOT
    make default_install JCOUNT=20 \
	HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
	PACKAGEVERSION=%{pkg_version} \
	PACKAGEROOT=/tmp \
    BUILDDIRROOT=/tmp \
	SRCPATH=${SRCPATH} \
	INSTALLPATH=%{INSTALL_DIR} \
	MODULEDIRSET=$RPM_BUILD_ROOT/%{MODULE_DIR}

    popd

    ################ end of new stuff

    cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
    ## cp -r doc src test $RPM_BUILD_ROOT/%{INSTALL_DIR}/

  rm -rf /tmp/build-${pkg_version}*

umount %{INSTALL_DIR}

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

%files %{PACKAGE}-gpu
  %defattr(0644,root,root,0755)
  %{INSTALL_DIR}

%files %{MODULEFILE}-gpu
  %defattr(0644,root,root,0755)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Apr 13 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 5: 4.8
* Tue Nov 26 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: install mishap
* Sat Nov 23 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: keep in sync cpu/gpu
* Thu Nov 14 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: remake for hdf5 dependency
* Thu Sep 26 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 1 : first release 
