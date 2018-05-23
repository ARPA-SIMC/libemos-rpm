Name:           libemos
Version:        4.5.5
Release:        1%{?dist}
Summary:        ECMWF Interpolation Library

License:        Apache 2.0
URL:            https://software.ecmwf.int/wiki/display/EMOS/
Source0:        https://software.ecmwf.int/wiki/download/attachments/3473472/%{name}-%{version}-Source.tar.gz
BuildRequires:  cmake
BuildRequires:  eccodes-devel
BuildRequires:  eccodes-doc
BuildRequires:  gcc-gfortran
BuildRequires:  fftw-devel
BuildRequires:  boost-devel
BuildRequires:  git
# Apparently only required for CentOs
BuildRequires:  jasper-devel
BuildRequires:  openjpeg2-devel

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

%cmake .. \
    -DCMAKE_FC_FLAGS="$FCFLAGS -Wno-unused-variable -Wno-unused-but-set-variable -Wno-unused-label -Wno-integer-division" \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DINSTALL_LIB_DIR=%{_lib} \
    -DCMAKE_BUILD_TYPE=Release \
    -DINSTALL_INCLUDE_DIR=%{_includedir} \
    -DCMAKE_INSTALL_MESSAGE=NEVER \
    -DENABLE_SINGLE_PRECISION=ON \
    -DBUILD_SHARED_LIBS=ON \
    -DENABLE_GRIBEX_ABORT=OFF

%make_build

popd

%check
pushd build
CTEST_OUTPUT_ON_FAILURE=1 make test
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd build
%make_install
popd


%files
%license LICENSE
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libemos.a
%{_libdir}/libemosR64.a
%{_libdir}/pkgconfig/libemos.pc
%{_libdir}/pkgconfig/libemosR64.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*


%changelog
* Wed May 23 2018 Daniele Branchini <dbranchini@arpae.it> - 4.5.5-1
- Upstream update
- Reducing build logs (#1)
- Enabling GRIBEX call since some internal sw (verifica) depends on it

* Tue Mar 27 2018 Daniele Branchini <dbranchini@arpae.it> - 4.5.4-1
- Upstream update

* Wed Feb  7 2018 Emanuele Di Giacomo <edigiacomo@arpae.it> - 4.5.1-1
- First package
