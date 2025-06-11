Name:           libosmo-sigtran
Version:        2.1.1
Release:        1.dcbw%{?dist}
Summary:        Osmocom SCCP, SIGTRAN and STP
License:        AGPL-3.0-or-later AND GPL-2.0-or-later

URL:            https://osmocom.org/projects/libosmo-sccp/wiki

BuildRequires:  git make autoconf automake libtool doxygen systemd-devel
BuildRequires:  lksctp-tools-devel libtalloc-devel
BuildRequires:  libosmocore-devel >= 1.10.0
BuildRequires:  libosmo-netif-devel >= 1.6.0

Requires: osmo-usergroup

Patch1: 0001-build-fixes.patch
Source0: %{name}-%{version}.tar.bz2


%description
C-language library implementation of a variety of telecom
signaling protocols, such as M3UA, SUA, SCCP (connection
oriented and connectionless), as well as the OsmoSTP,
a SS7 Transfer Point.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.


%prep
%autosetup -p1

%build
%global optflags %(echo %optflags | sed 's|-Wp,-D_GLIBCXX_ASSERTIONS||g')
echo "%{version}" >.tarball-version
autoreconf -fiv
%configure --enable-shared \
           --disable-static \
           --enable-manual \
           --with-systemdsystemunitdir=%{_unitdir}

sed -i -e 's|tests||g' Makefile
# Fix unused direct shlib dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
# Remove libtool archives
find %{buildroot} -name '*.la' -exec rm -f {} \;
find %{buildroot} -name '*.a' -exec rm -f {} \;
# versioning
sed -i 's|UNKNOWN|%{version}|' %{buildroot}%{_libdir}/pkgconfig/*.pc


%check
make check

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%post
%systemd_post %{name}.service

%ldconfig_scriptlets

%files
%doc %{_docdir}/*
%license COPYING
%{_bindir}/*
%{_unitdir}/osmo-stp.service
%attr(0644,root,root) %config(missingok,noreplace) %{_sysconfdir}/osmocom/osmo-stp.cfg
%{_libdir}/*.so.*

%files devel
%{_includedir}/osmocom/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun Jun  8 2025 Dan Williams <dan@ioncontrol.co> - 2.1.1
- Update to 2.1.1

* Sun Aug 26 2018 Cristian Balint <cristian.balint@gmail.com>
- git update releases
