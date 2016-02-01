Name: zipnish-log-reader
Summary: Zipnish LogReader service for fetching Varnishlog data.
Release: 1%{?dist}
Group: Application/Tools
License: GPL
Version: 1.0
Vendor: Varnish Software
Source0: %{expand:%%(pwd)}
URL: https://www.varnish-software.com/
BuildRequires: python-virtualenv
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(post): /sbin/chkconfig

%define __pip_cmd pip

%description
This package provides log-reader, a daemon that fetches
Varnishlog data.


%prep
mkdir -p %{_builddir}/var/log/zipnish/
mkdir -p %{_builddir}/etc/zipnish/
mkdir -p %{_builddir}/opt/zipnish/log-reader/log/
mkdir -p %{_builddir}/usr/lib/systemd/system/
mkdir -p %{_builddir}/etc/init.d/

cp %{SOURCEURL0}/log-reader/default.cfg %{_builddir}/etc/zipnish/zipnish.cfg
cp %{SOURCEURL0}/log-reader/app.py %{_builddir}/opt/zipnish/log-reader/app.py
cp %{SOURCEURL0}/log-reader/varnishapi.py %{_builddir}/opt/zipnish/log-reader/varnishapi.py
cp -r %{SOURCEURL0}/log-reader/* %{_builddir}/opt/zipnish/log-reader/

cp %{SOURCEURL0}/log-reader/redhat/log-reader.service %{_builddir}/usr/lib/systemd/system/log-reader.service
cp %{SOURCEURL0}/log-reader/redhat/log-reader.service %{_builddir}/etc/init.d/log-reader.service

# Build virtual environment
virtualenv %{_builddir}/opt/zipnish/log-reader/venv

source %{_builddir}/opt/zipnish/log-reader/venv/bin/activate
export PATH="$PATH:%{_builddir}/opt/zipnish/log-reader/venv/bin"

%{__pip_cmd} install simplemysql
%{__pip_cmd} install crochet

virtualenv --relocatable %{_builddir}/opt/zipnish/log-reader/venv

# Fix broken --relocateable option which does not fix the VIRTUAL_ENV setting of the activate script
sed -i 's|.*/opt/zipnish/log-reader/venv|/opt/zipnish/log-reader/venv|g' %{_builddir}/opt/zipnish/log-reader/venv/bin/activate

%install
rm -rf %{buildroot}
cp -r %{_builddir} %{buildroot}
exit 0


%files
%defattr(-,root,root,-)
%config(noreplace) /etc/zipnish/zipnish.cfg
%attr(0755,zipnish,zipnish) /var/log/zipnish/
%attr(0755,root,root) /opt/zipnish/log-reader/
%attr(0755,root,root) /usr/lib/systemd/system/log-reader.service
%attr(0755,root,root) /etc/init.d/log-reader.service

%pre
# Create user and group
/usr/bin/getent group zipnish > /dev/null || /usr/sbin/groupadd -r zipnish
/usr/bin/getent passwd zipnish > /dev/null || /usr/sbin/useradd -r -g zipnish -d /opt/zipnish/log-reader -s /sbin/nologin zipnish

%clean
rm -rf %{_builddir}
