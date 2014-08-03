# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.27
# 

Name:       NetworkManager

# >> macros
# << macros

Summary:    Network connection manager and user applications
Version:    0.9.10.0
Release:    1
Group:      System/Base
License:    GPLv2+
URL:        http://www.gnome.org/projects/NetworkManager/
Source0:    %{name}-%{version}.tar.xz
Source1:    NetworkManager.conf
Source2:    NetworkManager-wakeup.sh
Source100:  NetworkManager.yaml
Requires:   dbus
Requires:   dhclient
Requires:   iproute
Requires:   wpa_supplicant
Requires:   ppp
Requires:   udev
Requires:   mobile-broadband-provider-info
Requires:   systemd
Requires(preun): /bin/systemctl
Requires(preun): systemd
Requires(post): /bin/systemctl
Requires(post): systemd
Requires(postun): /bin/systemctl
Requires(postun): systemd
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(nss)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(udev)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(libiptc)
BuildRequires:  pkgconfig(iso-codes)
BuildRequires:  pkgconfig(libnl-3.0)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  glib2
BuildRequires:  dbus-glib
BuildRequires:  wireless-tools-devel
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  wpa_supplicant
BuildRequires:  perl(XML::Parser)
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  intltool
BuildRequires:  libtool
BuildRequires:  ppp-devel
BuildRequires:  desktop-file-utils
BuildRequires:  readline-devel
BuildRequires:  libndp-devel

%description
NetworkManager is a system network service that manages your network devices
and connections, attempting to keep active network connectivity when available.
It manages ethernet, WiFi, mobile broadband (WWAN), and PPPoE devices, and
provides VPN integration with a variety of different VPN services.


%package glib
Summary:    Libraries for adding NetworkManager support to applications that use glib
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   dbus
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description glib
This package contains the libraries that make it easier to use some NetworkManager
functionality from applications that use glib.


%package glib-devel
Summary:    Header files for adding NetworkManager support to applications that use glib
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-devel = %{version}-%{release}
Requires:   %{name}-glib = %{version}-%{release}
Requires:   glib2-devel
Requires:   pkgconfig
Requires:   dbus-glib-devel

%description glib-devel
This package contains the header and pkg-config files for development applications using
NetworkManager functionality from applications that use glib.


%package devel
Summary:    Libraries and headers for adding NetworkManager support to applications
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   dbus-devel
Requires:   pkgconfig

%description devel
This package contains various headers accessing some NetworkManager functionality
from applications.


%prep
%setup -q -n %{name}-%{version}/upstream

# >> setup
# << setup

%build
# >> build pre
autoreconf --force --install --verbose
intltoolize --automake --copy --force
export CFLAGS="$CFLAGS -Wno-error=deprecated-declarations"
# << build pre

%configure --disable-static \
    --with-distro=redhat \
    --with-dhclient=yes \
    --with-dhcpcd=no \
    --with-crypto=nss \
    --enable-more-warnings=yes \
    --enable-wimax=no \
    --enable-polkit=yes \
    --with-system-ca-path=%{_sysconfdir}/pki/tls/certs \
    --with-tests=yes \
    --enable-ifcfg-rh

make %{?_smp_mflags}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre

# << install pre
%make_install

# >> install post
%{__cp} %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/

mkdir -p %{buildroot}/lib/systemd/system-sleep
chmod 0755 %{buildroot}/lib/systemd/system-sleep
cp %{SOURCE2} %{buildroot}/lib/systemd/system-sleep/NetworkManager-wakeup.sh
chmod 0755 %{buildroot}/lib/systemd/system-sleep/NetworkManager-wakeup.sh
mkdir -p %{buildroot}/%{_lib}/systemd/system/multi-user.target.wants
ln -s ./NetworkManager.service %{buildroot}/%{_lib}/systemd/system/dbus-org.freedesktop.NetworkManager.service
ln -s ../NetworkManager.service %{buildroot}/%{_lib}/systemd/system/multi-user.target.wants/NetworkManager.service

# Ditch documentation nm decides to build for no good reason :@
rm -rvf %{buildroot}/usr/share/doc
rm -rvf %{buildroot}/usr/share/gtk-doc
rm -rvf %{buildroot}/usr/share/man
# << install post

%find_lang %{name}

%preun
if [ "$1" -eq 0 ]; then
systemctl stop dbus-org.freedesktop.NetworkManager.service
fi

%post
systemctl daemon-reload
systemctl reload-or-try-restart dbus-org.freedesktop.NetworkManager.service

%postun
systemctl daemon-reload

%post glib -p /sbin/ldconfig

%postun glib -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
# >> files
%defattr(-,root,root,0755)
%doc COPYING NEWS AUTHORS README CONTRIBUTING TODO
%config %{_sysconfdir}/dbus-1/system.d/*
%{_sbindir}/%{name}
%{_bindir}/nmcli
%{_datadir}/bash-completion/completions/nmcli
%dir %{_sysconfdir}/%{name}/
%dir %{_sysconfdir}/%{name}/dispatcher.d
%config(noreplace) %{_sysconfdir}/%{name}/NetworkManager.conf
%{_bindir}/nm-online
%{_libexecdir}/*
%dir %{_libdir}/NetworkManager
%{_libdir}/NetworkManager/*.so*
#%{_mandir}/man1/*
#%{_mandir}/man5/*
#%{_mandir}/man8/*
%dir %{_localstatedir}/run/NetworkManager
%dir %{_localstatedir}/lib/NetworkManager
#%{_prefix}/libexec/nm-crash-logger
#%dir %{_datadir}/NetworkManager
#%{_datadir}/NetworkManager/gdb-cmd
%dir %{_sysconfdir}/NetworkManager/system-connections
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_libdir}/pppd/*/nm-pppd-plugin.so
%{_datadir}/polkit-1/actions/*.policy
/lib/udev/rules.d/*.rules
# systemd stuff
%{_libdir}/systemd/*
/%{_lib}/systemd/system-sleep/*
/%{_lib}/systemd/system/dbus-org.freedesktop.NetworkManager.service
/%{_lib}/systemd/system/multi-user.target.wants/NetworkManager.service
%{_datadir}/dbus-1/system-services/org.freedesktop.NetworkManager.service
# << files

%files glib
%defattr(-,root,root,-)
# >> files glib
%defattr(-,root,root,0755)
%{_libdir}/libnm-glib.so.*
%{_libdir}/libnm-glib-vpn.so.*
%{_libdir}/libnm-util.so.*
# << files glib

%files glib-devel
%defattr(-,root,root,-)
# >> files glib-devel
%defattr(-,root,root,0755)
%dir %{_includedir}/libnm-glib
%{_includedir}/libnm-glib/*.h
%{_includedir}/%{name}/nm-setting*.h
%{_includedir}/%{name}/nm-connection.h
%{_includedir}/%{name}/nm-utils.h
%{_includedir}/%{name}/nm-utils-enum-types.h
%{_libdir}/pkgconfig/libnm-glib.pc
%{_libdir}/pkgconfig/libnm-glib-vpn.pc
%{_libdir}/pkgconfig/libnm-util.pc
%{_libdir}/libnm-glib.so
%{_libdir}/libnm-glib-vpn.so
%{_libdir}/libnm-util.so
# << files glib-devel

%files devel
%defattr(-,root,root,-)
# >> files devel
%defattr(-,root,root,0755)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/%{name}.h
%{_includedir}/%{name}/NetworkManagerVPN.h
%{_includedir}/%{name}/nm-version.h
%{_libdir}/pkgconfig/%{name}.pc
# << files devel
