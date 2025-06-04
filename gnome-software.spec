# TODO:
# - use gtk4-update-icon-cache
#
# Conditional build:
%bcond_without	flatpak		# Flatpak support
%bcond_without	fwupd		# firmware support via fwupd
%bcond_with	eos		# Endless OS updater support
%bcond_without	malcontent	# parental control via libmalcontent
%bcond_with	mogwai		# metered data support using Mogwai
%bcond_without	packagekit	# PackageKit support
%bcond_with	rpm_ostree	# CoreOS rpm-ostree support
%bcond_with	snap		# Snap support
%bcond_with	ext_appstream	# external appstream support
%bcond_with	sysprof		# sysprof-capture support for profiling
#
Summary:	GNOME Software - install and update applications and system extensions
Summary(pl.UTF-8):	GNOME Software - instalowanie i uaktualnianie aplikacji oraz rozszerzeń systemu
Name:		gnome-software
Version:	48.2
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-software/48/%{name}-%{version}.tar.xz
# Source0-md5:	b461f32a818b5218864b90fb3303d306
URL:		https://apps.gnome.org/Software/
BuildRequires:	AppStream-devel >= 0.16.4
%{?with_packagekit:BuildRequires:	PackageKit-devel >= 1.2.5}
BuildRequires:	docbook-style-xsl-nons
%{?with_flatpak:BuildRequires:	flatpak-devel >= 1.14.1}
%{?with_fwupd:BuildRequires:	fwupd-devel >= 1.6.2}
BuildRequires:	gdk-pixbuf2-devel >= 2.32.0
BuildRequires:	gettext-its-metainfo
BuildRequires:	gettext-tools >= 0.19.7
BuildRequires:	glib2-devel >= 1:2.76.0
BuildRequires:	gnome-online-accounts-devel
BuildRequires:	gsettings-desktop-schemas-devel >= 3.18.0
BuildRequires:	gtk4-devel >= 4.16.0
BuildRequires:	gtk-doc >= 1.11
BuildRequires:	gspell-devel
BuildRequires:	json-glib-devel >= 1.6.0
BuildRequires:	libadwaita-devel >= 1.6
%{?with_rpm_ostree:BuildRequires:	libdnf-devel}
# for tests
#BuildRequires:	libglib-testing-devel
%{?with_malcontent:BuildRequires:	libmalcontent-devel >= 0.5.0}
BuildRequires:	libsoup3-devel >= 3.0
BuildRequires:	libxmlb-devel >= 0.3.4
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 1.0.1
# mogwai-schedule-client-0
%{?with_mogwai:BuildRequires:	mogwai-devel >= 0.2.0}
BuildRequires:	ninja >= 1.5
%if %{with eos} || %{with rpm_ostree}
BuildRequires:	ostree-devel
%endif
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel
BuildRequires:	rpm-build >= 4.6
%{?with_rpm_ostree:BuildRequires:	rpm-ostree-devel >= 2019.3}
BuildRequires:	rpmbuild(macros) >= 2.042
%{?with_snap:BuildRequires:	snapd-glib-2-devel >= 1.64}
%{?with_sysprof:BuildRequires:	sysprof-devel >= 3.37.2}
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-glib-devel
BuildRequires:	xz
Requires(post,postun):	glib2 >= 1:2.76.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	AppStream >= 0.16.4
%{?with_packagekit:Requires:	PackageKit >= 1.2.5}
%{?with_flatpak:Requires:	flatpak-libs >= 1.14.1}
%{?with_fwupd:Requires:	fwupd-libs >= 1.6.2}
Requires:	gdk-pixbuf2 >= 2.32.0
Requires:	glib2 >= 1:2.76.0
Requires:	gsettings-desktop-schemas >= 3.18.0
Requires:	gtk4 >= 4.16.0
Requires:	hicolor-icon-theme
Requires:	json-glib >= 1.6.0
Requires:	libadwaita >= 1.6
%{?with_malcontent:Requires:	libmalcontent >= 0.5.0}
Requires:	libsoup3 >= 3.0
Requires:	libxmlb >= 0.3.4
%{?with_mogwai:Requires:	mogwai >= 0.2.0}
%{?with_snap:Requires:	snapd-glib-2 >= 1.64}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		abiver	22
%define		gs_plugins_dir	%{_libdir}/gnome-software/plugins-%{abiver}

%description
GNOME Software lets you install and update applications and system
extensions.

%description -l pl.UTF-8
GNOME Software pozwala instalować i uaktualniać aplikacje oraz
rozszerzenia systemu.

