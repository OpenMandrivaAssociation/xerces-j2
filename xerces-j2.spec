%define cvs_version	2_11_0

Name:		xerces-j2
Version:	2.11.0
Release: 	7
Epoch:		0
Summary:	Java XML parser
License:	Apache License
URL:		http://xml.apache.org/xerces2-j/
Group:		Development/Java
Source0:	http://www.eu.apache.org/dist/xerces/j/source/Xerces-J-src.%{version}.tar.gz
Source1:	http://www.apache.org/dist/xerces/j/source/Xerces-J-src.%{version}.tar.gz.md5
Source2:	http://www.apache.org/dist/xerces/j/source/Xerces-J-src.%{version}.tar.gz.asc
Source3:	%{name}-version.sh
Source4:	%{name}-constants.sh
Source5:	https://svn.apache.org/repos/asf/xerces/java/trunk/tools/src/XJavac.java
Patch0:		%{name}-libgcj.patch
Patch1:		xerces-2.11.0-system-xml-apis.patch
Provides:	jaxp_parser_impl
Requires:	xalan-j2
Requires:	xml-commons-apis
Requires:	xml-commons-resolver >= 0:1.4
Requires(post):	update-alternatives
Requires(preun): update-alternatives
#BuildRequires:	java-devel
# Please do not switch this over to an OpenJDK requirement.
# xerces-j2 is required to bootstrap OpenJDK, and there are
# no drawbacks from building it with gcj.
BuildRequires:	java-1.5.0-gcj-devel
BuildRequires:	ant >= 0:1.5
BuildRequires:	ecj >= 2:4.2.2-1
BuildRequires:	java-rpmbuild >= 0:1.5
BuildRequires:	jaxp_parser_impl
BuildRequires:	xalan-j2
BuildRequires:	xml-commons-resolver = 1:1.2
BuildRequires:	xml-commons-apis xml-commons-apis-javadoc
BuildRequires:  coreutils

# RHEL3 and FC2
Obsoletes:	xerces-j <= 0:2.2
BuildArch:	noarch

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

mkdir -p tools/org/apache/xerces/util
cp -a %{SOURCE5} tools/org/apache/xerces/util

%apply_patches

%build
pushd tools
%{javac} -classpath $(build-classpath ant) org/apache/xerces/util/XJavac.java
mkdir bin && %{jar} cf bin/xjavac.jar org/apache/xerces/util/XJavac.class
popd

export OPT_JAR_LIST=:
export JAVA_HOME=%_prefix/lib/jvm/java-1.5.0-gcj
ant \
	-Dtools.dir=%{_javadir} \
	-Djar.apis=xml-commons-apis.jar \
	-Djar.resolver=xml-commons-resolver.jar \
        -Djar.serializer=xalan-j2-serializer.jar \
	clean jars javadocs
export GCJ_PROPERTIES=

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/xercesImpl.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)
# Let's keep the "standard" name as well
ln -sf %name-%version.jar $RPM_BUILD_ROOT%_javadir/xercesImpl.jar

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

%pre
rm -f %{_javadir}/xerces.jar

%post
%{_sbindir}/update-alternatives --install %{_javadir}/jaxp_parser_impl.jar \
  jaxp_parser_impl %{_javadir}/%{name}.jar 40

%preun
{
  [ $1 = 0 ] || exit 0
  %{_sbindir}/update-alternatives --remove jaxp_parser_impl %{_javadir}/%{name}.jar
} >/dev/null 2>&1 || :

%files
%defattr(0644,root,root,0755)
%doc LICENSE LICENSE-SAX.html LICENSE.DOM-documentation.html
%doc LICENSE.DOM-software.html LICENSE.resolver.txt
%doc LICENSE.serializer.txt NOTICE NOTICE.resolver.txt
%doc NOTICE.serializer.txt README Readme.html
%{_javadir}/%{name}*.jar
%{_javadir}/xercesImpl.jar

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

