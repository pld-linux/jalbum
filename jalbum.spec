Summary:	Jalbum web album software
Name:		jalbum
Version:	8.0
Release:	0.1
License:	freeware
Group:		Applications/WWW
Source0:	http://jalbum.net/download/%{version}/Linux/NoVM/Jalbuminstall.bin
# Source0-md5:	0e10280a6202fd9ae86336e0a0020e1b
URL:		http://jalbum.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	jre
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
With Jalbum it's easy to create your own photo album site. Just the
way you want it.

%prep
%setup -qcT

# emulate the self-extractable installer
head -n 256 %{SOURCE0} > header
ARCHREALSIZE=$(awk -F= '/^ARCHREALSIZE=/{print $2}' header)
BLOCKSIZE=$(awk -F= '/^BLOCKSIZE=/{print $2}' header)
RESSIZE=$(awk -F= '/^RESSIZE=/{print $2}' header)
ARCHSTART=$(awk -F= '/^ARCHSTART=/{print $2}' header)
RESOURCE_ZIP=Resource1.zip
INSTALLER_BLOCKS=$(expr $ARCHREALSIZE / $BLOCKSIZE)
INSTALLER_REMAINDER=$(expr $ARCHREALSIZE % $BLOCKSIZE || :)
if [ ${INSTALLER_REMAINDER:-0} -gt 0 ]; then
	INSTALLER_BLOCKS=$(expr $INSTALLER_BLOCKS + 1)
fi
dd if=%{SOURCE0} of="$RESOURCE_ZIP" bs=$BLOCKSIZE skip=`expr $ARCHSTART + $INSTALLER_BLOCKS` count=$RESSIZE

unzip -qq Resource1.zip
mv C_/Dev/Java/JAlbum/* .

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{name}" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -a dist/JAlbum/JAlbum.jar $RPM_BUILD_ROOT%{_appdir}

cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%{_appdir}
