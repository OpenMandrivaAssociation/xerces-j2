Name:		xerces-j2
Version:	2.12.2
Release:	1
Summary:	Apache Xerces-J XML parser
Group:		Development/Java
License:	Apache-2.0 AND W3C
URL:		https://xerces.apache.org/xerces2-j/
# Source distribution of Xerces-J 2.12.2. No prebuilt jars.
Source0:	https://archive.apache.org/dist/xerces/j/source/Xerces-J-src.%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	sysjar
BuildRequires:	mvn(xml-apis:xml-apis)
BuildRequires:	mvn(xml-resolver:xml-resolver)

%description
Apache Xerces-J 2.12.2. Gradle 9.9.1 accepts
mvn(xerces:xercesImpl) at this version. The JDK java.xml
module does not publish that coordinate.
Cooker's xml-apis jar has no HTMLDOMImplementation, so this
package compiles the interface that ships in the Xerces source
tree. XML Catalog resolution is optional, as in the upstream POM.

%prep
%autosetup -n xerces-2_12_2 -p1
find . \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -delete

%build
sed -i 's|@@VERSION@@|Xerces-J %{version}|' src/org/apache/xerces/impl/Version.java
grep -q 'Xerces-J %{version}' src/org/apache/xerces/impl/Version.java
find src/org/apache -name '*.java' > sources.list
echo src/org/w3c/dom/html/HTMLDOMImplementation.java >> sources.list
test "$(wc -l < sources.list)" -eq 711
mkdir -p classes
javac --release 8 -encoding UTF-8 -Xlint:-options \
	-cp "%{_javadir}/xml-apis.jar:%{_javadir}/xml-commons-resolver.jar" \
	-d classes @sources.list
find src/org/apache \( -name '*.properties' -o -name '*.res' \) -print0 |
	while IFS= read -r -d '' f; do
		dest="classes/${f#src/}"
		mkdir -p "$(dirname "$dest")"
		/bin/cp -f "$f" "$dest"
	done
for bundle in DatatypeMessages DOMMessages JAXPValidationMessages SAXMessages \
	XIncludeMessages XMLMessages XMLSchemaMessages XMLSerializerMessages \
	XPointerMessages; do
	/bin/cp -f "src/org/apache/xerces/impl/msg/${bundle}.properties" \
		"classes/org/apache/xerces/impl/msg/${bundle}_en.properties"
done
/bin/cp -f src/org/apache/xerces/impl/xpath/regex/message.properties \
	classes/org/apache/xerces/impl/xpath/regex/message_en.properties
mkdir -p classes/META-INF/services
/bin/cp -f src/org/apache/xerces/jaxp/datatype/javax.xml.datatype.DatatypeFactory \
	classes/META-INF/services/javax.xml.datatype.DatatypeFactory
/bin/cp -f src/org/apache/xerces/jaxp/validation/javax.xml.validation.SchemaFactory \
	classes/META-INF/services/javax.xml.validation.SchemaFactory
/bin/cp -f src/org/apache/xerces/stax/javax.xml.stream.XMLEventFactory \
	classes/META-INF/services/javax.xml.stream.XMLEventFactory
/bin/cp -f src/org/apache/xerces/parsers/org.xml.sax.driver \
	classes/META-INF/services/org.xml.sax.driver
/bin/cp -f src/org/apache/xerces/dom/org.w3c.dom.DOMImplementationSourceList \
	classes/META-INF/services/org.w3c.dom.DOMImplementationSourceList
jar cf xercesImpl.jar -C classes .
cat > xercesImpl.pom <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>xerces</groupId>
  <artifactId>xercesImpl</artifactId>
  <version>2.12.2</version>
  <name>Xerces2-j</name>
  <description>Apache Xerces-J XML parser.</description>
  <url>https://xerces.apache.org/xerces2-j/</url>
  <licenses>
    <license>
      <name>The Apache Software License, Version 2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>xml-apis</groupId>
      <artifactId>xml-apis</artifactId>
      <version>1.4.01</version>
    </dependency>
    <dependency>
      <groupId>xml-resolver</groupId>
      <artifactId>xml-resolver</artifactId>
      <version>1.2</version>
      <optional>true</optional>
    </dependency>
  </dependencies>
</project>
EOF

%install
sysjar install --buildroot %{buildroot} \
	--artifact xercesImpl.pom:xercesImpl.jar \
	--file-name xercesImpl \
	--filelist .mfiles

%check
JAR=%{buildroot}%{_javadir}/xercesImpl.jar
test -f "$JAR"
mkdir -p check
cat > check/Smoke.java <<'END'
import org.apache.xerces.impl.Version;
import org.apache.xerces.parsers.DOMParser;
import org.w3c.dom.Element;
import org.xml.sax.InputSource;
import java.io.StringReader;
public class Smoke {
	public static void main(String[] args) throws Exception {
		DOMParser parser = new DOMParser();
		parser.parse(new InputSource(new StringReader("<a>xerces_ok</a>")));
		Element el = parser.getDocument().getDocumentElement();
		System.out.println(Version.fVersion + " " + el.getTextContent().trim());
	}
}
END
javac --release 8 -encoding UTF-8 -Xlint:-options \
	-cp "$JAR:%{_javadir}/xml-apis.jar:%{_javadir}/xml-commons-resolver.jar" \
	-d check check/Smoke.java
java -cp "check:$JAR:%{_javadir}/xml-apis.jar:%{_javadir}/xml-commons-resolver.jar" Smoke > check/out.txt
cat check/out.txt
grep -F -q 'Xerces-J 2.12.2 xerces_ok' check/out.txt

%files -f .mfiles
%license LICENSE NOTICE LICENSE.DOM-software.html LICENSE-SAX.html LICENSE.resolver.txt LICENSE.serializer.txt
%doc README
