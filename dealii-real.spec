Summary: Dealii install

# https://www.dealii.org/9.1.1/readme.html

# Give the package a base name
%define pkg_base_name dealii
%define MODULE_VAR    DEALII

# Create some macros (spec file variables)
%define major_version 9
%define minor_version 5
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%define use_petsc 1
## petsc 3.11 has been compiled with impi: release instead of release_mt
%define dealiipetscversion 3.20
## as of petsc 3.15 slepc is rolled into petsc
%define explicit_slepc 0
%define python_version 3
# for gcc explicit python
%define python_module 3.8.2

%define use_trilinos 1
%define dealiitrilinosversion 12.18.1

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
License: GPLv2
Group: Development/Numerical-Libraries
Source: %{pkg_base_name}-%{pkg_version}.tgz
URL: http://www.dealii.org/
Vendor: TAMU
Packager: TACC -- eijkhout@tacc.utexas.edu

%define debug_package %{nil}
%define _build_id_links none
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Dealii is an open source finite element package
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: Dealii is an open source finite element package
Group: Development/Numerical-Libraries

%description
%description %{PACKAGE}
The main aim of deal.II is to enable rapid development of modern
finite element codes, using among other aspects adaptive meshes and a
wide array of tools classes often used in finite element
program. Writing such programs is a non-trivial task, and successful
programs tend to become very large and complex. We believe that this
is best done using a program library that takes care of the details of
grid handling and refinement, handling of degrees of freedom, input of
meshes and output of results in graphics formats, and the
like. Likewise, support for several space dimensions at once is
included in a way such that programs can be written independent of the
space dimension without unreasonable penalties on run-time and memory
consumption.

%description %{MODULEFILE}
The main aim of deal.II is to enable rapid development of modern
finite element codes, using among other aspects adaptive meshes and a
wide array of tools classes often used in finite element
program. Writing such programs is a non-trivial task, and successful
programs tend to become very large and complex. We believe that this
is best done using a program library that takes care of the details of
grid handling and refinement, handling of degrees of freedom, input of
meshes and output of results in graphics formats, and the
like. Likewise, support for several space dimensions at once is
included in a way such that programs can be written independent of the
space dimension without unreasonable penalties on run-time and memory
consumption.

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
%include compiler-load.inc
%include mpi-load.inc

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
  
module load cmake python3
## %{python_version}/%{python_module}
module load boost gsl metis p4est
module load mumps netcdf phdf5
module load petsc/%{dealiipetscversion}
module load trilinos/%{dealiitrilinosversion}
module list

####
#### MKL
####
%if "%{comp_fam}" == "gcc"
  module load mkl
%else
  export MKLFLAG="-mkl"
%endif

##
## TBBROOT
##
# %if "%{comp_fam}" == "gcc"
#   export TACC_INTEL_DIR=/opt/intel/compilers_and_libraries_2019.5.281/linux
#   if [ ! -d ${TACC_INTEL_DIR} ] ; then 
#       echo "Invalid TACC_INTEL_DIR: ${TACC_INTEL_DIR}" ; exit 1
#   fi
#   export TBBROOT=${TACC_INTEL_DIR}/tbb
# %endif

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}
    export SRCPATH=`pwd`
    export VICTOR=/admin/build/admin/rpms/frontera/SPECS/victor_scripts
    export MAKEINCLUDES=${VICTOR}/make-support-files

    pushd ${VICTOR}/makefiles/%{pkg_base_name}

    ## get rid of that PACKAGEROOT
    make real JCOUNT=20 \
	HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
	PACKAGEVERSION=%{pkg_version} \
	PACKAGEROOT=/tmp \
	SRCPATH=${SRCPATH} \
	INSTALLPATH=%{INSTALL_DIR} \
	MODULEDIRSET=$RPM_BUILD_ROOT/%{MODULE_DIR}

    popd

    cp -r %{INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/

umount %{INSTALL_DIR} # tmpfs # $INSTALL_DIR

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
# release 4: adding boost-mpi dependency
* Tue Feb 06 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release of 9.5.0 under new setup
