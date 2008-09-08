Summary:	Jalbum web album software
Name:		jalbum
Version:	8.0.9
Release:	0.1
License:	freeware
Group:		Applications/WWW
Source0:	http://jalbum.net/download/8.0/Linux/NoVM/Jalbuminstall.bin
# Source0-md5:	0e10280a6202fd9ae86336e0a0020e1b
URL:		http://jalbum.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	jre
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}

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
dd if=%{SOURCE0} of="$RESOURCE_ZIP" bs=$BLOCKSIZE skip=$(expr $ARCHSTART + $INSTALLER_BLOCKS) count=$RESSIZE

unzip -qq Resource1.zip
mv C_/Dev/Java/JAlbum/* .
rm -f dist/JAlbum/lib/windows_zg_ia_sf.jar
rm -f dist/JAlbum/lib/sunos_zg_ia_sf.jar

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -a dist/JAlbum/JAlbum.jar $RPM_BUILD_ROOT%{_appdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_appdir}
