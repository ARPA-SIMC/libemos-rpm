Name:           libemos
Version:        4.5.1
Release:        1%{?dist}
Summary:        ECMWF Interpolation Library

License:        Apache 2.0
URL:            https://software.ecmwf.int/wiki/display/EMOS/
Source0:        https://software.ecmwf.int/wiki/download/attachments/3473472/%{name}-%{version}-Source.tar.gz

BuildRequires:  cmake
BuildRequires:  eccodes-devel
BuildRequires:  gcc-gfortran
BuildRequires:  fftw-devel

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
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DINSTALL_LIB_DIR=%{_lib} \
    -DCMAKE_BUILD_TYPE=Release


%make_build

popd

%check
pushd build
make test
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
* Wed Feb  7 2018 Emanuele Di Giacomo <edigiacomo@arpae.it> - 4.5.1-1
- First package
