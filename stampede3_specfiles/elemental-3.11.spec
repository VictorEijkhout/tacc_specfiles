# ELEMENTAL specfile
# Victor Eijkhout 2018
# version 3.11 corresponds to the petsc version
# we inherit from
#
# based on Bar.spec
# W. Cyrus Proctor
# Antonio Gomez
# 2015-08-25
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
# VERBOSE=1       -> Print detailed information at install time
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#
# Typical Command-Line Example:
# ./build_rpm.sh Bar.spec
# cd ../RPMS/x86_64
# rpm -i --relocate /tmprpm=/opt/apps Bar-package-1.1-1.x86_64.rpm
# rpm -i --relocate /tmpmod=/opt/apps Bar-modulefile-1.1-1.x86_64.rpm
# rpm -e Bar-package-1.1-1.x86_64 Bar-modulefile-1.1-1.x86_64

Summary: Elemental, piggybacking on the PETSc install

# Give the package a base name
%define pkg_base_name elemental
%define MODULE_VAR    ELEMENTAL

# Create some macros (spec file variables)
%define major_version 0
%define minor_version 87
%define micro_version xxx

%define pkg_version %{major_version}.%{minor_version}
%define petscversion 3.11
###%define NO_PACKAGE 0

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc
#%include name-defines-hidden.inc
#%include name-defines-noreloc.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1%{?dist}
License:   BSD-like
Group:     Development/Numerical-Libraries
URL:       http://graal.ens-lyon.fr/ELEMENTAL/
Packager:  TACC - eijkhout@tacc.utexas.edu
#Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define _build_id_links none
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: Elemental local binary install
Group: System Environment/Base
%description modulefile
This is the long description for the modulefile RPM...

%description
Elemental is a solver library for distributed sparse linear system.

#---------------------------------------
%prep
#---------------------------------------

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

%include compiler-load.inc
%include mpi-load.inc

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

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
  
##
## configure install loop
##
export dynamic="debug cxx cxxdebug complex complexdebug cxxcomplex cxxcomplexdebug "

for ext in \
  "" \
  ${dynamic} \
  ; do

echo "module file for ${ext}"

module unload petsc
if [ -z "${ext}" ] ; then
  export architecture=skylake
  module load petsc/%{petscversion}
else
  export architecture=skylake-${ext}
  module load petsc/%{petscversion}-${ext}
fi


##
## modulefile part of the configure install loop
##
if [ -z "${ext}" ] ; then
  export modulefilename=%{version}
else
  export modulefilename=%{version}-${ext}
fi

echo 
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF
help( [[
The Elemental module defines the following environment variables:
TACC_ELEMENTAL_INC and TACC_ELEMENTAL_LIB for the location
of the Elemental include files and libraries.

Version %{version}
]] )

whatis( "Name: Elemental" )
whatis( "Version: %{version}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://graal.ens-lyon.fr/ELEMENTAL/" )
whatis( "Description: Numerical library for sparse solvers" )

local             elemental_arch =    "${architecture}"
local             elemental_dir  =     "${TACC_PETSC_DIR}"
local             elemental_inc  = pathJoin(elemental_dir,elemental_arch,"include")
local             elemental_lib  = pathJoin(elemental_dir,elemental_arch,"lib")

prepend_path("LD_LIBRARY_PATH", elemental_lib)

setenv("TACC_ELEMENTAL_INC",        elemental_inc )
setenv("TACC_ELEMENTAL_LIB",        elemental_lib)
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Elemental %version
##

set     ModulesVersion      "${modulefilename}"
EOF

## %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua 

  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua
  %endif

##
## end of module file loop
##
done

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


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

%changelog
* Wed Jun 05 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release