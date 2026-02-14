Summary: Underworld install

# Give the package a base name
%define pkg_base_name underworld
%define MODULE_VAR    UNDERWORLD

# Create some macros (spec file variables)
%define major_version git20220106

%define pkg_version %{major_version}

# need petsc because mumps comes with Scotch/Scalapack/Metis/Parmetis baggage
%define petscversion 3.16
%define phdf5version 1.10.4
%define python_version 3.9.2
%define python_version_version 3.9

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
URL: https://github.com/underworld/Underworld
Vendor: Sandia National Labs
Packager: TACC -- eijkhout@tacc.utexas.edu

%define debug_package %{nil}
%define _build_id_links none
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Underworld is a large suite of numerical algorithms from Sandia National Laboratories
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: Underworld is a large suite of numerical algorithms from Sandia National Laboratories
Group: Development/Numerical-Libraries

%description
%description %{PACKAGE}
The Underworld Project is an effort to develop algorithms and enabling
technologies within an object-oriented software framework for the
solution of large-scale, complex multi-physics engineering and
scientific problems. A unique design feature of Underworld is its focus
on packages.

Each Underworld package is a self-contained, independent piece of
software with its own set of requirements, its own development team
and group of users. Because of this, Underworld itself is designed to
respect the autonomy of packages. Underworld offers a variety of ways
for a particular package to interact with other Underworld packages. It
also offers a set of tools that can assist package developers with
builds across multiple platforms, generating documentation and
regression testing across a set of target platforms. At the same time,
what a package must do to be called a Underworld package is minimal, and
varies with each package.
%description %{MODULEFILE}
The Underworld Project is an effort to develop algorithms and enabling
technologies within an object-oriented software framework for the
solution of large-scale, complex multi-physics engineering and
scientific problems. A unique design feature of Underworld is its focus
on packages.

Each Underworld package is a self-contained, independent piece of
software with its own set of requirements, its own development team
and group of users. Because of this, Underworld itself is designed to
respect the autonomy of packages. Underworld offers a variety of ways
for a particular package to interact with other Underworld packages. It
also offers a set of tools that can assist package developers with
builds across multiple platforms, generating documentation and
regression testing across a set of target platforms. At the same time,
what a package must do to be called a Underworld package is minimal, and
varies with each package.

%prep

%setup -n underworld-%{version}

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

module load phdf5/%{phdf5version} petsc/%{petscversion}-nohdf5
module load python3
echo $LD_LIBRARY_PATH


#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}
##cp -r * %{INSTALL_DIR}
##pushd %{INSTALL_DIR}

rm -rf /tmp/underworld-build
mkdir -p /tmp/underworld-build
pushd /tmp/underworld-build

export UNDERWORLD_SRC=%{_topdir}/BUILD/underworld-%{pkg_version}
export UNDERWORLD_INSTALLATION=%{INSTALL_DIR}

export CXX=mpicxx
export CC=mpicc
#### HDF5_MPI="ON" HDF5_DIR=/path/to/your/hdf5/install/ pip install --no-binary=h5py h5py
( \
  cd ${UNDERWORLD_SRC}/underworld/libUnderworld \
   && python3 configure.py \
      --prefix=${UNDERWORLD_INSTALLATION} \
      --mpi-dir=${TACC_IMPI_DIR}  \
      --h5py-launcher=ibrun \
      --h5py-notest=1 \
)
( \
  cd ${UNDERWORLD_SRC}/underworld/libUnderworld \
   && echo python3 setup.py install \
   && python3 compile.py \
   && python3 scons.py install \
)

echo "are we still in /tmp/underworld-build?"
pwd
popd

cp -r docs %{INSTALL_DIR}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
The underworld module defines the following environment variables:
TACC_UNDERWORLD_DIR, TACC_UNDERWORLD_BIN, and
TACC_UNDERWORLD_LIB for the location
of the Underworld distribution, documentation, binaries,
and libraries.

The python interface requires python3 3.9 or higher.

Version %{version}
external packages installed: ${underworld_extra_libs}
]] )

whatis( "Name: Underworld" )
whatis( "Version: %{version}${versionextra}${dynamicextra}" )
whatis( "Version-notes: external packages installed: ${packages}" )
whatis( "Category: library, mathematics" )
whatis( "URL: https://github.com/underworld/Underworld" )
whatis( "Description: Portable Extendible Toolkit for Scientific Computing, Numerical library for sparse linear algebra" )

local             underworld_dir =     "%{INSTALL_DIR}/"

prepend_path("PYTHONPATH",      underworld_dir )

setenv("TACC_UNDERWORLD_DIR",             underworld_dir)

depends_on( "python3", "phdf5/1.10.4" )
EOF

%if "%{has_python}" == "1"
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
prepend_path("PYTHONPATH",         pathJoin(underworld_dir,"lib","python%{python_version_version}","site-packages") )

depends_on( "python3" )
EOF
%endif

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << EOF
#%Module1.0#################################################
##
## version file for Underworld %version
##

set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

##
## end of configure install section
##

module unload python
cp -r %{INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/

  rm -rf /tmp/build-${pkg_version}*

umount %{INSTALL_DIR} # tmpfs # $INSTALL_DIR

%files %{PACKAGE}
  %defattr(0644,root,root,0755)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(0644,root,root,0755)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
* Wed Jan 05 2022 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
