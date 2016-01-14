%global pkg_name xmlgraphics-commons
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.5
Release:        3.11%{?dist}
Epoch:          0
Summary:        XML Graphics Commons

License:        ASL 2.0
URL:            http://xmlgraphics.apache.org/
Source0:        http://apache.skknet.net/xmlgraphics/commons/source/%{pkg_name}-%{version}-src.tar.gz

BuildArch:      noarch
BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
BuildRequires:  %{?scl_prefix_java_common}ant >= 0:1.6
BuildRequires:  %{?scl_prefix_java_common}ant-junit >= 0:1.6
BuildRequires:  %{?scl_prefix_java_common}junit
BuildRequires:  %{?scl_prefix_java_common}apache-commons-io >= 1.3.1
BuildRequires:  %{?scl_prefix_java_common}apache-commons-logging >= 1.0.4
Requires:       %{?scl_prefix_java_common}apache-commons-io >= 1.3.1
Requires:       %{?scl_prefix_java_common}apache-commons-logging >= 1.0.4

%description
Apache XML Graphics Commons is a library that consists of
several reusable components used by Apache Batik and
Apache FOP. Many of these components can easily be used
separately outside the domains of SVG and XSL-FO. You will
find components such as a PDF library, an RTF library,
Graphics2D implementations that let you generate PDF &
PostScript files, and much more.

%package        javadoc
Summary:        Javadoc for %{pkg_name}

%description    javadoc
%{summary}.


%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
rm -f `find . -name "*.jar"`

# create pom from template
sed "s:@version@:%{version}:g" %{pkg_name}-pom-template.pom \
    > %{pkg_name}.pom
%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
export CLASSPATH=$(build-classpath commons-logging)
export OPT_JAR_LIST="ant/ant-junit junit"
pushd lib
ln -sf $(build-classpath commons-io) .
popd
ant package javadocs
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -Dpm 0644 build/%{pkg_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}.jar
install -pm 644 %{pkg_name}.pom $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{pkg_name}.pom
%add_maven_depmap JPP-%{pkg_name}.pom %{pkg_name}.jar

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE NOTICE README

%files javadoc
%doc LICENSE NOTICE
%doc %{_javadocdir}/%{name}


%changelog
* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0:1.5-3.11
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michal Srb <msrb@redhat.com> - 1.5-3.10
- Fix BR/R

* Wed Jan 07 2015 Michal Srb <msrb@redhat.com> - 1.5-3.9
- Migrate to .mfiles

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 0:1.5-3.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-3.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-3.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-3.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-3.4
- Remove requires on java

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 0:1.5-3.3
- SCL-ize BR/R

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-3.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-3.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 01.5-3
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-2
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Tue Mar 19 2013 Mat Booth <fedora@matbooth.co.uk> - 0:1.5-1
- Update to 1.5, rhbz #895934
- Drop unneeded patch

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 06 2012 Deepak Bhole <dbhole@redhat.com> 1.4-5
- Added dist to the release tag

* Thu Mar 01 2012 Jiri Vanek <jvanek@redhat.com> - 0:1.4-5
- Resolves: rhbz#796341
- Added xmlgraphics-commons-java-7-fix.patch to fix build with Java 7

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue May  3 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.4-3
- Install maven metadata
- Versionless jars & javadocs
- Fixes according to new guidelines

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 1 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4-1
- Updte to 1.4.

* Sat Jan 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.3.1-1
- Update to 1.3.1.
- Fix Source0 url.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Apr 02 2008 Lillian Angel <langel at redhat.com> - 0:1.3-1
- Added java-1.6.0-openjdk-devel as build requirement.

* Mon Mar 31 2008 Lillian Angel <langel at redhat.com> - 0:1.3-1
- Updated sources to 1.3.

* Fri Nov 23 2007 Lillian Angel <langel at redhat.com> - 0:1.2-1
- Added epoch.

* Fri Nov 23 2007 Lillian Angel <langel at redhat.com> - 0:1.2-1
- Added missing BuildRoot line.

* Fri Nov 23 2007 Lillian Angel <langel at redhat.com> - 0:1.2-1
- Fixed install section.

* Fri Nov 23 2007 Lillian Angel <langel at redhat.com> - 0:1.2-1
- Fixed rpmlint errors.

* Tue Sep 18 2007 Joshua Sumali <jsumali at redhat.com> - 0:1.2-1jpp
- Update to 1.2

* Tue May 23 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.0-1jpp
- First JPP-1.7 release
