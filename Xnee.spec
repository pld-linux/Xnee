# TODO:
# - rename spec xnee.spec -> Xnee.spec
# - separate subpackages: libs, tools
# - generate docs - deps are crazy...
Summary:	Suite of programs that can record and replay user actions under X11
Summary(pl.UTF-8):   Zestaw programów do nagrywania i odtwarzania akcji użytkownika pod X11
Name:		Xnee
Version:	2.01
Release:	0.1
License:	GPL v2
Group:		X11/Applications
Source0:	ftp://ftp.gnu.org/gnu/xnee/%{name}-%{version}.tar.gz
# Source0-md5:	c22cb4ce520bdf27867b823e57b6e7da
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/xnee/www/index.html
BuildRequires:	XFree86-devel
BuildRequires:	gtk+2-devel
BuildRequires:	pkg-config > 0.9.0
# needed for docs only :-/ :
#BuildRequires:	ImageMagick
#BuildRequires:	ImageMagick-coder-jpeg
#BuildRequires:	ImageMagick-coder-png
#BuildRequires:	dia
#BuildRequires:	ghostscript
#BuildRequires:	tetex-dvips
#BuildRequires:	tetex-format-plain
#BuildRequires:	tetex-tex-misc
#BuildRequires:	texinfo
#BuildRequires:	texinfo-texi2dvi
Obsoletes:	xnee
Provides:	xnee
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

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--enable-xosd \
	--disable-doc

%{__make} \
	GPROF_FLAG="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#install -D xnee/doc/xnee.1 $RPM_BUILD_ROOT%{_mandir}/man1/xnee.1

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog EXAMPLES NEWS TODO
%attr(755,root,root) %{_bindir}/cnee
%attr(755,root,root) %{_bindir}/gnee
%{_libdir}/libxnee.a
#%{_mandir}/man1/xnee.1*
#%{_infodir}/xnee.info*
