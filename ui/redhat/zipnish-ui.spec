Name: zipnish-ui
Summary: Zipnish UI service for visualizing Microservices performance.
Release: 1%{?dist}
Group: Application/Tools
License: GPL
Version: 1.0
Vendor: Varnish Software
Source0: %{expand:%%(pwd)}
URL: https://www.varnish-software.com/


%description
This package provides an user interface for the Zipnish microservice tracker.


%prep
mkdir -p %{_builddir}/etc/zipnish/
mkdir -p %{_builddir}/opt/zipnish/ui/app/
mkdir -p %{_builddir}/usr/lib/systemd/system/
mkdir -p %{_builddir}/etc/init.d/

cp %{SOURCEURL0}/app.py %{_builddir}/opt/zipnish/ui/app.py
cp %{SOURCEURL0}/config.py %{_builddir}/opt/zipnish/ui/config.py
cp %{SOURCEURL0}/manage.py %{_builddir}/opt/zipnish/ui/manage.py
cp %{SOURCEURL0}/ui.cfg %{_builddir}/etc/zipnish/ui.cfg
cp -r %{SOURCEURL0}/app %{_builddir}/opt/zipnish/ui

cp %{SOURCEURL0}/redhat/zipnish-ui.service %{_builddir}/usr/lib/systemd/system/zipnish-ui.service
cp %{SOURCEURL0}/redhat/zipnish-ui.service %{_builddir}/etc/init.d/zipnish-ui.service


%install
rm -rf %{buildroot}
cp -r %{_builddir} %{buildroot}
exit 0


%files
%defattr(-,root,root,-)
%config(noreplace) /etc/zipnish/ui.cfg
%attr(0755,zipnish-ui,zipnish-ui) /opt/zipnish/ui/app
%attr(0755,zipnish-ui,zipnish-ui) /opt/zipnish/ui/app.py
%attr(0755,zipnish-ui,zipnish-ui) /opt/zipnish/ui/config.py
%attr(0755,zipnish-ui,zipnish-ui) /opt/zipnish/ui/manage.py
%attr(0755,root,root) /usr/lib/systemd/system/zipnish-ui.service
%attr(0755,root,root) /etc/init.d/zipnish-ui.service

%pre
# Create user and group
/usr/bin/getent group zipnish-ui > /dev/null || /usr/sbin/groupadd -r zipnish-ui
/usr/bin/getent passwd zipnish-ui > /dev/null || /usr/sbin/useradd -r -g zipnish-ui -d /opt/zipnish/ui -s /sbin/nologin zipnish-ui

%clean
rm -rf %{_builddir}