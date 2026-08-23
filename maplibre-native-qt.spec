%define major 3
%define libcore %mklibname QMapLibre %{major}
%define libloc %mklibname QMapLibreLocation %{major}
%define libwid %mklibname QMapLibreWidgets %{major}
%define devname %mklibname QMapLibre -d

Name:		maplibre-native-qt
Version:	3.0.0
Release:	1
Summary:	MapLibre Native Qt bindings and Qt Location plugin
License:	BSD-2-Clause
Group:		System/Libraries
Url:		https://github.com/maplibre/maplibre-native-qt
# Recursively vendored snapshot (upstream release tarball has no submodules)
Source0:	maplibre-native-qt-%{version}.tar.xz
# GCC 15: missing <cstdint> in maplibre-native
Patch0:		maplibre-native-qt-gcc15.patch
# Source snapshot omits test/benchmark trees
Patch1:		maplibre-native-qt-skip-tests.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Sql)
BuildRequires:	cmake(Qt6Location)
BuildRequires:	cmake(Qt6LocationPrivate)
BuildRequires:	cmake(Qt6OpenGLWidgets)
BuildRequires:	cmake(Qt6Widgets)
BuildSystem:	cmake
BuildOption:	-DQT_VERSION_MAJOR=6
BuildOption:	-DBUILD_SHARED_LIBS:BOOL=ON
BuildOption:	-DMLN_QT_WITH_LOCATION:BOOL=ON
BuildOption:	-DMLN_QT_WITH_WIDGETS:BOOL=ON
BuildOption:	-DBUILD_TESTING:BOOL=OFF
BuildOption:	-DMLN_WITH_WERROR:BOOL=OFF

%description
Qt bindings for MapLibre Native, including a Qt Location geoservices plugin
used by applications such as KDE Itinerary.

%package -n %{libcore}
Summary:	MapLibre Native Qt core library
Group:		System/Libraries

%description -n %{libcore}
Core QMapLibre library.

%package -n %{libloc}
Summary:	MapLibre Native Qt Location library
Group:		System/Libraries
Requires:	%{libcore} = %{EVRD}

%description -n %{libloc}
QMapLibre Location integration and Qt geoservices/QML plugins.

%package -n %{libwid}
Summary:	MapLibre Native Qt Widgets library
Group:		System/Libraries
Requires:	%{libcore} = %{EVRD}

%description -n %{libwid}
QMapLibre Widgets (QMapLibre::GLWidget).

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libcore} = %{EVRD}
Requires:	%{libloc} = %{EVRD}
Requires:	%{libwid} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Headers and CMake files for %{name}.

%prep
%autosetup -p1
# Qt 6.10+ needs the Location private headers
sed -i \
	-e 's/COMPONENTS Location REQUIRED/COMPONENTS Location LocationPrivate REQUIRED/' \
	-e '/^add_subdirectory(test)$/d' \
	CMakeLists.txt

%install -a
# Upstream installs plugins/QML under $prefix/{plugins,qml}; Qt looks in qt6/
if [ -d %{buildroot}%{_prefix}/plugins ]; then
	mkdir -p %{buildroot}%{_libdir}/qt6
	mv %{buildroot}%{_prefix}/plugins %{buildroot}%{_libdir}/qt6/plugins
fi
if [ -d %{buildroot}%{_prefix}/qml ]; then
	mkdir -p %{buildroot}%{_libdir}/qt6
	mv %{buildroot}%{_prefix}/qml %{buildroot}%{_libdir}/qt6/qml
fi
if [ -d %{buildroot}%{_libdir}/cmake/QMapLibre ]; then
	sed -i \
		-e 's,/plugins/,/%{_lib}/qt6/plugins/,g' \
		-e 's,/qml/,/%{_lib}/qt6/qml/,g' \
		%{buildroot}%{_libdir}/cmake/QMapLibre/*.cmake
fi

%files -n %{libcore}
%license LICENSES/*
%{_libdir}/libQMapLibre.so.%{major}*

%files -n %{libloc}
%{_libdir}/libQMapLibreLocation.so.%{major}*
%{_libdir}/qt6/plugins/geoservices
%{_libdir}/qt6/qml/MapLibre

%files -n %{libwid}
%{_libdir}/libQMapLibreWidgets.so.%{major}*

%files -n %{devname}
%{_includedir}/QMapLibre
%{_includedir}/QMapLibreWidgets
%{_includedir}/mbgl
%{_libdir}/libQMapLibre.so
%{_libdir}/libQMapLibreLocation.so
%{_libdir}/libQMapLibreWidgets.so
%{_libdir}/cmake/QMapLibre
