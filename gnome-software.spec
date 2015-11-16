#
# Conditional build:
%bcond_without	fwupd	# firmware support via fwupd
%bcond_with	limba	# Limba support
#
Summary:	GNOME Software - install and update applications and system extensions
Summary(pl.UTF-8):	GNOME Software - instalowanie i uaktualnianie aplikacji oraz rozszerzeń systemu
Name:		gnome-software
Version:	3.18.3
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-software/3.18/%{name}-%{version}.tar.xz
# Source0-md5:	dc93107a8fb1a2cbda6faf144a6f4537
URL:		https://wiki.gnome.org/Apps/Software
%{?with_limba:BuildRequires:	Limba-devel >= 0.4.2}
BuildRequires:	PackageKit-devel >= 1.0.9
BuildRequires:	appstream-glib-devel >= 0.5.1
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
%{?with_fwupd:BuildRequires:	fwupd-devel}
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.45.8
BuildRequires:	gnome-common
BuildRequires:	gnome-desktop-devel >= 3.18
BuildRequires:	gsettings-desktop-schemas-devel >= 3.11.5
BuildRequires:	gtk+3-devel >= 3.17.7
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libsoup-devel >= 2.52
BuildRequires:	libtool >= 2:2
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	glib2 >= 1:2.45.8
Requires(post,postun):	gtk-update-icon-cache
Requires:	glib2 >= 1:2.45.8
Requires:	gsettings-desktop-schemas >= 3.11.5
Requires:	gtk+3 >= 3.17.7
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME Software lets you install and update applications and system
extensions.

%description -l pl.UTF-8
GNOME Software pozwala instalować i uaktualniać aplikacje oraz
rozszerzenia systemu.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-firmware%{!?with_fwupd:=no} \
	--enable-limba%{!?with_limba:=no} \
	--disable-silent-rules \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/gs-plugins-8/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_icon_cache hicolor
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README
%attr(755,root,root) %{_bindir}/gnome-software
/etc/xdg/autostart/gnome-software-service.desktop
%dir %{_libdir}/gs-plugins-8
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_appstream.so
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_epiphany.so
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_fedora_tagger_ratings.so
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_fedora_tagger_usage.so
%if %{with fwupd}
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_fwupd.so
%endif
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_hardcoded-featured.so
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_icons.so
%if %{with limba}
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_limba.so
%endif
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_local-ratings.so
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_menu-spec-categories.so
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_menu-spec-refine.so
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_moduleset.so
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_packagekit.so
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_packagekit-history.so
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_packagekit-offline.so
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_packagekit-refine.so
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_packagekit-refresh.so
%attr(755,root,root) %{_libdir}/gs-plugins-8/libgs_plugin_systemd-updates.so
%{_datadir}/appdata/org.gnome.Software.appdata.xml
%{_datadir}/dbus-1/services/org.freedesktop.PackageKit.service
%{_datadir}/dbus-1/services/org.gnome.Software.service
%{_datadir}/glib-2.0/schemas/org.gnome.software.gschema.xml
%{_datadir}/gnome-shell/search-providers/gnome-software-search-provider.ini
%{_datadir}/gnome-software
%{_desktopdir}/gnome-software-local-file.desktop
%{_desktopdir}/org.gnome.Software.desktop
%{_iconsdir}/hicolor/*x*/apps/gnome-software.png
%{_iconsdir}/hicolor/scalable/apps/gnome-software-symbolic.svg
%{_mandir}/man1/gnome-software.1*
