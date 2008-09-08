# TODO
# - system java deps from lib/ dir
Summary:	Jalbum web album software
Name:		jalbum
Version:	8.0.9
Release:	0.6
License:	freeware
Group:		Applications/Publishing
Source0:	http://jalbum.net/download/8.0/Linux/NoVM/Jalbuminstall.bin
# Source0-md5:	0e10280a6202fd9ae86336e0a0020e1b
Source1:	%{name}.desktop
Source2:	%{name}.png
URL:		http://jalbum.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	jre
# ifarch and x86 tray library
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifnarch %{ix86}
# only on x86 something to strip
%define		_enable_debug_packages	0
%endif

%define		_appdir		%{_libdir}/%{name}

%description
With Jalbum it's easy to create your own photo album site. Just the
way you want it.

%prep
%setup -qcT

# emulate the InstallAnywhere UNIX Self Extractor
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

for jar in $(find -name '*_zg_ia_sf.jar'); do
	dir=${jar%*_zg_ia_sf.jar}
	unzip -qq -a $jar -d $dir
	rm -f $jar
done

%ifarch %{ix86}
chmod +x dist/JAlbum/lib/linux/x86/libtray.so
%else
rm -rf dist/JAlbum/lib/linux/x86
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_appdir}}
cp -a dist/JAlbum/* $RPM_BUILD_ROOT%{_appdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_bindir}/%{name}
#!/bin/sh
exec %{_bindir}/java -Xmx512M -jar %{_appdir}/JAlbum.jar
EOF

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%{_pixmapsdir}/%{name}.png
%{_desktopdir}/%{name}.desktop
%dir %{_appdir}
%{_appdir}/JAlbum.jar
%{_appdir}/ext
%{_appdir}/includes
%{_appdir}/lib
%{_appdir}/license
%{_appdir}/plugins
%{_appdir}/res
%{_appdir}/system
%{_appdir}/tools

%dir %{_appdir}/texts
%{_appdir}/texts/texts.properties
%lang(bg) %{_appdir}/texts/texts_bg.properties
%lang(ca) %{_appdir}/texts/texts_ca.properties
%lang(cs) %{_appdir}/texts/texts_cs.properties
%lang(da) %{_appdir}/texts/texts_da.properties
%lang(de) %{_appdir}/texts/texts_de.properties
%lang(et) %{_appdir}/texts/texts_ee.properties
%lang(el) %{_appdir}/texts/texts_el.properties
%lang(es) %{_appdir}/texts/texts_es.properties
%lang(fi) %{_appdir}/texts/texts_fi.properties
%lang(fr) %{_appdir}/texts/texts_fr.properties
%lang(hr) %{_appdir}/texts/texts_hr.properties
%lang(hu) %{_appdir}/texts/texts_hu.properties
%lang(it) %{_appdir}/texts/texts_it.properties
%lang(ja) %{_appdir}/texts/texts_ja.properties
%lang(ko) %{_appdir}/texts/texts_ko.properties
%lang(nl) %{_appdir}/texts/texts_nl.properties
%lang(no) %{_appdir}/texts/texts_no.properties
%lang(pl) %{_appdir}/texts/texts_pl.properties
%lang(pt) %{_appdir}/texts/texts_pt.properties
%lang(ro) %{_appdir}/texts/texts_ro.properties
%lang(ru) %{_appdir}/texts/texts_ru.properties
%lang(sh) %{_appdir}/texts/texts_sh.properties
%lang(sk) %{_appdir}/texts/texts_sk.properties
%lang(sl) %{_appdir}/texts/texts_sl.properties
%lang(sr) %{_appdir}/texts/texts_sr.properties
%lang(sv) %{_appdir}/texts/texts_sv.properties
%lang(th) %{_appdir}/texts/texts_th.properties
%lang(tr) %{_appdir}/texts/texts_tr.properties
%lang(uk) %{_appdir}/texts/texts_uk.properties
%lang(zh_CN) %{_appdir}/texts/texts_zh_CN.properties
%lang(zh_TW) %{_appdir}/texts/texts_zh_TW.properties

%dir %{_appdir}/skins
%dir %{_appdir}/skins/*
%{_appdir}/skins/*/*.htt
%{_appdir}/skins/*/*.txt
%{_appdir}/skins/*/*.bsh
%{_appdir}/skins/*/*.jpg
%{_appdir}/skins/*/*.jap
%{_appdir}/skins/*/res
%{_appdir}/skins/*/styles
%{_appdir}/skins/*/plugins
%{_appdir}/skins/*/png
%{_appdir}/skins/*/includes
%{_appdir}/skins/*/help
%{_appdir}/skins/*/config
%{_appdir}/skins/*/guestbook
%dir %{_appdir}/skins/*/texts
%{_appdir}/skins/Chameleon/texts/texts.properties
%{_appdir}/skins/Chameleon/texts/texts_en.properties
%{_appdir}/skins/Minimal/texts/texts.properties
%{_appdir}/skins/Nature/texts/texts.properties
%{_appdir}/skins/Standard/texts/texts.properties
%{_appdir}/skins/Standard/texts/texts_en.properties
%{_appdir}/skins/Wedding/texts/texts.properties
%lang(bs) %{_appdir}/skins/Chameleon/texts/texts_bs.properties
%lang(cs) %{_appdir}/skins/Chameleon/texts/texts_cs.properties
%lang(da) %{_appdir}/skins/Chameleon/texts/texts_da.properties
%lang(de) %{_appdir}/skins/Chameleon/texts/texts_de.properties
%lang(es) %{_appdir}/skins/Chameleon/texts/texts_es.properties
%lang(fi) %{_appdir}/skins/Chameleon/texts/texts_fi.properties
%lang(fr) %{_appdir}/skins/Chameleon/texts/texts_fr.properties
%lang(hu) %{_appdir}/skins/Chameleon/texts/texts_hu.properties
%lang(is) %{_appdir}/skins/Chameleon/texts/texts_is.properties
%lang(it) %{_appdir}/skins/Chameleon/texts/texts_it.properties
%lang(nl) %{_appdir}/skins/Chameleon/texts/texts_nl.properties
%lang(no) %{_appdir}/skins/Chameleon/texts/texts_no.properties
%lang(pl) %{_appdir}/skins/Chameleon/texts/texts_pl.properties
%lang(pt) %{_appdir}/skins/Chameleon/texts/texts_pt.properties
%lang(ru) %{_appdir}/skins/Chameleon/texts/texts_ru.properties
%lang(sk) %{_appdir}/skins/Chameleon/texts/texts_sk.properties
%lang(sl) %{_appdir}/skins/Chameleon/texts/texts_sl.properties
%lang(sr) %{_appdir}/skins/Chameleon/texts/texts_sr.properties
%lang(sr@Latn) %{_appdir}/skins/Chameleon/texts/texts_sr_latin.properties
%lang(sv) %{_appdir}/skins/Chameleon/texts/texts_sv.properties
%lang(uk) %{_appdir}/skins/Chameleon/texts/texts_uk.properties
%lang(zh) %{_appdir}/skins/Chameleon/texts/texts_zh.properties
%lang(sv) %{_appdir}/skins/Nature/texts/texts_sv.properties
%lang(cs) %{_appdir}/skins/Standard/texts/texts_cs.properties
%lang(sv) %{_appdir}/skins/Standard/texts/texts_sv.properties
%lang(sk) %{_appdir}/skins/Wedding/texts/texts_sk.properties
%lang(sv) %{_appdir}/skins/Wedding/texts/texts_sv.properties
