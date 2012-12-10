Name: mapserver
Version: 6.2.0
Release: 1
Summary: Web-based Map Server
Source0: http://download.osgeo.org/mapserver/%{name}-%{version}.tar.gz
URL: http://mapserver.org/
License: MIT
Group: Sciences/Geosciences
BuildRequires: proj-devel 
BuildRequires: libgdal-devel 
BuildRequires: php-devel 
BuildRequires: curl-devel
BuildRequires: freetype2-devel 
BuildRequires: gd-devel >= 2.0.12 
BuildRequires: webserver 
BuildRequires: apache-mpm-prefork
BuildRequires: autoconf
BuildRequires: netcdf-devel
BuildRequires: cfitsio-devel
BuildRequires: postgresql-devel
BuildRequires: geos-devel
BuildRequires: ming-devel
BuildRequires: shapelib-devel
BuildRequires: readline-devel
BuildRequires: pkgconfig(ftgl)
BuildRequires: pkgconfig(libsvg-cairo)
Requires: webserver

%description
MapServer is an  OpenSource development environment for building spatially 
enabled Internet applications. The software builds upon other popular 
OpenSource or freeware systems like Shapelib, FreeType, Proj.4, libTIFF, 
Perl and others.

The MapServer CGI application provides a significant number of 
"out-of-the-box" features. Here's a sampling:

* vector formats supported: ESRI shapefiles, simple embedded features, 
  ESRI ArcSDE (alpha release)
* raster formats supported (8-bit only): TIFF/GeoTIFF, GIF, PNG, ERDAS, 
  JPEG and EPPL7
* quadtree spatial indexing for shapefiles
* fully customizable, template driven output
* feature selection by item/value, point, area or another feature
* TrueType font support
* support for tiled raster and vector data (display only)
* automatic legend and scalebar building
* scale dependent feature drawing and application execution
* thematic map building using logical or regular expression based classes
* feature labeling including label collision mediation
* on-the-fly configuration via URLs
* on-the-fly projection

MapServer is not a full-featured GIS system, nor does it aspire to be. 
It does, however, provide enough core functionality to support a wide 
variety of web applications. Beyond browsing GIS data, MapServer allows 
you create "geographic image maps", that is, maps that can direct users 
to content.

%package -n php-mapscript
Group: Sciences/Geosciences
Summary: Mapserver php-mapscript
Obsoletes: mapserver-php < 4.10.3
Provides: mapscript = %{EVRD}
Provides: mapserver-php = %{EVRD}
Requires: php 
Requires: libgdal 
Requires: curl

%description -n php-mapscript
php-mapscript allows you to have mapserver functions from within php,
creating maps with php commands.

%package devel
Summary: Mapserver development files

%description devel
Development files for %{name}.

%prep
%setup -q

%build
%configure2_5x \
    --with-proj \
    --with-gdal \
    --with-ogr \
    --with-wms \
    --with-php=%{_bindir}/php-config \
    --without-tiff \
    --with-threads \
    --with-postgis \
    --with-wfs \
    --with-wcs \
    --with-wmsclient \
    --with-wfsclient \
    --with-png \
    --with-geos \
    --with-httpd=%{_sbindir}/httpd \
    --with-kml \
    --with-ftgl \
    --with-opengl \
    --with-mysql \
    --with-cairo \
    --with-libsvg-cairo \
    --with-zlib \
    --with-gd

%make

%install
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_includedir}/%{name}-4.6
mkdir -p %{buildroot}/%{_libdir}/php/extensions
mkdir -p %{buildroot}/%{_sysconfdir}/php.d/

cat > 40_mapscript.ini <<EOF
extension = php_mapscript.so
EOF

%makeinstall_std

#install -d %{buildroot}/%{_var}/www/cgi-bin
install -d %{buildroot}/%{_var}/www/html/mapserver/tmp

#for file in mapserv shp2img legend shptree shptreevis \
# shptreetst scalebar sortshp tile4ms msencrypt
#do
#mv %{buildroot}%{_bindir}/$file %{buildroot}/%{_var}/www/cgi-bin
#done

install -m755 40_mapscript.ini %{buildroot}/%{_sysconfdir}/php.d/

for binary in mapserv shp2img legend shptree shptreevis \
    shptreetst scalebar sortshp tile4ms msencrypt
do
    chrpath -d %{buildroot}%{_bindir}/$binary
done

%post -n php-mapscript
%{_post_webapp}

%postun -n php-mapscript
%{_postun_webapp}


