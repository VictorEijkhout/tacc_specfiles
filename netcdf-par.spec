Summary: Netcdf install

# Give the package a base name
%define pkg_base_name parallelnetcdf
%define MODULE_VAR    PARALLELNETCDF

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 10
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define pkgf_version 4.6.1

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

Release: 7
License: GPL
Vendor: https://github.com/Unidata/netcdf
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: netcdf-%{pkg_version}.tgz

%define debug_package %{nil}
%define _build_id_links none
## global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: Netcdf local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Netcdf local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
Forest support library
%description %{MODULEFILE}
Forest support library

%prep

%setup -n netcdf-%{version}

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
#mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

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
  
module --latest load cmake
module load phdf5/1.14 pnetcdf
LS6 module load python/3.12
module -t list | sort | tr '\n' ' '

################ new stuff

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export MAKEINCLUDES=${VICTOR}/make-support-files

export PATH=/admin/build/admin/rpms/frontera/SPECS/rpmtng/MrPackMod:${PATH}
export PYTHONPATH=/admin/build/admin/rpms/frontera/SPECS/rpmtng:${PYTHONPATH}

##
## first install the C version
##
pushd ${VICTOR}/makefiles/netcdf

# module goes straight into rpm build root
HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    BUILDDIRROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIR=$RPM_BUILD_ROOT/%{MODULE_DIR} \
mpm.py -t -j 20 -c Configuration.par install

popd

##
## now install the Fortran version
##
tar fxz /admin/build/admin/rpms/frontera/SOURCES/netcdf-fortran-%{pkgf_version}.tgz
pushd ${VICTOR}/makefiles/netcdff

NETCDF_MODDIR=$RPM_BUILD_ROOT/%{MODULE_DIR}/../
# echo "Is there a netcdf module in <<${NETCDF_MODDIR}>> ?"
# ls ${NETCDF_MODDIR}
# ls ${NETCDF_MODDIR}/%{pkg_base_name}
module use ${NETCDF_MODDIR}
module load parallelnetcdf/%{pkg_version}

    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
	PACKAGE=parallelnetcdf PACKAGEVERSION=%{pkgf_version} NOMODULE=1 \
	PACKAGEROOT=/tmp \
	SRCPATH=${SRCPATH}/netcdf-fortran-%{pkgf_version} \
	INSTALLPATH=%{INSTALL_DIR} \
    mpm.py -t -j 20 -c Configuration.par configure build 

popd

################ end of new stuff

chmod -R g+rX,o+rX %{INSTALL_DIR}

cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
## cp -r doc src test $RPM_BUILD_ROOT/%{INSTALL_DIR}/

  rm -rf /tmp/build-${pkg_version}*

umount %{INSTALL_DIR}

# {SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

%files %{PACKAGE}
  %defattr(0644,root,root,0755)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(0644,root,root,0755)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun May 17 2026 eijkhout <eijkhout@tacc.utexas.edu>
- release 7 : 4.10, using mpm
* Tue Nov 26 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 6: rebuild for fortran module name
* Wed Oct 30 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 5: trying to fix fortran
* Wed Jan 10 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: hdf5 version is going up
* Tue Jan 09 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 2 : seq and par separated out
