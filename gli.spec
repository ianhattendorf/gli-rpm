# Header only library
%global debug_package %{nil}

Name:		gli
Version:	0.8.2.0
Release:	1%{?dist}
Summary:	OpenGL Image (GLI) is a header only C++ image library for graphics software

License:	MIT
URL:		http://gli.g-truc.net
Source0:	https://github.com/g-truc/gli/releases/download/%{version}/%{name}-%{version}.zip
# Don't override CXX flags when building
Patch0:		gli-cxx-flags.patch
# Use system GLM instead of bundled version
Patch1:		gli-use-system-glm.patch

# Test failures on bid-endian machines
# https://github.com/g-truc/gli/issues/140
ExcludeArch:	ppc64 s390x

BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	glm-static

%description
OpenGL Image (GLI) is a header only C++ image library for graphics software.

GLI provides classes and functions to load image files (KTX and DDS), facilitate
graphics APIs texture creation, compare textures, access texture texels, sample
textures, convert textures, generate mipmaps, etc.

%package	devel
Summary:	OpenGL Image (GLI) is a header only C++ image library for graphics software
Requires:	glm-static

# https://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_Static_Libraries_2
Provides:	%{name}-static = %{version}-%{release}

%description	devel
OpenGL Image (GLI) is a header only C++ image library for graphics software.

GLI provides classes and functions to load image files (KTX and DDS), facilitate
graphics APIs texture creation, compare textures, access texture texels, sample
textures, convert textures, generate mipmaps, etc.

%package	doc
Summary:	Documentation for %{name}-devel

%description	doc
API documentation for the %{name}-devel package.

%prep
%setup -q -n gli

# Patches are in unix (LF) format from git
sed -i 's/\r//' CMakeLists.txt

# Doc file line endings
sed -i 's/\r//' manual.md
sed -i 's/\r//' readme.md
sed -i 's/\r//' doc/api/doxygen.css
sed -i 's/\r//' doc/api/tabs.css

%patch0 -p1
%patch1 -p1

%build
mkdir build
cd build
%{cmake} ..
%make_build

%check
cd build
ctest --output-on-failure

%install
cd build
%make_install
find $RPM_BUILD_ROOT -name CMakeLists.txt -delete

%files devel
%doc readme.md
%doc manual.md
%{_includedir}/%{name}
%{_libdir}/cmake

%files doc
%doc doc/api

%changelog
* Sat Mar 10 2018 Ian Hattendorf <ian@ianhattendorf.com> - 0.8.2.0-1
- Initial RPM spec

