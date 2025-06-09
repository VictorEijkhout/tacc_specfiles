#
# Boost by Victor, as opposed to Si Liu
#
Summary: Boost install

# Give the package a base name
%define pkg_base_name boost
%define MODULE_VAR    BOOST

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 86
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%include rpm-dir.inc
%include compiler-defines.inc
## %include mpi-defines.inc

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

Release: 8%{?dist}
License: GPL
Vendor: https://github.com/cburstedde/boost
#Source1: boost-setup.sh
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{version}.tgz

%define debug_package %{nil}
%define _build_id_links none
## global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: Boost local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Boost local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
Forest support library
%description %{MODULEFILE}
Forest support library

%prep

%setup -n boost-%{version}

#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc
%include compiler-defines.inc
## %include mpi-defines.inc
module purge
%include compiler-load.inc
## %include mpi-load.inc

export BOOST_DIR=`pwd`

#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

# %if "%{comp_fam}" == "gcc"
#   module load mkl
#   export BLASOPTIONS="-Wl,--start-group $MKLROOT/lib/intel64/libmkl_intel_lp64.so $MKLROOT/lib/intel64/libmkl_sequential.so $MKLROOT/lib/intel64/libmkl_core.so -Wl,--end-group -lpthread -lm"
#   export BLASFLAG=
# %else
#   export BLASOPTIONS=
#   export BLASFLAG=-mkl
# %endif

################ new stuff

export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export MAKEINCLUDES=${VICTOR}/make-support-files

pushd ${VICTOR}/makefiles/%{pkg_base_name}

## get rid of that PACKAGEROOT
make configure build JCOUNT=10 \
    $( if [ "${TACC_FAMILY_COMPILER}" = "nvidia" ] ; then echo TOOLSET=pgi ; fi ) \
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
## cp -r doc example src test $RPM_BUILD_ROOT/%{INSTALL_DIR}/

  rm -rf /tmp/build-${pkg_version}*

umount %{INSTALL_DIR}

# cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${version} << EOF
# #%Module1.0#################################################
# ##
# ## version file for Boost %version
# ##

# set     ModulesVersion      "${modulefilename}"
# EOF

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
* Mon Sep 16 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 8: 1.86
* Tue Aug 13 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 7: nvidia uses pgi toolset
* Mon Apr 15 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 6: finally using correct compiler
* Wed Apr 03 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 5: adding graphviz
* Tue Mar 26 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: adding serialization
* Mon Mar 04 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: up to 1.84, adding system
* Fri Jan 05 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 2 : up to 1.83
* Tue Mar 21 2023 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release 1.81.0
