Summary: Siesta install

# Give the package a base name
%define pkg_base_name siesta
%define MODULE_VAR    SIESTA

# Create some macros (spec file variables)
%define major_version 5
%define minor_version 4
%define micro_version 1
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

Release: 5
License: GPL
Vendor: https://github.com/cburstedde/siesta
#Source1: siesta-setup.sh
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{pkg_version}.tgz

%define debug_package %{nil}
%define _build_id_links none
## global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: Siesta local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Siesta local binary install
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

#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export MAKEINCLUDES=${VICTOR}/make-support-files

##
## the follwing edits are needed for Frontera
## I'm guessing they don't hurt to apply in general
##
  # GIT_REPOSITORY "https://gitlab.com/siesta-project/libraries/libfdf"
# sed -i ./Config/cmake/Modules/FindCustomlibfdf.cmake \
#     -e '/REPOSITORY/s?libfdf?libfdf.git?'

#   # GIT_REPOSITORY "https://gitlab.com/siesta-project/libraries/xmlf90"
# sed -i ./Config/cmake/Modules/FindCustomxmlf90.cmake \
#     -e '/REPOSITORY/s?xmlf90?xmlf90.git?'

#   # GIT_REPOSITORY "https://gitlab.com/siesta-project/libraries/libpsml"
# sed -i ./Config/cmake/Modules/FindCustomlibpsml.cmake \
#     -e '/REPOSITORY/s?libpsml?libpsml.git?'

#   # GIT_REPOSITORY "https://gitlab.com/siesta-project/libraries/libgridxc"
# sed -i ./Config/cmake/Modules/FindCustomLibGridxc.cmake \
#     -e '/REPOSITORY/s?libgridxc?libgridxc.git?'

pushd ${VICTOR}/makefiles/%{pkg_base_name}

module --latest load cmake
module load fftw3
if [ "${TACC_SYSTEM}" = "vista" ] ; then
    module load nvpl
else
    if [ "${TACC_FAMILY_COMPILER}" = "gcc" ] ; then 
	module load mkl
    else
	export MKLFLAG="-mkl"
    fi
fi

## get rid of that PACKAGEROOT
make configure build JCOUNT=10 \
    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    BUILDDIRROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIRSET=$RPM_BUILD_ROOT/%{MODULE_DIR}
rm -rf /tmp/%{pkg_base_name}

popd

################ end of new stuff

cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
## cp -r doc example src test $RPM_BUILD_ROOT/%{INSTALL_DIR}/
# popd

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
* Tue Sep 16 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 5: 5.4.0, add netcdf
* Tue Apr 29 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: 5.2.2 and fix ilp
* Mon Jan 06 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: 5.2.1 with wannier
* Sat Oct 19 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: added bin dir
* Thu Aug 01 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
