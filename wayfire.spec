#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	A modular and extensible wayland compositor
Name:		wayfire
Version:	0.8.0
Release:	2
License:	MIT
Group:		Applications
Source0:	https://github.com/WayfireWM/wayfire/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	36e88c89c0be0e6af725ecab15049ecb
Patch0:		no-git-check.patch
URL:		https://wayfire.org/
BuildRequires:	EGL-devel
BuildRequires:	GLM-devel >= 0.9.9.9
BuildRequires:	OpenGLESv2-devel
BuildRequires:	cairo-devel
BuildRequires:	cmake
BuildRequires:	libdrm-devel
BuildRequires:	libevdev-devel
BuildRequires:	libinput-devel >= 1.7.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel >= 6:9
BuildRequires:	libxcb-devel
BuildRequires:	meson >= 0.56.0
BuildRequires:	ninja
BuildRequires:	nlohmann-json-devel
BuildRequires:	pango-devel
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	wayland-devel
BuildRequires:	wayland-protocols >= 1.12
BuildRequires:	wf-config-devel < 0.9.0
BuildRequires:	wf-config-devel >= 0.8.0
BuildRequires:	wlroots-devel < 0.17.0
BuildRequires:	wlroots-devel >= 0.16.0
BuildRequires:	xorg-lib-libxkbcommon-devel
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libinput >= 1.7.0
Requires:	wf-config < 0.9.0
Requires:	wf-config >= 0.8.0
Requires:	wlroots < 0.17.0
Requires:	wlroots >= 0.16.0
Suggests:	alacritty
Suggests:	alsa-utils
Suggests:	grim
Suggests:	kanshi
Suggests:	mako
Suggests:	swayidle
Suggests:	swaylock
Suggests:	wcm
Suggests:	wf-shell
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Wayfire is a 3D Wayland compositor, inspired by Compiz and based on
wlroots. It aims to create a customizable, extendable and lightweight
environment without sacrificing its appearance.

%package libs
Summary:	Wayfire libraries
Group:		Libraries

%description libs
Wayfire libraries

%package devel
Summary:	Header files for wayfire
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	GLM-devel >= 0.9.9.9
Requires:	cairo-devel
Requires:	libstdc++-devel >= 6:9
Requires:	pango-devel
Requires:	pixman-devel
Requires:	wayland-devel
Requires:	wf-config-devel < 0.9.0
Requires:	wf-config-devel >= 0.8.0
Requires:	wlroots-devel < 0.17.0
Requires:	wlroots-devel >= 0.16.0

%description devel
Header files for wayfire.

%package static
Summary:	Static wayfire libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static wayfire libraries.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	%{!?with_static_libs:--default-library=shared}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/wayfire/icons

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CONTRIBUTING.md LICENSE README.md wayfire.ini
%attr(755,root,root) %{_bindir}/wayfire
%attr(755,root,root) %{_libdir}/libwayfire-blur-base.so
%dir %{_libdir}/wayfire
%attr(755,root,root) %{_libdir}/wayfire/*.so
%dir %{_datadir}/wayfire
%dir %{_datadir}/wayfire/icons
%{_datadir}/wayfire/metadata
%{_datadir}/wayland-sessions/wayfire.desktop
%{_mandir}/man1/wayfire.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwf-utils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwf-utils.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwf-utils.so
%{_includedir}/wayfire
%{_pkgconfigdir}/wayfire.pc
%{_pkgconfigdir}/wf-utils.pc
%{_datadir}/wayfire/protocols

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwf-utils.a
%endif
