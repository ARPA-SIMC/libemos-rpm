Name:           libemos
Version:        4.5.9
Release:        6%{?dist}
Summary:        ECMWF Interpolation Library

License:        Apache 2.0
URL:            https://confluence.ecmwf.int/display/EMOS/
Source0:        https://confluence.ecmwf.int/download/attachments/3473472/%{name}-%{version}-Source.tar.gz

BuildRequires:  cmake3
BuildRequires:  eccodes-devel
BuildRequires:  eccodes-doc
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  fftw-devel
BuildRequires:  boost-devel
BuildRequires:  git
# Apparently only required for CentOs
BuildRequires:  jasper-devel
BuildRequires:  openjpeg2-devel
BuildRequires:  libpng-devel

%description
The Interpolation library (EMOSLIB) includes Interpolation software
and BUFR & CREX encoding/decoding routines.
It is used by the ECMWF meteorological archival and retrieval system
(MARS) and also by the ECMWF workstation Metview.

This software covers :
 - Interpolating fields
   - spectral coefficients to spectral coefficients
   - spectral coefficients to rotated spectral coefficients
   - spectral coefficients to regular latitude-longitude grids
   - spectral coefficients to regular gaussian grids
   - spectral coefficients to quasi-regular gaussian grids
   - regular latitude-longitude grids to regular latitude-longitude grids
   - regular latitude-longitude grids to regular gaussian grids
   - regular gaussian grids to regular gaussian grids
   - regular gaussian grids to regular latitude-longitude grids
   - quasi-regular gaussian grids to regular latitude-longitude grids
   - quasi-regular gaussian grids to regular gaussian grids
 - encoding/decoding of WMO FM-94 BUFR BUFR code messages
 - encoding/decoding of WMO FM-95 CREX CREX code messages
 - handling pure binary unix files
 - multiple(Tempertons) FFT routines (from release 000340 onwards)


%prep
%setup -q -n %{name}-%{version}-Source


%build
mkdir build
pushd build

# TODO:
# Patch all arguments mismatch?

%if 0%{?fedora} >= 32
# https://gcc.gnu.org/gcc-10/changes.html (see Fortran section)
%define f_mismatch 1
%endif

# TODO:
# somethere beteween eccodes 2.12.5 and 2.13.0 libemos stopped to detect
# eccodes variables (include dir and libraries).
# Forcing assignment is a (not ideal) workaround.

%cmake3 .. \
	-DCMAKE_C_FLAGS="%{optflags} -w" \
	-DCMAKE_Fortran_FLAGS="%{optflags} %{?f_mismatch:-fallow-argument-mismatch}" \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DINSTALL_LIB_DIR=%{_lib} \
	-DECCODES_INCLUDE_DIR=%{_includedir} \
	-DECCODES_LIBRARIES="eccodes" \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_MESSAGE=NEVER \
	-DENABLE_SINGLE_PRECISION=ON \
	-DBUILD_SHARED_LIBS=ON \
	-DENABLE_GRIBEX_ABORT=OFF


%if 0%{?fedora} >= 32
# https://fedoraproject.org/wiki/Changes/CMake_to_do_out-of-source_builds
%cmake_build
%else
%make_build
%endif

popd

%check

%if 0%{?rhel} >= 7
%define python3_vers python36
# test disabled
%else
pushd build
CTEST_OUTPUT_ON_FAILURE=1 ctest3 %{?_smp_mflags}
popd
%endif

%install
[ "%{buildroot}" != / ] && rm -rf %{buildroot}
pushd build

%if 0%{?fedora} >= 32
# https://fedoraproject.org/wiki/Changes/CMake_to_do_out-of-source_builds
%cmake_install
%else
%make_install
%endif

popd

%clean
[ "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%license LICENSE
%defattr(-,root,root)
%{_bindir}/*
# these are also in eccodes package...
%exclude %{_bindir}/bufr_compare
%exclude %{_bindir}/bufr_compare_dir
%exclude %{_bindir}/bufr_copy
%exclude %{_bindir}/bufr_count
%exclude %{_bindir}/bufr_dump
%exclude %{_bindir}/bufr_filter
%exclude %{_bindir}/bufr_get
%exclude %{_bindir}/bufr_ls
%exclude %{_bindir}/bufr_set
%{_libdir}/libemos.a
%{_libdir}/libemosR64.a
%{_libdir}/pkgconfig/libemos.pc
%{_libdir}/pkgconfig/libemosR64.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*


%changelog
* Wed May  5 2021 Daniele Branchini <dbranchini@arpae.it> - 4.5.9-6
- fixed builds for F33/F34

* Wed Apr 29 2020 Daniele Branchini <dbranchini@arpae.it> - 4.5.9-5
- Allowing argument mismatch for gcc 10

* Thu Dec 19 2019 Daniele Branchini <dbranchini@arpae.it> - 4.5.9-4
- Restored some binaries for Metview compilation

* Tue Nov 12 2019 Daniele Branchini <dbranchini@arpae.it> - 4.5.9-3
- Removing bin from package to avoid conflict with eccodes

* Wed Oct 16 2019 Daniele Branchini <dbranchini@arpae.it> - 4.5.9-2
- Re-enabling GRIBEX call

* Thu Oct  3 2019 Daniele Branchini <dbranchini@arpae.it> - 4.5.9-1
- Upstream update

* Mon Oct 15 2018 Daniele Branchini <dbranchini@arpae.it> - 4.5.7-1
- Upstream update

* Fri Sep  7 2018 Daniele Branchini <dbranchini@arpae.it> - 4.5.5-2
- Bogus release to get rid of libeccodes_memfs.so dependency

* Wed May 23 2018 Daniele Branchini <dbranchini@arpae.it> - 4.5.5-1
- Upstream update
- Reducing build logs (#1)
- Enabling GRIBEX call since some internal sw (verifica) depends on it

* Tue Mar 27 2018 Daniele Branchini <dbranchini@arpae.it> - 4.5.4-1
- Upstream update

* Wed Feb  7 2018 Emanuele Di Giacomo <edigiacomo@arpae.it> - 4.5.1-1
- First package