%files
%exclude %{_includedir}/*
#%{_var}/www/cgi-bin/*
%dir %{_var}/www/html/mapserver
%attr(755,apache,apache) %{_var}/www/html/mapserver/tmp
%doc INSTALL README HISTORY.TXT
%{_libdir}/lib%{name}-%{version}.so
%{_bindir}/legend
%{_bindir}/mapserv
%{_bindir}/msencrypt
%{_bindir}/scalebar
%{_bindir}/shp2img
%{_bindir}/shptree
%{_bindir}/shptreetst
%{_bindir}/shptreevis
%{_bindir}/sortshp
%{_bindir}/tile4ms

%files -n php-mapscript
%{_sysconfdir}/php.d/40_mapscript.ini
%{_libdir}/php/extensions/*

%files devel
%{_libdir}/lib%{name}.so
%{_bindir}/mapserver-config



%changelog
* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 5.6.6-2mdv2012.0
+ Revision: 696387
- rebuilt for php-5.3.8

* Wed Apr 20 2011 Michael Scherer <misc@mandriva.org> 5.6.6-1
+ Revision: 656145
- update to new version 5.6.6

* Sat Aug 21 2010 Funda Wang <fwang@mandriva.org> 5.6.5-2mdv2011.0
+ Revision: 571655
- fix linkage

* Mon Aug 09 2010 Buchan Milne <bgmilne@mandriva.org> 5.6.5-1mdv2011.0
+ Revision: 567989
- update to new version 5.6.5
- Fix postgresql/postgis buildrequires

* Fri Apr 23 2010 Buchan Milne <bgmilne@mandriva.org> 5.6.3-1mdv2010.1
+ Revision: 538157
- buildrequire readline-devel
- update to new version 5.6.3

* Thu Oct 08 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 5.2.1-6mdv2010.0
+ Revision: 455894
- rebuild for new curl SSL backend

* Mon Oct 05 2009 Guillaume Rousse <guillomovitch@mandriva.org> 5.2.1-5mdv2010.0
+ Revision: 454294
- disable parallel build to fix build
- rebuild for new libdap

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Raphaël Gertz <rapsys@mandriva.org>
    - Rebuild

* Sat Jan 24 2009 Funda Wang <fwang@mandriva.org> 5.2.1-2mdv2009.1
+ Revision: 333299
- rebuild

  + Buchan Milne <bgmilne@mandriva.org>
    - New version 5.2.1
    - Fix "format not a string literal"

* Fri Aug 22 2008 Funda Wang <fwang@mandriva.org> 5.2.0-1mdv2009.0
+ Revision: 275025
- New version 5.2.0

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Buchan Milne <bgmilne@mandriva.org>
    - Enable ming and geos support
    - New version 5.0.3

* Mon Mar 03 2008 Buchan Milne <bgmilne@mandriva.org> 5.0.2-1mdv2008.1
+ Revision: 178226
- New version 5.0.2

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag
    - kill re-definition of %%buildroot on Pixel's request

* Fri Aug 24 2007 Helio Chissini de Castro <helio@mandriva.com> 4.10.3-1mdv2008.0
+ Revision: 71038
- New upstream version
- mapscript builds against php 5 since 4.8
- Added postgis support
- Changed mapscript package name to match other php packages

* Tue Aug 21 2007 Buchan Milne <bgmilne@mandriva.org> 4.10.2-1mdv2008.0
+ Revision: 68453
- Buildrequire cfitsio-devel
- Buildrequire netcdf-devel
- Buildrequire php4-devel on recent distros
- New version 4.10.2
- Fix PHP detection (use cpp instead of grep) with multiarched headers


* Sat Jan 27 2007 Emmanuel Andry <eandry@mandriva.org> 4.10.0-2mdv2007.0
+ Revision: 114441
- buildrequires apache-mpm-prefork

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - Rebuild against new curl

  + David Walluck <walluck@mandriva.org>
    - Import mapserver

* Tue Oct 31 2006 Franck Martin <franck@sopac.org> 4.10.0-1mdk
- New Release 4.10.0

* Tue Sep 05 2006 Franck Martin <franck@sopac.org> 4.8.4-1mdk
- New Release 4.8.4

* Tue Sep 13 2005 Franck Martin <franck@sopac.org> 4.6.1-1mdk
- New release 4.6.1

* Thu Jul 21 2005 Franck Martin <franck@sopac.org> 4.6.0-1mdk
- New release 4.6.0
- includes php mapscript

* Sun Jul 18 2004 Michael Scherer <misc@mandrake.org> 4.2.1-1mdk
- New release 4.2.1
- rpmbuildupdate aware

