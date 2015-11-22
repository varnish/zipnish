Name: log-reader
Summary: LogReader service for fetching Varnishlog data.
Release: 1%{?dist}
Group: Application/Tools
License: GPL
Version: 1.0
Vendor: Varnish Software
Source0: %{expand:%%(pwd)}
URL: https://www.varnish-software.com/

%if 0%{?el6}
%define __pip_cmd pip
%endif

%if 0%{?el7}
%define __pip_cmd python -m pip
%endif


%description
This package provides log-reader, a daemon that fetches
Varnishlog data.


%prep
mkdir -p %{_builddir}/var/log/zipnish/
mkdir -p %{_builddir}/etc/zipnish/
mkdir -p %{_builddir}/opt/zipnish/log/

cp %{SOURCEURL0}/default.cfg %{_builddir}/etc/zipnish/zipnish.cfg
cp %{SOURCEURL0}/app.py %{_builddir}/opt/zipnish/app.py
cp %{SOURCEURL0}/varnishapi.py %{_builddir}/opt/zipnish/varnishapi.py
cp %{SOURCEURL0}/requirements.txt %{_builddir}/etc/zipnish/requirements.cfg
cp -r %{SOURCEURL0}/log %{_builddir}/opt/zipnish

%{__pip_cmd} install simplemysql
%{__pip_cmd} install crochet
%{__pip_cmd} install tabulate


%install
rm -rf %{buildroot}
cp -r %{_builddir} %{buildroot}
exit 0


%files
%defattr(-,root,root,-)
%config(noreplace) /etc/zipnish/zipnish.cfg
%config(noreplace) /etc/zipnish/requirements.cfg
%attr(0755,zipnish,zipnish) /var/log/zipnish/
%attr(0755,zipnish,zipnish) /opt/zipnish/app.py
%attr(0755,zipnish,zipnish) /opt/zipnish/log
%attr(0755,zipnish,zipnish) /opt/zipnish/varnishapi.py

%pre
# Create user and group
/usr/bin/getent group zipnish > /dev/null || /usr/sbin/groupadd -r zipnish
/usr/bin/getent passwd zipnish > /dev/null || /usr/sbin/useradd -r -g zipnish -d /opt/zipnish -s /sbin/nologin zipnish

%clean
rm -rf %{_builddir}