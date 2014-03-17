%define libname %mklibname %{name} %{version}
%define devname %mklibname %{name} -d

Summary:	Web-based Map Server
Name:		mapserver
Version:	6.2.1
Release:	1
License:	MIT
Group:		Sciences/Geosciences
Url:		http://mapserver.org/
Source0:	http://download.osgeo.org/mapserver/%{name}-%{version}.tar.gz
Patch0:		mapserver-6.2.1-link.patch
Patch1:		mapserver-6.2.1-gdver.patch
BuildRequires:	apache-mpm-prefork
BuildRequires:	webserver
BuildRequires:	gd-devel
BuildRequires:	gdal-devel
BuildRequires:	geos-devel
BuildRequires:	php-devel
BuildRequires:	postgresql-devel
BuildRequires:	readline-devel
BuildRequires:	shapelib-devel
BuildRequires:	pkgconfig(cfitsio)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(ftgl)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libming)
BuildRequires:	pkgconfig(libsvg-cairo)
BuildRequires:	pkgconfig(netcdf)
BuildRequires:	pkgconfig(proj)
Requires:	webserver

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

%files
%dir %{_var}/www/html/mapserver
%attr(755,apache,apache) %{_var}/www/html/mapserver/tmp
%doc INSTALL README HISTORY.TXT
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

#----------------------------------------------------------------------------

%package -n php-mapscript
Summary:	Mapserver php-mapscript
Group:		Sciences/Geosciences
Provides:	mapscript = %{EVRD}
Provides:	mapserver-php = %{EVRD}
Requires:	php
Requires:	curl

%description -n php-mapscript
php-mapscript allows you to have mapserver functions from within php,
creating maps with php commands.

%files -n php-mapscript
%{_sysconfdir}/php.d/40_mapscript.ini
%{_libdir}/php/extensions/*

%post -n php-mapscript
%{_post_webapp}

%postun -n php-mapscript
%{_postun_webapp}

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Mapserver shared library
Group:		System/Libraries
Conflicts:	%{name} < 6.2.1

%description -n %{libname}
Mapserver shared library.

%files -n %{libname}
%{_libdir}/lib%{name}-%{version}.so

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Mapserver development files
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Conflicts:	%{name}-devel < 6.2.1
Obsoletes:	%{name}-devel < 6.2.1

%description -n %{devname}
Development files for %{name}.

%files -n %{devname}
%{_libdir}/lib%{name}.so
%{_bindir}/mapserver-config

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p0
%patch1 -p1

%build
%global ldflags %{ldflags} -lX11

autoreconf -fi
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

install -d %{buildroot}/%{_var}/www/html/mapserver/tmp

install -m755 40_mapscript.ini %{buildroot}/%{_sysconfdir}/php.d/

for binary in mapserv shp2img legend shptree shptreevis \
	shptreetst scalebar sortshp tile4ms msencrypt
do
	chrpath -d %{buildroot}%{_bindir}/$binary
done

