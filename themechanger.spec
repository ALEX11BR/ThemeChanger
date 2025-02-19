%global appid com.github.alex11br.themechanger

Name:           themechanger
Version:        0.12.1
Release:        %autorelease
Summary:        Theme changing utility for Linux destops

License:        GPL-2.0-or-later
URL:            https://github.com/ALEX11BR/ThemeChanger
Source0:        https://github.com/ALEX11BR/ThemeChanger/archive/refs/tags/v%{version}.tar.gz#/%{name}-v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  desktop-file-utils
BuildRequires:  gtk3
BuildRequires:  meson >= 0.50.0
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(pygobject-3.0)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  python3-devel
BuildRequires:  python3-gobject-devel
BuildRequires:  /usr/bin/appstream-util
BuildRequires:  /usr/bin/glib-compile-resources
BuildRequires:  /usr/bin/pkg-config

Requires:       gobject-introspection%{?_isa}
Requires:       gtk3%{?_isa}
Requires:       hicolor-icon-theme
Requires:       python3{?_isa}
Requires:       python3-gobject-base%{?_isa}

%description
This app is a theme changing utility for Linux, BSDs, and whatnots.
It lets the user change GTK 2/3/4, Kvantum, icon and cursor themes, even for
libadwaita apps, edit GTK CSS with live preview, and set some related options.
It also lets the user install icon and widget theme archives.

Features:

   * Set the GTK3 theme, sync the GTK2, GTK4, Kvantum themes with it
     or choose another one for each of these toolkits
   * Set the icon theme
   * Set the cursor theme, and tweak the cursor's size
   * Set all these themes with a special searchable selector with
     previews for GTK3, icon and cursor themes
   * Set various options like whether buttons have images or not
   * Instantaneously apply your setting changes to the running
     applications in GNOME, Cinnamon, Mate, XFCE, LXDE using
     lxsession, or using xsettingsd (you must download xsettingsd and
     run it in the background) for those that don't use GTK desktop
     environments
   * Edit GTK CSS with instantaneous feedback of the changes made
   * Install new widget or icon themes from archives available e.g.
     at https://gnome-look.org/

%prep
%autosetup -n ThemeChanger-%{version}

%build
%meson
%meson_build

%install
%meson_install

%check
desktop-file-validate \
    %{buildroot}%{_datadir}/applications/%{appid}.desktop

appstream-util validate-relax --nonet \
    %{buildroot}%{_metainfodir}/%{appid}.appdata.xml

%files
%license LICENSE
%doc README.md screenshot1.png
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{appid}.desktop
%{_metainfodir}/%{appid}.appdata.xml

%changelog
* Wed Feb 19 2025 Popa Ioan-Alexandru <https://alex11br.github.io/> - 0.12.1-1
- Update to 0.12.1

* Tue Jul 16 2024 Joel Barrios <http://www.alcancelibre.org/> - 0.12.0-1
- Update to 0.12.0

* Mon Sep 05 2022 Joel Barrios <http://www.alcancelibre.org/> - 0.11.1-1
- Initial spec file.
