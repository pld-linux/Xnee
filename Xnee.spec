# TODO:
# - package libxnee if needed for anything (it's noinst now)
# - generate docs - (some files are missing)
#
# Conditional build:
%bcond_with	doc	# documentation (broken, missing files)
%bcond_with	gnome	# GNOME 2 panel applet (not ready for GNOME 3)
#
Summary:	Suite of programs that can record and replay user actions under X11
Summary(pl.UTF-8):	Zestaw programów do nagrywania i odtwarzania akcji użytkownika pod X11
Name:		Xnee
Version:	3.18
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	http://ftp.gnu.org/gnu/xnee/xnee-%{version}.tar.gz
# Source0-md5:	2ffd7832026c871d0fb0f63e06c71519
Patch0:		%{name}-info.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-am.patch
URL:		http://www.gnu.org/software/xnee/www/index.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	texinfo
BuildRequires:	xorg-proto-recordproto-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXtst-devel
%if %{with gnome}
BuildRequires:	GConf2-devel >= 2.0
BuildRequires:	gnome-panel-devel >= 2.0
BuildRequires:	gnome-panel-devel < 3
%endif
%if %{with doc}
BuildRequires:	ImageMagick
BuildRequires:	ImageMagick-coder-jpeg
BuildRequires:	ImageMagick-coder-png
BuildRequires:	dia
BuildRequires:	ghostscript
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-plain
BuildRequires:	tetex-tex-misc
BuildRequires:	texinfo-texi2dvi
%endif
Provides:	xnee
Obsoletes:	xnee
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Xnee is a suite of programs that can record, replay and distribute
user actions under the X11 environment. Think of it as a robot that
can imitate the job you just did. Xnee can be used to: automate tests,
demonstrate programs, distribute actions, record and replay "macros",
retype a file etc.

%description -l pl.UTF-8
Xnee to zestaw programów do nagrywania, odtwarzania i powielania akcji
użytkownika w środowisku X11. Można je określić jako maszynę
powtarzającą pracę wykonaną przez nas. Xnee można użyć do:
automatyzowania testów, demonstrowania programów, powielania akcji (na
wielu komputerach), nagrywania i odtwarzania "makr", przepisywania
plików itp.

%package gtk
Summary:	gnee - GTK+ based graphical frontent to GNU Xnee
Summary(pl.UTF-8):	gnee - oparty na GTK+ graficzny interfejs do GNU Xnee
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gtk
gnee is the graphical frontend to GNU Xnee, based on GTK+ toolkit.

%description gtk -l pl.UTF-8
gnee to graficzny interfejs do GNU Xnee, oparty na GTK+.

%package gnome
Summary:	pnee - GNOME panel applet for GNU Xnee
Summary(pl.UTF-8):	pnee - aplet panelu GNOME dla GNU Xnee
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gnome
pnee is the GNOME panel applet for GNU Xnee.

%description gnome -l pl.UTF-8
pnee to aplet panelu GNOME dla GNU Xnee.

%prep
%setup -q -n xnee-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# disable static as no API is installed
%configure \
	--disable-doc \
	--disable-static \
	--disable-static-programs \
	%{?with_gnome:--enable-gnome-applet} \
	--enable-gui \
	--enable-lib \
	--enable-xosd

%{__make} \
	CNEE_INFO="cnee.info"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	CNEE_INFO="cnee.info" \
	PANEL_APPLET_DIR=$RPM_BUILD_ROOT%{_bindir} \
	PANEL_SERVER_DIR=$RPM_BUILD_ROOT%{_libdir}/bonobo/servers

# API not installed
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libxnee.{so,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/sbin/ldconfig
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/sbin/ldconfig
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog FAQ NEWS README TODO
%attr(755,root,root) %{_bindir}/cnee
%attr(755,root,root) %{_libdir}/libxnee.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxnee.so.0
%dir %{_datadir}/xnee
%{_datadir}/xnee/*.sh
%{_datadir}/xnee/*.xns
%{_pixmapsdir}/xnee.png
%{_pixmapsdir}/xnee.xpm
%{_mandir}/man1/cnee.1*
%{_mandir}/man1/xnee.1*
%{_infodir}/cnee.info*

%files gtk
%defattr(644,root,root,755)
%doc gnee/AUTHORS
%attr(755,root,root) %{_bindir}/gnee
%{_mandir}/man1/gnee.1*

%if %{with gnome}
%files gnome
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pnee
%{_libdir}/bonobo/servers/pnee.server
%dir %{_datadir}/xnee/pixmaps
%{_datadir}/xnee/pixmaps/pnee-*.png
%{_mandir}/man1/pnee.1*
%endif
