#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	A modular and extensible wayland compositor
Summary(pl.UTF-8):	Modularny i rozszerzalny kompozytor Wayland
Name:		wayfire
Version:	0.10.0
Release:	1
License:	MIT
Group:		Applications
#Source0Download: https://github.com/WayfireWM/wayfire/releases
Source0:	https://github.com/WayfireWM/wayfire/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	4a5f02e27cc4e00da22865a78ef2e0f8
Patch0:		glm.patch
URL:		https://wayfire.org/
BuildRequires:	EGL-devel
BuildRequires:	GLM-devel >= 0.9.9.9
BuildRequires:	OpenGLESv2-devel
BuildRequires:	Vulkan-Loader-devel
BuildRequires:	cairo-devel
BuildRequires:	cmake
BuildRequires:	libdrm-devel
BuildRequires:	libevdev-devel
BuildRequires:	libgomp-devel
BuildRequires:	libinput-devel >= 1.27.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel >= 6:12
BuildRequires:	libxcb-devel
BuildRequires:	meson >= 0.64.0
BuildRequires:	ninja
BuildRequires:	pango-devel
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	wayland-devel
BuildRequires:	wayland-protocols >= 1.12
BuildRequires:	wf-config-devel < 0.11.0
BuildRequires:	wf-config-devel >= 0.10.0
BuildRequires:	wlroots0.19-devel <= 0.19.99
BuildRequires:	wlroots0.19-devel >= 0.19.0
BuildRequires:	xorg-lib-libxkbcommon-devel
BuildRequires:	xz
BuildRequires:	yyjson-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libinput >= 1.27.0
Requires:	wf-config < 0.11.0
Requires:	wf-config >= 0.10.0
Requires:	wlroots0.19 <= 0.19.99
Requires:	wlroots0.19 >= 0.19.0
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

%description -l pl.UTF-8
Wayfire to trójwymiarowy kompozytor Wayland, zainspirowany Compizem i
oparty na wlroots. Celem jest utworzenie rozszerzalnego, lekkiego
środowiska bez poświęcania wyglądu.

%package libs
Summary:	Wayfire libraries
Summary(pl.UTF-8):	Biblioteki Wayfire
Group:		Libraries

%description libs
Wayfire libraries.

%description libs -l pl.UTF-8
Biblioteki Wayfire.

%package devel
Summary:	Header files for wayfire
Summary(pl.UTF-8):	Pliki nagłówkowe wayfire
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	GLM-devel >= 0.9.9.9
Requires:	cairo-devel
Requires:	libstdc++-devel >= 6:12
Requires:	pango-devel
Requires:	pixman-devel
Requires:	wayland-devel
Requires:	wf-config-devel < 0.11.0
Requires:	wf-config-devel >= 0.10.0
Requires:	wlroots0.19-devel <= 0.19.99
Requires:	wlroots0.19-devel >= 0.19.0

%description devel
Header files for wayfire.

%description devel -l pl.UTF-8
Pliki nagłówkowe wayfire.

%package static
Summary:	Static wayfire libraries
Summary(pl.UTF-8):	Biblioteki statyczne wayfire
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static wayfire libraries.

%description static -l pl.UTF-8
Biblioteki statyczne wayfire.

%prep
%setup -q
%patch -P0 -p1

%build
%meson \
	%{!?with_static_libs:--default-library=shared}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/wayfire/icons

%meson_install

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
%{_datadir}/xdg-desktop-portal/wayfire-portals.conf
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
%{_libdir}/libwayfire-move-drag-interface.a
%{_libdir}/libwayfire-workspace-wall.a
%{_libdir}/libwf-utils.a
%{_libdir}/libwftouch.a
%endif
