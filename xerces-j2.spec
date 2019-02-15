%{?_javapackages_macros:%_javapackages_macros}
%global cvs_version 2_12_0

%define __requires_exclude system.bundle

Name:          xerces-j2
Version:       2.12.0
Release:       1
Summary:       Java XML parser
Group:         Development/Java
License:       ASL 2.0
URL:           http://xerces.apache.org/xerces2-j/

Source0:       http://mirror.ox.ac.uk/sites/rsync.apache.org/xerces/j/source/Xerces-J-src.%{version}.tar.gz
Source1:       %{name}-version.sh
Source2:       %{name}-constants.sh
Source11:      %{name}-version.1
Source12:      %{name}-constants.1

# Custom javac ant task used by the build
Source3:       https://svn.apache.org/repos/asf/xerces/java/tags/Xerces-J_%{cvs_version}/tools/src/XJavac.java

# Custom doclet tags used in javadocs
Source5:       https://svn.apache.org/repos/asf/xerces/java/tags/Xerces-J_%{cvs_version}/tools/src/ExperimentalTaglet.java
Source6:       https://svn.apache.org/repos/asf/xerces/java/tags/Xerces-J_%{cvs_version}/tools/src/InternalTaglet.java

Source7:       %{name}-pom.xml

# Patch the build so that it doesn't try to use bundled xml-commons source
Patch0:        %{name}-build.patch

# Patch the manifest so that it includes OSGi stuff
Patch1:        %{name}-manifest.patch

Patch2:		xerces-2.12.0-find-xjavac.jar.patch
Patch3:		xerces-2.12.0-getContentDocument-buildfix.patch
Patch4:		xerces-2.12.0-dont-copy-system-libraries.patch

BuildArch:     noarch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: jpackage-utils
BuildRequires: xalan-j2 >= 2.7.1
BuildRequires: xml-commons-resolver >= 1.2
BuildRequires: ant
BuildRequires: jaxp_parser_impl
%if 0%{?fedora}
BuildRequires: dejavu-sans-fonts
%else
BuildRequires: fonts-ttf-dejavu
%endif
BuildRequires: xerces-j2
Requires:      java-headless
Requires:      jpackage-utils
Requires:      xalan-j2 >= 2.7.1
Requires:      xml-commons-resolver >= 1.2

Provides:      jaxp_parser_impl = 1.4
Provides:      %{name}-scripts = %{version}-%{release}
Obsoletes:     %{name}-scripts < 2.11.0-6

Requires(post):  chkconfig jaxp_parser_impl
Requires(preun): chkconfig jaxp_parser_impl

# This documentation is provided by xml-commons-apis
Obsoletes:     %{name}-javadoc-apis < %{version}-%{release}

# http://mail-archives.apache.org/mod_mbox/xerces-j-dev/201008.mbox/%3COF8D7E2F83.0271A181-ON8525777F.00528302-8525777F.0054BBE0@ca.ibm.com%3E
Obsoletes:     %{name}-manual < %{version}-%{release}

%description
Welcome to the future! Xerces2 is the next generation of high performance,
fully compliant XML parsers in the Apache Xerces family. This new version of
Xerces introduces the Xerces Native Interface (XNI), a complete framework for
building parser components and configurations that is extremely modular and
easy to program.

The Apache Xerces2 parser is the reference implementation of XNI but other
parser components, configurations, and parsers can be written using the Xerces
Native Interface. For complete design and implementation documents, refer to
the XNI Manual.

Xerces2 is a fully conforming XML Schema processor. For more information,
refer to the XML Schema page.

Xerces2 also provides a complete implementation of the Document Object Model
Level 3 Core and Load/Save W3C Recommendations and provides a complete
implementation of the XML Inclusions (XInclude) W3C Recommendation. It also
provides support for OASIS XML Catalogs v1.1.

Xerces2 is able to parse documents written according to the XML 1.1
Recommendation, except that it does not yet provide an option to enable
normalization checking as described in section 2.13 of this specification. It
also handles name spaces according to the XML Namespaces 1.1 Recommendation,
and will correctly serialize XML 1.1 documents if the DOM level 3 load/save
APIs are in use.

%package        javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

# Consolidating all javadocs into one package
Obsoletes:      %{name}-javadoc-impl < %{version}-%{release}
Obsoletes:      %{name}-javadoc-xs < %{version}-%{release}
Obsoletes:      %{name}-javadoc-xni < %{version}-%{release}
Obsoletes:      %{name}-javadoc-other < %{version}-%{release}

%description    javadoc
This package contains the API documentation for %{name}.

%package        demo
Summary:        Demonstrations and samples for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}

%description    demo
%{summary}.

%prep
%autosetup -p1 -n xerces-%{cvs_version}

# Copy the custom ant tasks into place
mkdir -p tools/org/apache/xerces/util
mkdir -p tools/bin
cp -a %{SOURCE3} %{SOURCE5} %{SOURCE6} tools/org/apache/xerces/util

# Make sure upstream hasn't sneaked in any jars we don't know about
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

sed -i 's/\r//' LICENSE README NOTICE

%build
cd tools
# Build custom ant tasks
javac -classpath %{_datadir}/ant/lib/ant.jar:%{_datadir}/ant/lib/ant-launcher.jar org/apache/xerces/util/XJavac.java
jar cf bin/xjavac.jar org/apache/xerces/util/XJavac.class
cd ..

ant \
	-Dtools.dir=%{_datadir}/java \
	-Djar.resolver=xml-resolver.jar \
	clean jars javadocs

%install
# jars
install -pD -T build/xercesImpl.jar %{buildroot}%{_javadir}/%{name}.jar

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
mkdir -p %{buildroot}%{_javadocdir}/%{name}/impl
mkdir -p %{buildroot}%{_javadocdir}/%{name}/xs
mkdir -p %{buildroot}%{_javadocdir}/%{name}/xni
mkdir -p %{buildroot}%{_javadocdir}/%{name}/other

cp -pr build/docs/javadocs/xerces2/* %{buildroot}%{_javadocdir}/%{name}/impl
cp -pr build/docs/javadocs/xni/* %{buildroot}%{_javadocdir}/%{name}/xni
cp -pr build/docs/javadocs/other/* %{buildroot}%{_javadocdir}/%{name}/other

# scripts
install -pD -m755 -T %{SOURCE1} %{buildroot}%{_bindir}/%{name}-version
install -pD -m755 -T %{SOURCE2} %{buildroot}%{_bindir}/%{name}-constants

# manual pages
install -d -m 755 %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE11} %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE12} %{buildroot}%{_mandir}/man1

# demo
install -pD -T build/xercesSamples.jar %{buildroot}%{_datadir}/%{name}/%{name}-samples.jar
cp -pr data %{buildroot}%{_datadir}/%{name}

# Pom
install -pD -T -m 644 %{SOURCE7} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

%files
%doc LICENSE NOTICE README
%{_javadir}/%{name}*
%{_bindir}/*
%{_mandir}/*/*

%files javadoc
%{_javadocdir}/%{name}

%files demo
%{_datadir}/%{name}
