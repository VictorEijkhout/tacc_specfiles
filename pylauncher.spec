#
# autoconf.spec
# Victor Eijkhout
#

Summary: Pylauncher

# Give the package a base name
%define pkg_base_name pylauncher
%define MODULE_VAR    PYLAUNCHER

# Create some macros (spec file variables)
%define major_version 5
%define minor_version 3
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
# include compiler-defines.inc

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

Release:   14
License:   BSD
Group:     Development/Tools
URL:       https://github.com/TACC/pylauncher
Packager:  TACC - eijkhout@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tgz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%define _build_id_links none
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Pylauncher
Group: Support
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: Pylauncher
Group: Support
%description modulefile
Pylauncher

%description
Pylauncher


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
%endif
# BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
  %endif
  # BUILD_MODULEFILE |
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
# %include compiler-load.inc

# Insert further module commands

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
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
  
mkdir -p %{INSTALL_DIR}
rm -rf %{INSTALL_DIR}/*
mount -t tmpfs tmpfs %{INSTALL_DIR}

## no prereqs
## module load 

################ new stuff

export SRCPATH=`pwd`
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export VICTOR=/admin/build/admin/rpms/frontera/SPECS/rpmtng
export MAKEINCLUDES=${VICTOR}/make-support-files

pushd ${VICTOR}/makefiles/%{pkg_base_name}

## get rid of that PACKAGEROOT
make default_install JCOUNT=10 \
    HOMEDIR=/admin/build/admin/rpms/frontera/SOURCES \
    PACKAGEVERSION=%{pkg_version} \
    PACKAGEROOT=/tmp \
    BUILDDIRROOT=/tmp \
    SRCPATH=${SRCPATH} \
    INSTALLPATH=%{INSTALL_DIR} \
    MODULEDIRSET=$RPM_BUILD_ROOT/%{MODULE_DIR}

popd

################ end of new stuff

  # Copy installation from tmpfs to RPM directory
  ls %{INSTALL_DIR}
  cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/

  rm -rf /tmp/build-${pkg_version}*

umount %{INSTALL_DIR}
  
ls $RPM_BUILD_ROOT/%{INSTALL_DIR}/

#-----------------------  
%endif
# BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
  %endif

#--------------------------
  %endif
  # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(0644,root,root,0755)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
  %endif
  # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 
#---------------------------

  %defattr(0644,root,root,0755)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

#--------------------------
  %endif
  # BUILD_MODULEFILE |
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

#---------------------------------------
%changelog
#---------------------------------------
#
* Tue Apr 15 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 14: umask fix
* Tue Apr 15 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 13: core handling really fixed
* Wed Mar 19 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 12: 5.2.2 fixes core count
* Tue Mar 18 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 11: 5.2.1 fixes internal version
* Mon Mar 17 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 10: 5.2 fixes the submitlauncher
* Mon Mar 10 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 9: file core mode fixed in 5.1.1
* Fri Mar 07 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 8: file core handling fixed
* Mon Mar 03 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 7: repo mixup
* Mon Mar 03 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 6: gpu launcher
* Tue Jan 07 2025 eijkhout <eijkhout@tacc.utexas.edu>
- release 5: no longer testing node type
* Mon Sep 09 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: core count detection
* Fri Sep 06 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: fix ibrun launcher
* Thu Aug 01 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: bug fixes
* Fri Jul 12 2024 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
