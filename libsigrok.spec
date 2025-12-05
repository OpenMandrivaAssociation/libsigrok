%define major 4
%define libname %mklibname sigrok
%define libcxxname %mklibname sigrok-cxx
%define devname %mklibname sigrok -d
%define devcxxname %mklibname sigrok-cxx -d

%define sourcedate 20251204
%define gitcommit 0bc2487

# NOTE To update this package run package-source.sh in order to create a new source
# NOTE tarball from the latest upstream git master branch.
# NOTE The script will adjust sourcedate & gitcommit defines to match created tarball.
# NOTE You may have to reload this file to see the changed values.

# these language bindings break the build, disable them.
%bcond java 0
%bcond python 0
%bcond ruby 0
# disable building of static libraries
%bcond static 0

Name:		libsigrok
Version:	0.6.0+git%{sourcedate}.%{gitcommit}
Release:	1
Summary:	libsigrok is a shared library which provides hardware access drivers for logic analyzers, oscilloscopes, multimeters, and more
URL:		https://sigrok.org
License:	GPL-3.0-or-later
Group:		Productivity/Scientific
Source0:	%{name}-%{sourcedate}-%{gitcommit}.tar.zst
#Source0:	https://sigrok.org/download/source/%%{name}/%%{name}-%%{version}.tar.gz
# Alternative GH source
#Source0:	https://github.com/sigrokproject/libsigrok/archive/%%{version}/%%{name}-%%{version}.tar.gz

BuildRequires:	autoconf automake slibtool
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	hicolor-icon-theme
BuildRequires:	ieee1284-devel
%if %{with java}
BuildRequires:	java-devel
%endif
BuildRequires:	make
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(glibmm-2.4)
BuildRequires:	pkgconfig(hidapi-hidraw)
BuildRequires:	pkgconfig(hidapi-libusb)
BuildRequires:	pkgconfig(libftdi1)
BuildRequires:	pkgconfig(libgpib)
BuildRequires:	pkgconfig(libserialport)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libzip)
BuildRequires:	pkgconfig(nettle)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(zlib)
%if %{with python}
BuildRequires:	python%{pyver}dist(doxypypy)
BuildRequires:	python%{pyver}dist(numpy)
BuildRequires:	python%{pyver}dist(pygobject)
BuildRequires:	python%{pyver}dist(setuptools)
%endif
%if %{with ruby}
BuildRequires:	pkgconfig(ruby)
%endif
BuildRequires:	swig


%description
libsigrok is a shared library written in C which provides the basic API
for talking to hardware and reading/writing the acquired data into various
input/output file formats.

%package -n %{libname}
Summary:	libsigrok is a shared library which provides hardware access drivers for logic analyzers, oscilloscopes, multimeters, and more
Group:		System/Libraries
Recommends:		sigrok-firmware-fx2lafw

%description -n %{libname}
libsigrok is a shared library written in C which provides the basic API
for talking to hardware and reading/writing the acquired data into various
input/output file formats.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%package -n %{libcxxname}
Summary:	C++ language bindings for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{libcxxname}
The %{libcxxname} package contains C++ libraries for %{name}.

libsigrok is a shared library written in C which provides the basic API
for talking to hardware and reading/writing the acquired data into various
input/output file formats.

%package -n %{devcxxname}
Summary:	Development files for %{name} C++ bindings
Group:		Development/C
Requires:	%{libcxxname} = %{version}-%{release}

%description -n %{devcxxname}
The %{devcxxname} package contains libraries and header files for
developing applications that use %{name} C++ bindings.


%prep
%autosetup -n %{name}-%{sourcedate}-%{gitcommit} -p1
# fixup udev rules
sed -i -e 's/ENV{ID_SIGROK}="1"/TAG+="uaccess"/g' contrib/60-libsigrok.rules

%build
autoreconf -fvi
%configure \
	CPPFLAGS=-I/usr/include/tirpc LDFLAGS=-ltirpc \
	--enable-fx2lafw \
	%{!?with_java:--disable-java} \
	%{!?with_python:--disable-python} \
	%{!?with_ruby:--disable-ruby} \
	%{!?with_static:--disable-static}
%make_build

%install
%make_install

find %{buildroot} -type f -name "*.la" -delete -print

# install udev rules
install -Dpm 644 contrib/60-libsigrok.rules %{buildroot}%{_udevrulesdir}/60-libsigrok.rules


%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libcxxname} -p /sbin/ldconfig

%postun -n %{libcxxname} -p /sbin/ldconfig


%files -n %{libname}
%doc README README.devices NEWS
%license COPYING
%{_libdir}/libsigrok.so.%{major}*
%{_udevrulesdir}/60-libsigrok.rules
%{_datadir}/mime/packages/vnd.sigrok.session.xml
%{_datadir}/icons/hicolor/48x48/mimetypes/libsigrok.png
%{_datadir}/icons/hicolor/scalable/mimetypes/libsigrok.svg

%files -n %{devname}
%{_includedir}/libsigrok/
%{_libdir}/libsigrok.so
%{_libdir}/pkgconfig/libsigrok.pc

%files -n %{libcxxname}
%{_libdir}/libsigrokcxx.so.%{major}*

%files -n %{devcxxname}
%{_includedir}/libsigrokcxx/
%{_libdir}/libsigrokcxx.so
%{_libdir}/pkgconfig/libsigrokcxx.pc