%package devel
Summary:	Header files for GNOME Software plugins development
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia wtyczek GNOME Software
Group:		Development/Libraries
# doesn't require base
Requires:	AppStream-devel >= 0.16.4
Requires:	atk-devel
Requires:	glib2-devel >= 1:2.76.0
Requires:	gtk4-devel >= 4.16.0
Requires:	libsoup3-devel >= 3.0

%description devel
Header files for GNOME Software plugins development.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia wtyczek GNOME Software.

%package apidocs
Summary:	GNOME Software plugin API documentation
Summary(pl.UTF-8):	Dokumentacja API wtyczek GNOME Software
Group:		Documentation
BuildArch:	noarch

%description apidocs
GNOME Software plugin API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API wtyczek GNOME Software.

%prep
%setup -q

%build
%meson \
	--default-library=shared \
	%{?with_ext_appstream:-Dexternal_appstream=true} \
	%{!?with_flatpak:-Dflatpak=false} \
	%{!?with_fwupd:-Dfwupd=false} \
	%{?with_eos:-Deos_updater=true} \
	%{!?with_malcontent:-Dmalcontent=false} \
	%{?with_mogwai:-Dmogwai=true} \
	%{?with_packagekit:-Dpackagekit=true} \
	%{?with_rpm_ostree:-Drpm_ostree=true} \
	%{?with_snap:-Dsnap=true} \
	-Dsysprof=%{__enabled_disabled sysprof} \
	-Dtests=false
# packagekit_autoremove?

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/gnome-software

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name} --with-gnome

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
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_bindir}/gnome-software
/etc/xdg/autostart/org.gnome.Software.desktop
%attr(755,root,root) %{_libexecdir}/gnome-software-cmd
%attr(755,root,root) %{_libexecdir}/gnome-software-restarter
%dir %{_libdir}/gnome-software
%attr(755,root,root) %{_libdir}/gnome-software/libgnomesoftware.so.%{abiver}
%dir %{gs_plugins_dir}
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_appstream.so
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_dpkg.so
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_dummy.so
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_epiphany.so
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_fedora-langpacks.so
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_fedora-pkgdb-collections.so
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_generic-updates.so
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_hardcoded-blocklist.so
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_icons.so
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_modalias.so
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_os-release.so
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_provenance.so
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_provenance-license.so
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_repos.so
%{_datadir}/dbus-1/services/org.gnome.Software.service
%{_datadir}/glib-2.0/schemas/org.gnome.software.gschema.xml
%{_datadir}/gnome-shell/search-providers/org.gnome.Software-search-provider.ini
%{_datadir}/metainfo/org.gnome.Software.metainfo.xml
%{_datadir}/metainfo/org.gnome.Software.Plugin.Epiphany.metainfo.xml
%dir %{_datadir}/swcatalog
%dir %{_datadir}/swcatalog/xml
%{_datadir}/swcatalog/xml/gnome-pwa-list-foss.xml
%{_datadir}/swcatalog/xml/gnome-pwa-list-proprietary.xml
%if %{with eos}
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_eos-updater.so
%endif
%if %{with ext_appstream}
%attr(755,root,root) %{_libexecdir}/gnome-software-install-appstream
%{_datadir}/polkit-1/actions/org.gnome.software.external-appstream.policy
%endif
%if %{with flatpak}
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_flatpak.so
%{_datadir}/metainfo/org.gnome.Software.Plugin.Flatpak.metainfo.xml
%{_desktopdir}/gnome-software-local-file-flatpak.desktop
%endif
%if %{with fwupd}
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_fwupd.so
%{_datadir}/metainfo/org.gnome.Software.Plugin.Fwupd.metainfo.xml
%{_desktopdir}/gnome-software-local-file-fwupd.desktop
%endif
%if %{with malcontent}
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_malcontent.so
%endif
%if %{with packagekit}
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_packagekit.so
%{_datadir}/dbus-1/services/org.freedesktop.PackageKit.service
%{_desktopdir}/gnome-software-local-file-packagekit.desktop
%endif
%if %{with rpm_ostree}
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_rpm-ostree.so
%endif
%if %{with snap}
%attr(755,root,root) %{gs_plugins_dir}/libgs_plugin_snap.so
%{_datadir}/metainfo/org.gnome.Software.Plugin.Snap.metainfo.xml
%{_desktopdir}/gnome-software-local-file-snap.desktop
%endif
%{bash_compdir}/gnome-software
%{_desktopdir}/org.gnome.Software.desktop
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Software.svg
%{_iconsdir}/hicolor/scalable/categories/system-component-*.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Software-symbolic.svg
%{_mandir}/man1/gnome-software.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gnome-software/libgnomesoftware.so
%{_includedir}/gnome-software
%{_pkgconfigdir}/gnome-software.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gnome-software