%files scripts
%defattr(0755,root,root,0755)
%{_bindir}/*


%changelog
* Mon Jun 13 2011 Oden Eriksson <oeriksson@mandriva.com> 0:2.9.0-15mdv2011.0
+ Revision: 684471
- sync with MDVSA-2011:108

* Sat May 07 2011 Oden Eriksson <oeriksson@mandriva.com> 0:2.9.0-14
+ Revision: 671304
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.9.0-13mdv2011.0
+ Revision: 608203
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.9.0-12mdv2010.1
+ Revision: 524438
- rebuilt for 2010.1

* Sun Sep 27 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0:2.9.0-11mdv2010.0
+ Revision: 449800
- rebuild for new era

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:2.9.0-10mdv2009.1
+ Revision: 351200
- rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0:2.9.0-9mdv2009.0
+ Revision: 226032
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 David Walluck <walluck@mandriva.org> 0:2.9.0-8mdv2008.1
+ Revision: 125963
- can't own alternative symlink
- remove javadoc %%post/%%postun
- remove explicit settings for gcj
- fix OPT_JAR_LIST
- call update-alternatives with full path

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:2.9.0-7mdv2008.1
+ Revision: 121052
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Wed Sep 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0:2.9.0-6mdv2008.0
+ Revision: 90379
- rebuild

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:2.9.0-5mdv2008.0
+ Revision: 87272
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

  + Thierry Vignaud <tv@mandriva.org>
    - kill file require on update-alternatives

* Wed Jul 18 2007 Anssi Hannula <anssi@mandriva.org> 0:2.9.0-4mdv2008.0
+ Revision: 53216
- use xml-commons-jaxp-1.3-apis and xml-commons-resolver12 explicitely
  instead of the generic xml-commons-apis and xml-commons-resolver which
  are provided by multiple packages (see bug #31473)


* Sat Dec 16 2006 David Walluck <walluck@mandriva.org> 2.9.0-3mdv2007.0
+ Revision: 98115
- tighten BuildRequires
- set noarch if no gcj_support
- 2.9.0
- Import xerces-j2

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:2.8.0-1mdv2007.0
- 2.8.0

* Fri Jun 02 2006 David Walluck <walluck@mandriva.org> 0:2.7.1-6.7.3mdv2007.0
- rebuild for libgcj.so.7

* Sat Apr 22 2006 David Walluck <walluck@mandriva.org> 0:2.7.1-6.7.2mdk
- recreate

* Wed Apr 12 2006 David Walluck <walluck@mandriva.org> 0:2.7.1-6.7.1mdk
- 2.7.1

* Sat Dec 03 2005 David Walluck <walluck@mandriva.org> 0:2.6.2-5.2.1mdk
- sync with 5jpp_2fc

* Mon May 23 2005 David Walluck <walluck@mandriva.org> 0:2.6.2-4.2mdk
- remove pre-compiled xjavac task

* Sun May 22 2005 David Walluck <walluck@mandriva.org> 0:2.6.2-4.1mdk
- release

* Fri Apr 29 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_3fc
- Revert xjavac classpath workaround, and patch to use libgcj's
  classes instead of those in xml-commons (#152255).

* Fri Apr 22 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_2fc
- Add classpath workaround to xjavac task (#152255).

* Wed Jan 12 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_1fc
- Reenable building of classes that require javax.swing (#130006).
- Sync with RHAPS.

* Mon Nov 15 2004 Fernando Nasser <fnasser@redhat.com>  0:2.6.2-4jpp_1rh
- Merge with upstream for 2.6.2 upgrade

* Thu Nov 04 2004 Gary Benson <gbenson@redhat.com> 0:2.6.2-2jpp_5fc
- Build into Fedora.

* Fri Oct 29 2004 Gary Benson <gbenson@redhat.com> 0:2.6.2-2jpp_4fc
- Bootstrap into Fedora.

* Sat Oct 02 2004 Andrew Overholt <overholt@redhat.com> 0:2.6.2-2jpp_4rh
- add coreutils BuildRequires

* Fri Oct 01 2004 Andrew Overholt <overholt@redhat.com> 0:2.6.2-2jpp_3rh
- Remove xml-commons-resolver as a Requires

* Fri Aug 27 2004 Ralph Apel <r.apel at r-apel.de> 0:2.6.2-4jpp
- Build with ant-1.6.2
- Dropped jikes requirement, built for 1.4.2

* Thu Jun 24 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:2.6.2-3jpp
- Updated Patch #0 to fix breakage using BEA 1.4.2 SDK, new patch
  from <mwringe@redhat.com> and <vivekl@redhat.com>.

* Tue Jun 22 2004 Vivek Lakshmanan <vivekl@redhat.com> 0:2.6.2-2jpp_2rh
- Added new Source1 URL and added new %%setup to expand it under the
  expanded result of Source0.
- Updated Patch0 to fix version discrepancies.
- Added build requirement for xml-commons-apis

* Tue Jun 15 2004 Matt Wringe <mwringe@redhat.com> 0:2.6.2-2jpp_1rh
- Update to 2.6.2
- made patch names comformant

* Tue Mar 30 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:2.6.2-2jpp
- Rebuilt with jikes 1.18 for java 1.3.1_11

* Fri Mar 26 2004 Frank Ch. Eigler <fche@redhat.com> 0:2.6.1-1jpp_2rh
- add RHUG upgrade cleanup

* Tue Mar 23 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:2.6.2-1jpp
- 2.6.2

* Thu Mar 11 2004 Frank Ch. Eigler <fche@redhat.com> 0:2.6.1-1jpp_1rh
- RH vacuuming
- remove jikes dependency
- add nonjikes-cast.patch

* Sun Feb 08 2004 David Walluck <david@anti-microsoft.org> 0:2.6.1-1jpp
- 2.6.1
- update Source0 URL
- now requires xml-commons-resolver

* Fri Jan 09 2004 Kaj J. Niemi <kajtzu@fi.basen.net> - 0:2.6.0-1jpp
- Update to 2.6.0
- Patch #1 (xerces-j2-manifest.patch) is unnecessary (upstream)

