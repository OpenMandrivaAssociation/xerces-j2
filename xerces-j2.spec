%global cvs_version 2_11_0

Name:          xerces-j2
Version:       2.11.0
Release:       6
Summary:       Java XML parser
Group:         Development/Java
License:       ASL 2.0
URL:           http://xerces.apache.org/xerces2-j/

Source0:       http://mirror.ox.ac.uk/sites/rsync.apache.org/xerces/j/source/Xerces-J-src.%{version}.tar.gz
Source1:       %{name}-version.sh
Source2:       %{name}-constants.sh

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

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch

BuildRequires: java-devel >= 0:1.6.0
BuildRequires: jpackage-utils
BuildRequires: xalan-j2 >= 2.7.1
BuildRequires: xml-commons-apis >= 1.4.01
BuildRequires: xml-commons-resolver >= 1.2
BuildRequires: ant
BuildRequires: xml-stylebook
BuildRequires: jaxp_parser_impl
BuildRequires: fonts-ttf-dejavu
Requires:      java
Requires:      jpackage-utils
Requires:      xalan-j2 >= 2.7.1
Requires:      xml-commons-apis >= 1.4.01
Requires:      xml-commons-resolver >= 1.2

Provides:      jaxp_parser_impl = 1.4

Requires(post):  chkconfig jaxp_parser_impl
Requires(preun): chkconfig jaxp_parser_impl
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

# This documentation is provided by xml-commons-apis
Obsoletes:     %{name}-javadoc-apis < %{version}-%{release}

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

%package        javadoc-impl
Summary:        Javadoc for %{name} implementation
Group:          Development/Java

%description    javadoc-impl
%{summary}.

%package        javadoc-xs
Summary:        Javadoc for %{name} XML schema API
Group:          Development/Java

%description    javadoc-xs
%{summary}.

%package        javadoc-xni
Summary:        Javadoc for %{name} XNI
Group:          Development/Java

%description    javadoc-xni
%{summary}.

%package        javadoc-other
Summary:        Javadoc for other %{name} components
Group:          Development/Java

%description    javadoc-other
%{summary}.

%package        manual
Summary:        Manual for %{name}
Group:          Development/Java
Requires:       xml-commons-apis-javadoc
Requires:       %{name}-javadoc-impl = %{version}-%{release}
Requires:       %{name}-javadoc-xs = %{version}-%{release}
Requires:       %{name}-javadoc-xni = %{version}-%{release}
Requires:       %{name}-javadoc-other = %{version}-%{release}

%description    manual
%{summary}.

%package        demo
Summary:        Demonstrations and samples for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}

%description    demo
%{summary}.

%package        scripts
Summary:        Additional utility scripts for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}

%description    scripts
%{summary}.

%prep
%setup -q -n xerces-%{cvs_version}
%patch0 -p0 -b .orig
%patch1 -p0 -b .orig

# Copy the custom ant tasks into place
mkdir -p tools/org/apache/xerces/util
mkdir -p tools/bin
cp -a %{SOURCE3} %{SOURCE5} %{SOURCE6} tools/org/apache/xerces/util

# Make sure upstream hasn't sneaked in any jars we don't know about
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

sed -i 's/\r//' LICENSE README NOTICE

%build
pushd tools

# Build custom ant tasks
javac -classpath $(build-classpath ant) org/apache/xerces/util/XJavac.java
jar cf bin/xjavac.jar org/apache/xerces/util/XJavac.class

