####
#### FROM FRONTERA, NEEDS ADAPTING
####

#
# Spec file for SUPERLU_SEQ:
# Sequential version of SuperLU
# (needed for Trilinos, as opposed to PETSc which needs distributed.)
#
# Victor Eijkhout, 2017

Summary:    Set of tools for manipulating geographic and Cartesian data sets

# Give the package a base name
%define pkg_base_name superlu_seq
%define MODULE_VAR    SUPERLUSEQ

# Create some macros (spec file variables)
%define major_version 5
%define minor_version 3
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
## being sequential this does not use MPI
#%include mpi-defines.inc
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

Release:   8%{?dist}
License:   GNU
Group: Development/Numerical-Libraries
Vendor:     Argonne National Lab
Group:      Libraries/maps
Source:	    superlu_seq-%{version}.tar.gz
URL:	    http://crd-legacy.lbl.gov/~xiaoye/SuperLU/
Packager:   eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define _build_id_links none
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

# Prevent weird relocation type 42 error
# . parsimonious solution: use the correct strip
# https://bugzilla.redhat.com/show_bug.cgi?id=1545386
# https://stackoverflow.com/questions/48706962/unresolvable-r-x86-64-none-relocation
%if 0%{?scl:1}
%define __strip %{_bindir}/strip
%endif
# . better? not strip at all
%undefine __brp_strip_static_archive

%package %{PACKAGE}
Summary: SUPERLUSEQ is a single processor sparse direct solver
Group: Libraries
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: SUPERLUSEQ is a single processor sparse direct solver
Group: Libraries
%description modulefile
This is the long description for the modulefile RPM...

%description
Summary: SUPERLUSEQ is a single processor sparse direct solver
Group: Libraries


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_version}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

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
# Load Compiler
%include compiler-load.inc
# Load MPI Library
#%include mpi-load.inc

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
  
#
# Use mount temp trick
#
mkdir -p             %{INSTALL_DIR}
mkdir -p ${RPM_BUILD_ROOT}/%{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}
export SLU_INSTALLATION=%{INSTALL_DIR}

#
# make a copy of the source tree in which to build
# (later try doing everything in BUILD?)
#
export SLU_SRC=/tmp/superlu-build
rm -rf ${SLU_SRC}
mkdir -p ${SLU_SRC}
cp -r * ${SLU_SRC}
## cp %{SPEC_DIR}/superlu_seq-%{version}.inc ${SLU_SRC}/make.inc
pushd ${SLU_SRC} # place for cmake crap

mkdir build
cd build

#
# config/make
#
%if "%{is_intel}" == "1"
  export CC=icc
  export CXX=icpc
  export FC=ifort
  export CFLAGS="-mkl -O2 -fPIC"
  export LOADOPTS=-mkl
%endif
%if "%{is_gcc}" == "1"
  module load mkl
  # /opt/intel/compilers_and_libraries_2017.4.196/linux/mkl/lib/intel64
  export CC="gcc"
  export CXX=g++
  export FC="gfortran"
  export CFLAGS="-g -O2 -fPIC"
%endif

ls $PKG_CONFIG_PATH
module --latest load cmake
cmake \
    -D CMAKE_INSTALL_PREFIX:PATH="${SLU_INSTALLATION}" \
    -D CMAKE_BUILD_TYPE:STRING=RELEASE \
    -D enable_internal_blaslib=OFF \
    -D TPL_BLAS_LIBRARIES="-mkl" \
    ${SLU_SRC}

make && make install

popd # from /tmp back to BUILD
cp -r %{INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/
  rm -rf /tmp/build-${pkg_version}*

umount %{INSTALL_DIR}

#-----------------------  
%endif # BUILD_PACKAGE |
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
  
# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
Module %{name} loads environmental variables defining
the location of SUPERLUSEQ directory, libraries, and binaries:
TACC_SUPERLUSEQ_DIR TACC_SUPERLUSEQ_LIB TACC_SUPERLUSEQ_BIN

Version: %{version}
]] )

whatis( "SUPERLUSEQ" )
whatis( "Version: %{version}" )
whatis( "Category: system, development" )
whatis( "Keywords: System, Cartesian Grids" )
whatis( "Description: Supernodal LU factorization" )
whatis( "URL: http://crd-legacy.lbl.gov/~xiaoye/SuperLU/" )

local version =  "%{version}"
local superlu_seq_dir =  "%{INSTALL_DIR}"

setenv("TACC_SUPERLUSEQ_DIR",superlu_seq_dir)
-- setenv("TACC_SUPERLUSEQ_BIN",pathJoin( superlu_seq_dir,"bin" ) )
setenv("TACC_SUPERLUSEQ_INC",pathJoin( superlu_seq_dir,"include" ) )
setenv("TACC_SUPERLUSEQ_LIB",pathJoin( superlu_seq_dir,"lib64" ) )
setenv("TACC_SUPERLUSEQ_SHARE",pathJoin( superlu_seq_dir,"share" ) )

prepend_path ("PATH",pathJoin( superlu_seq_dir,"share" ) )
-- prepend_path ("PATH",pathJoin( superlu_seq_dir,"bin" ) )
prepend_path ("LD_LIBRARY_PATH",pathJoin( superlu_seq_dir, "lib64" ) )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for %{name} version %{version}
##
set ModulesVersion "%version"
EOF

  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
  %endif

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
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
* Fri Nov 11 2022 eijkhout <eijkhout@tacc.utexas.edu>
- release 8: up to 5.3.0, cmake support
* Wed Feb 13 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 7: let's try to get that strip correct
* Tue Aug 28 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 6: just to disambiguate for intel18
* Wed Jul 18 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 5: TACC_SUPERLU_LIB: lib -> lib64
* Tue Apr 03 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: using cmake
* Mon Mar 12 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: fPIC really fixed
* Tue Feb 13 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: fPIC option
* Sat Jan 20 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
