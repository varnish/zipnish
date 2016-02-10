Name: zipnish-logreader
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

%description
This package provides zipnish-logreader, a daemon that plugs
into varnishlog and reads required time information
for spans and annotations.

%define __pip_cmd pip
%define __python_cmd python

%prep
mkdir -p %{_builddir}/var/log/zipnish/
mkdir -p %{_builddir}/etc/zipnish/
mkdir -p %{_builddir}/opt/zipnish/logreader/log/
mkdir -p %{_builddir}/usr/lib/systemd/system/
mkdir -p %{_builddir}/etc/init.d/

cp %{SOURCEURL0}/logreader/default.cfg %{_builddir}/etc/zipnish/zipnish.cfg
cp %{SOURCEURL0}/logreader/app.py %{_builddir}/opt/zipnish/logreader/app.py
cp %{SOURCEURL0}/logreader/varnishapi.py %{_builddir}/opt/zipnish/logreader/varnishapi.py
cp -r %{SOURCEURL0}/logreader/* %{_builddir}/opt/zipnish/logreader/

cp %{SOURCEURL0}/logreader/redhat/zipnish-logreader.service %{_builddir}/usr/lib/systemd/system/zipnish-logreader.service

# Build virtual environment
virtualenv %{_builddir}/opt/zipnish/logreader/venv

# Replace symlinks in the venv to decouple it from the system python, which
# may differ from the system python we're using in our build environment.
source %{_builddir}/opt/zipnish/logreader/venv/bin/activate
export PATH="$PATH:%{_builddir}/opt/zipnish/logreader/venv/bin"


%{__python_cmd} %{_builddir}/opt/zipnish/logreader/venv/bin/pip install simplemysql==1.0
%{__python_cmd} %{_builddir}/opt/zipnish/logreader/venv/bin/pip install crochet==0.7.0
%{__python_cmd} %{_builddir}/opt/zipnish/logreader/venv/bin/pip list

virtualenv --relocatable %{_builddir}/opt/zipnish/logreader/venv

# Fix broken --relocateable option which does not fix the VIRTUAL_ENV setting of the activate script
sed -i 's|%{_builddir}/opt/zipnish/logreader/venv|/opt/zipnish/logreader/venv|g' %{_builddir}/opt/zipnish/logreader/venv/bin/activate

%install
rm -rf %{buildroot}
cp -r %{_builddir} %{buildroot}
exit 0


%files
%defattr(-,root,root,-)
%config(noreplace) /etc/zipnish/zipnish.cfg
%attr(0755,zipnish,zipnish) /var/log/zipnish/
%attr(0755,root,root) /opt/zipnish/logreader/
%attr(0755,root,root) /usr/lib/systemd/system/zipnish-logreader.service

%pre
# Create user and group
/usr/bin/getent group zipnish > /dev/null || /usr/sbin/groupadd -r zipnish
/usr/bin/getent passwd zipnish > /dev/null || /usr/sbin/useradd -r -g zipnish -d /opt/zipnish/logreader -s /sbin/nologin zipnish

%clean
rm -rf %{_builddir}
