Summary:	Suite of programs that can record and replay user actions under X11
Summary(pl):	Zestaw programów do nagrywania i odtwarzania akcji u¿ytkownika pod X11
Name:		xnee
Version:	1.08
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	ftp://ftp.gnu.org/gnu/xnee/%{name}-%{version}.tar.gz
# Source0-md5:	cef82f631d06d6091ecb90436efa0e69
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/xnee/
BuildRequires:	XFree86-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Xnee is a suite of programs that can record, replay and distribute
user actions under the X11 environment. Think of it as a robot that
can imitate the job you just did. Xnee can be used to: automate tests,
demonstrate programs, distribute actions, record and replay "macros",
retype a file etc.

%description -l pl
Xnee to zestaw programów do nagrywania, odtwarzania i powielania akcji
u¿ytkownika w ¶rodowisku X11. Mo¿na je okre¶liæ jako maszynê
powtarzaj±c± pracê wykonan± przez nas. Xnee mo¿na u¿yæ do:
automatyzowania testów, demonstrowania programów, powielania akcji (na
wielu komputerach), nagrywania i odtwarzania "makr", przepisywania
plików itp.

%prep
%setup -q
%patch0 -p1

%build
%configure
%{__make} \
	GPROF_FLAG="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D xnee/doc/xnee.1 $RPM_BUILD_ROOT%{_mandir}/man1/xnee.1

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog EXAMPLES NEWS TODO USAGE
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/xnee.1*
%{_infodir}/xnee.info*
