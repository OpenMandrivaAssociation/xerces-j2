%define cvs_version	2_9_0
%define section		free
%define gcj_support	1

Name:		xerces-j2
Version:	2.9.0
Release: 	%mkrel 9
Epoch:		0
Summary:	Java XML parser
License:	Apache License
URL:		http://xml.apache.org/xerces2-j/
Group:		Development/Java
Source0:	http://www.apache.org/dist/xml/xerces-j/Xerces-J-src.%{version}.tar.gz
Source1:	http://www.apache.org/dist/xml/xerces-j/Xerces-J-src.%{version}.tar.gz.md5
Source2:	http://www.apache.org/dist/xml/xerces-j/Xerces-J-src.%{version}.tar.gz.sig
Source3:        %{name}-version.sh
Source4:        %{name}-constants.sh
Source5:	XJavac.java
Patch0:         %{name}-build.patch
Patch1:         %{name}-libgcj.patch
Provides:	jaxp_parser_impl
Requires:	xalan-j2
Requires:	xml-commons-jaxp-1.3-apis
Requires:	xml-commons-resolver12 >= 0:1.1
Requires(post):	update-alternatives
Requires(preun): update-alternatives
BuildRequires:	java-devel
BuildRequires:	ant >= 0:1.5
BuildRequires:	java-rpmbuild >= 0:1.5
BuildRequires:	jaxp_parser_impl
BuildRequires:	xalan-j2
BuildRequires:	xml-commons-resolver12 >= 0:1.3
BuildRequires:	xml-commons-jaxp-1.3-apis
BuildRequires:  coreutils
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
# RHEL3 and FC2
Obsoletes:	xerces-j <= 0:2.2
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel >= 0:1.0.31
%else
BuildArch:        noarch
%endif

%description
Welcome to the future! Xerces2 is the next generation of high
performance, fully compliant XML parsers in the Apache Xerces family.
This new version of Xerces introduces the Xerces Native Interface (XNI),
a complete framework for building parser components and configurations
that is extremely modular and easy to program.

The Apache Xerces2 parser is the reference implementation of XNI but
other parser components, configurations, and parsers can be written
using the Xerces Native Interface. For complete design and
implementation documents, refer to the XNI Manual.

Xerces 2 is a fully conforming XML Schema processor. For more
information, refer to the XML Schema page.

Xerces 2 also provides a partial implementation of Document Object Model
Level 3 Core, Load and Save and Abstract Schemas [deprecated] Working
Drafts. For more information, refer to the DOM Level 3 Implementation
page.

%package        javadoc-impl
Summary:	Javadoc for %{name} implementation
Group:		Development/Java

%description    javadoc-impl
Javadoc for %{name} implementation.

%package        javadoc-apis
Summary:	Javadoc for %{name} apis
Group:		Development/Java

%description    javadoc-apis
Javadoc for %{name} apis.

%package        javadoc-xni
Summary:	Javadoc for %{name} xni
Group:		Development/Java

%description    javadoc-xni
Javadoc for %{name} xni.

%package        javadoc-other
Summary:	Javadoc for other %{name} components
Group:		Development/Java

%description    javadoc-other
Javadoc for other %{name} components.

%package        demo
Summary:	Demo for %{name}
Group:		Development/Java
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description    demo
Demonstrations and samples for %{name}.

%package        scripts
Summary:        Additional utility scripts for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:	jpackage-utils >= 0:1.5

%description    scripts
Additional utility scripts for %{name}.

%prep
%setup -q -n xerces-%{cvs_version}
%patch0 -p1 -b .build

mkdir -p tools/org/apache/xerces/util
cp -a %{SOURCE5} tools/org/apache/xerces/util
%patch1 -p0 -b .libgcj


%build
pushd tools
%{javac} -classpath $(build-classpath ant) org/apache/xerces/util/XJavac.java
mkdir bin && %{jar} cf bin/xjavac.jar org/apache/xerces/util/XJavac.class
popd

export CLASSPATH=
export OPT_JAR_LIST=:
%{ant} \
	-Dbuild.compiler=modern \
	-Dtools.dir=%{_javadir} \
	-Djar.apis=xml-commons-jaxp-1.3-apis.jar \
	-Djar.resolver=xml-commons-resolver12.jar \
        -Djar.serializer=xalan-j2-serializer.jar \
	clean jars javadocs
export GCJ_PROPERTIES=

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/xercesImpl.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-impl-%{version}
#cp -pr build/docs/javadocs/xerces2/* \
#  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-impl-%{version}
ln -s %{name}-impl-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-impl

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-apis-%{version}
#cp -pr build/docs/javadocs/api/* \
#  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-apis-%{version}
ln -s %{name}-apis-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-apis

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-xni-%{version}
#cp -pr build/docs/javadocs/xni/* \
#  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-xni-%{version}
ln -s %{name}-xni-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-xni

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-other-%{version}
#cp -pr build/docs/javadocs/other/* \
#  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-other-%{version}
ln -s %{name}-other-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-other

rm -rf build/docs/javadocs

# scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/%{name}-version
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}/%{name}-constants

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p build/xercesSamples.jar \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-samples.jar
cp -pr data $RPM_BUILD_ROOT%{_datadir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%pre
rm -f %{_javadir}/xerces.jar

%post
%{_sbindir}/update-alternatives --install %{_javadir}/jaxp_parser_impl.jar \
  jaxp_parser_impl %{_javadir}/%{name}.jar 40
%if %{gcj_support}
%{update_gcjdb}
%endif

%preun
{
  [ $1 = 0 ] || exit 0
  %{_sbindir}/update-alternatives --remove jaxp_parser_impl %{_javadir}/%{name}.jar
} >/dev/null 2>&1 || :

%if %{gcj_support}
%postun
%{clean_gcjdb}

%post demo
%{update_gcjdb}

%postun demo
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE LICENSE-SAX.html LICENSE.DOM-documentation.html
%doc LICENSE.DOM-software.html LICENSE.resolver.txt
%doc LICENSE.serializer.txt NOTICE NOTICE.resolver.txt
%doc NOTICE.serializer.txt README Readme.html
%{_javadir}/%{name}*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%endif

%files javadoc-impl
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-impl-%{version}
%ghost %doc %{_javadocdir}/%{name}-impl

%files javadoc-apis
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-apis-%{version}
%ghost %doc %{_javadocdir}/%{name}-apis

%files javadoc-other
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-other-%{version}
%ghost %doc %{_javadocdir}/%{name}-other

%files javadoc-xni
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-xni-%{version}
%ghost %doc %{_javadocdir}/%{name}-xni

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-samples.jar.*
%endif

%files scripts
%defattr(0755,root,root,0755)
%{_bindir}/*
