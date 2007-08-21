%define php php4
%if %mdkversion < 200600
%define php php
%endif


Name:		mapserver
Version: 	4.10.2
Release:        %mkrel 1
Summary:	Web-based Map Server
Source:		http://download.osgeo.org/mapserver/mapserver-%{version}.tar.gz
URL:		http://mapserver.gis.umn.edu/
License:	MIT
Group:		Sciences/Geosciences
BuildRequires:	libproj-devel libgdal-devel php-devel curl-devel
BuildRequires:	freetype2-devel gd-devel >= 2.0.12 webserver apache-mpm-prefork
BuildRequires:	autoconf
Patch:		mapserver-4.10.2-multiarch.patch
Requires:	webserver
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

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

%package 	php
Group:          Sciences/Geosciences
Summary:	Mapserver php-mapscript
URL:		http://mapserver.gis.umn.edu/
Requires:	php libgdal curl

%description	php
php-mapscript allows you to have mapserver functions from within php,
creating maps with php commands.

%prep
%setup -q
%patch -p0 -b .multiarch
autoconf

%build
%configure --with-proj --with-gdal --with-ogr --with-wms \
	--with-php=/usr/include/%php --without-tiff --with-threads \
	--with-wfs --with-wcs --with-wmsclient --with-wfsclient \
	--with-httpd=/usr/sbin/httpd
perl -pi -e 's,/usr/local,\$(DESTDIR)/%{_prefix},g' Makefile

# not buildable in //
make

%install
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_includedir}/%{name}-4.6
mkdir -p %{buildroot}/%{_libdir}/%{php}/extensions
mkdir -p %{buildroot}/%{_sysconfdir}/%{php}.d/

cat > 40_mapscript.ini <<EOF
extension = php_mapscript.so
EOF

%makeinstall_std

install -d %{buildroot}/%{_var}/www/cgi-bin
install -d %{buildroot}/%{_var}/www/html/mapserver/tmp
install -m755 mapserv shp2img shp2pdf legend shptree shptreevis \
 shptreetst scalebar sortshp tile4ms %{buildroot}/%{_var}/www/cgi-bin
install -m755 mapscript/php3/php_mapscript.so %{buildroot}/%{_libdir}/%{php}/extensions
install -m755 40_mapscript.ini %{buildroot}/%{_sysconfdir}/%{php}.d/

%post php
%{_post_webapp}

%postun php
%{_postun_webapp}


%files
%defattr(-,root,root)
%exclude %{_includedir}/*
%{_var}/www/cgi-bin/*
%dir %{_var}/www/html/mapserver
%attr(755,apache,apache) %{_var}/www/html/mapserver/tmp
%doc INSTALL README HISTORY.TXT

%files php
%defattr(-,root,root)
%{_sysconfdir}/%{php}.d/40_mapscript.ini
%{_libdir}/%{php}/extensions/*

%clean
rm -Rf %{buildroot}


