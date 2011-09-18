# TODO
# - system java deps from lib/ dir
Summary:	Jalbum web album software
Summary(pl.UTF-8):	Jalbum - oprogramowanie do albumów WWW
Name:		jalbum
Version:	8.2.8
Release:	4
License:	Freely Distributable
Group:		Applications/Publishing
Source0:	http://jalbum.net/download/%{version}/Linux/NoVM/Jalbuminstall.bin
# Source0-md5:	96e40cb736edb652de00dfadc349b201
Source1:	%{name}.desktop
Source2:	%{name}.png
Source3:	x-%{name}.desktop
Source4:	%{name}.sh
URL:		http://jalbum.net/
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
Requires:	jre
Requires:	desktop-file-utils
%if "%{pld_release}" != "ac"
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
%endif
# ifarch and x86 tray library
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifnarch %{ix86}
# only on x86 something to strip
%define		_enable_debug_packages	0
%endif

%define		_appdir		%{_libdir}/%{name}

%description
JAlbum makes Web albums of your digital images. No extra software is
needed to view your galleries other than a Web browser. Unlike "server
side" album scripts, a JAlbum gallery can be served from a plain Web
server without scripting support. JAlbum's built in Web server allows
you to share your albums straight from JAlbum. You can also share your
albums on a CD.

%description -l pl.UTF-8
JAlbum tworzy albumy WWW ze zdjęć cyfrowych. Do oglądania zdjęć nie
jest potrzebny żaden dodatkowy program poza przeglądarką WWW. W
przeciwieństwie do skryptów działających po stronie serwera galerie
utworzone przez JAlbum mogą być udostępniane przez zwykły serwer WWW
bez obsługi skryptów. Wbudowany w JAlbum serwer WWW umożliwia
udostępnianie zdjęć bezpośrednio z programu. Można także udostępniać
albumy na płytach CD.

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

%{__unzip} -qq Resource1.zip
mv C_/Dev/Java/JAlbum/* .
rm -f dist/JAlbum/lib/windows_zg_ia_sf.jar
rm -f dist/JAlbum/lib/sunos_zg_ia_sf.jar

for jar in $(find -name '*_zg_ia_sf.jar'); do
	dir=${jar%*_zg_ia_sf.jar}
	%{__unzip} -qq -a $jar -d $dir
	rm -f $jar
done
mv dist/Jalbum/skins dist/JAlbum

%ifarch %{ix86}
chmod +x dist/JAlbum/lib/linux/x86/libtray.so
%else
rm -rf dist/JAlbum/lib/linux/x86
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_appdir}}
cp -a dist/{Jalbum,JAlbum}/* $RPM_BUILD_ROOT%{_appdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__sed} -i -e 's,@APPDIR@,%{_appdir},g' $RPM_BUILD_ROOT%{_bindir}/%{name}

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_datadir}/mimelnk/application}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/mimelnk/application

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%{_pixmapsdir}/%{name}.png
%{_desktopdir}/%{name}.desktop
%{_datadir}/mimelnk/application/x-%{name}.desktop
%dir %{_appdir}
%{_appdir}/JAlbum.jar
%{_appdir}/ext
%{_appdir}/includes
%{_appdir}/license
%{_appdir}/plugins
%{_appdir}/res
%{_appdir}/system
%{_appdir}/tools

%dir %{_appdir}/lib
%{_appdir}/lib/*.jar
%dir %{_appdir}/lib/linux
%{_appdir}/lib/linux/jdic_stub.jar
%ifarch %{ix86}
%dir %{_appdir}/lib/linux/x86
%attr(755,root,root) %{_appdir}/lib/linux/x86/libtray.so
%endif

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
%lang(nb) %{_appdir}/texts/texts_no.properties
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
%{_appdir}/skins/*/examples
%{_appdir}/skins/*/guestbook
%{_appdir}/skins/*/help
%{_appdir}/skins/*/includes
%{_appdir}/skins/*/plugins
%{_appdir}/skins/*/res
%{_appdir}/skins/*/scripts
%{_appdir}/skins/*/styles
%{_appdir}/skins/*/skin.properties
%dir %{_appdir}/skins/*/texts
%{_appdir}/skins/*/texts/texts_en.properties
%{_appdir}/skins/*/texts/texts.properties
%{_appdir}/skins/TiltViewer/NOTES.media_server
%{_appdir}/skins/TiltViewer/texts/texts.base.properties
%lang(bs) %{_appdir}/skins/*/texts/texts_bs.properties
%lang(cs) %{_appdir}/skins/*/texts/texts_cs.properties
%lang(da) %{_appdir}/skins/*/texts/texts_da.properties
%lang(de) %{_appdir}/skins/*/texts/texts_de.properties
%lang(es) %{_appdir}/skins/*/texts/texts_es.properties
%lang(fi) %{_appdir}/skins/*/texts/texts_fi.properties
%lang(fr) %{_appdir}/skins/*/texts/texts_fr.properties
%lang(he) %{_appdir}/skins/*/texts/texts_he.properties
%lang(hu) %{_appdir}/skins/*/texts/texts_hu.properties
%lang(is) %{_appdir}/skins/*/texts/texts_is.properties
%lang(it) %{_appdir}/skins/*/texts/texts_it.properties
%lang(ko) %{_appdir}/skins/*/texts/texts_ko.properties
%lang(lt) %{_appdir}/skins/*/texts/texts_lt.properties
%lang(nb) %{_appdir}/skins/*/texts/texts_no.properties
%lang(nl) %{_appdir}/skins/*/texts/texts_nl.properties
%lang(pl) %{_appdir}/skins/*/texts/texts_pl.properties
%lang(pt) %{_appdir}/skins/*/texts/texts_pt.properties
%lang(ru) %{_appdir}/skins/*/texts/texts_ru.properties
%lang(sk) %{_appdir}/skins/*/texts/texts_sk.properties
%lang(sl) %{_appdir}/skins/*/texts/texts_sl.properties
%lang(sr) %{_appdir}/skins/*/texts/texts_sr.properties
%if "%{pld_release}" != "ac"
%lang(sr@latin) %{_appdir}/skins/*/texts/texts_sr_latin.properties
%else
%lang(sr@Latn) %{_appdir}/skins/*/texts/texts_sr_latin.properties
%endif
%lang(sv) %{_appdir}/skins/*/texts/texts_sv.properties
%lang(uk) %{_appdir}/skins/*/texts/texts_uk.properties
%lang(zh) %{_appdir}/skins/*/texts/texts_zh.properties
