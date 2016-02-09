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

%define __pip_cmd python -m pip

%description
This package provides zipnish-logreader, a daemon that plugs
into varnishlog and reads required time information
for spans and annotations.


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
find %{_builddir}/opt/zipnish/logreader/venv -type l | while read link; do
    target=$(readlink "$link")
    if [ -d "$target" ]; then
        echo "Replace symlink directory: $target -> $link"
        rm -rf "$link"
        cp -rL "$target" "$link"
    elif [ -f "$target" ]; then
        echo "Replace symlink file: $target -> $link"
        cp -L --remove-destination "$target" "$link"
    else
        echo "Unknown symlink. Leaving it."
    fi
done

source %{_builddir}/opt/zipnish/logreader/venv/bin/activate
export PATH="$PATH:%{_builddir}/opt/zipnish/logreader/venv/bin"

%{__pip_cmd} install simplemysql==1.0
%{__pip_cmd} install crochet==1.4.0
%{__pip_cmd} list

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