# Build custom doc taglets
javac -classpath /usr/lib/jvm/java/lib/tools.jar org/apache/xerces/util/*Taglet.java
jar cf bin/xerces2taglets.jar org/apache/xerces/util/*Taglet.class

ln -sf $(build-classpath xalan-j2-serializer) serializer.jar
ln -sf $(build-classpath xalan-j2)
ln -sf $(build-classpath xml-commons-apis) xml-apis.jar
ln -sf $(build-classpath xml-commons-resolver) resolver.jar
ln -sf $(build-classpath xml-stylebook) stylebook-1.0-b2.jar
popd

export CLASSPATH=$CLASSPATH:$(build-classpath xalan-j2-serializer)
# Build everything
export ANT_OPTS="-Xmx256m -Djava.endorsed.dirs=$(pwd)/tools -Djava.awt.headless=true -Dbuild.sysclasspath=first -Ddisconnected=true"
ant -Djavac.source=1.5 -Djavac.target=1.5 \
    -Dbuild.compiler=modern \
    clean jars javadocs docs

# Fix line endings in generated docs
sed -i 's/\r//' build/docs/download.cgi build/docs/resources/script.js

%install
rm -rf %{buildroot}

# jars
install -pD -T build/xercesImpl.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-impl-%{version}
cp -pr build/docs/javadocs/xerces2/* %{buildroot}%{_javadocdir}/%{name}-impl-%{version}
(cd %{buildroot}%{_javadocdir} && ln -sf %{name}-impl-%{version} %{name}-impl)

mkdir -p %{buildroot}%{_javadocdir}/%{name}-xs-%{version}
cp -pr build/docs/javadocs/api/* %{buildroot}%{_javadocdir}/%{name}-xs-%{version}
(cd %{buildroot}%{_javadocdir} && ln -sf %{name}-xs-%{version} %{name}-xs)

mkdir -p %{buildroot}%{_javadocdir}/%{name}-xni-%{version}
cp -pr build/docs/javadocs/xni/* %{buildroot}%{_javadocdir}/%{name}-xni-%{version}
(cd %{buildroot}%{_javadocdir} && ln -sf %{name}-xni-%{version} %{name}-xni)

mkdir -p %{buildroot}%{_javadocdir}/%{name}-other-%{version}
cp -pr build/docs/javadocs/other/* %{buildroot}%{_javadocdir}/%{name}-other-%{version}
(cd %{buildroot}%{_javadocdir} && ln -sf %{name}-other-%{version} %{name}-other)

rm -rf build/docs/javadocs/*

# manual
install -d %{buildroot}%{_docdir}/%{name}-%{version}/manual
cp -pr build/docs/* %{buildroot}%{_docdir}/%{name}-%{version}/manual
ln -s ../../../../javadoc/xml-commons-apis/ %{buildroot}%{_docdir}/%{name}-%{version}/manual/javadocs/api
ln -s ../../../../javadoc/%{name}-impl/ %{buildroot}%{_docdir}/%{name}-%{version}/manual/javadocs/xerces2
ln -s ../../../../javadoc/%{name}-xs/ %{buildroot}%{_docdir}/%{name}-%{version}/manual/javadocs/xs
ln -s ../../../../javadoc/%{name}-xni/ %{buildroot}%{_docdir}/%{name}-%{version}/manual/javadocs/xni
ln -s ../../../../javadoc/%{name}-other/ %{buildroot}%{_docdir}/%{name}-%{version}/manual/javadocs/other

# other docs
install -p -m644 LICENSE README NOTICE %{buildroot}%{_docdir}/%{name}-%{version}

# scripts
install -pD -m755 -T %{SOURCE1} %{buildroot}%{_bindir}/%{name}-version
install -pD -m755 -T %{SOURCE2} %{buildroot}%{_bindir}/%{name}-constants

# demo
install -pD -T build/xercesSamples.jar %{buildroot}%{_datadir}/%{name}/%{name}-samples.jar
cp -pr data %{buildroot}%{_datadir}/%{name}

# Pom
install -pD -T -m 644 %{SOURCE7} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap xerces xercesImpl %{version} JPP %{name}

# Legacy depmaps for compatability
%add_to_maven_depmap xerces xerces %{version} JPP %{name}
%add_to_maven_depmap xerces xmlParserAPIs %{version} JPP %{name}

# jaxp_parser_impl ghost symlink
ln -s %{_sysconfdir}/alternatives \
  %{buildroot}%{_javadir}/jaxp_parser_impl.jar

%clean
rm -rf %{buildroot}

%post
%update_maven_depmap
update-alternatives --install %{_javadir}/jaxp_parser_impl.jar \
  jaxp_parser_impl %{_javadir}/%{name}.jar 40

%postun
%update_maven_depmap

%preun
{
  [ $1 = 0 ] || exit 0
  update-alternatives --remove jaxp_parser_impl %{_javadir}/%{name}.jar
} >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/LICENSE
%doc %{_docdir}/%{name}-%{version}/NOTICE
%doc %{_docdir}/%{name}-%{version}/README
%{_mavendepmapfragdir}/*
%{_mavenpomdir}/*
%{_javadir}/%{name}*
%ghost %{_javadir}/jaxp_parser_impl.jar

%files javadoc-impl
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-impl-%{version}
%{_javadocdir}/%{name}-impl

%files javadoc-xs
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-xs-%{version}
%{_javadocdir}/%{name}-xs

%files javadoc-other
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-other-%{version}
%{_javadocdir}/%{name}-other

%files javadoc-xni
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-xni-%{version}
%{_javadocdir}/%{name}-xni

%files manual
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/manual

%files demo
%defattr(-,root,root,-)
%{_datadir}/%{name}

%files scripts
%defattr(-,root,root,-)
%{_bindir}/*

