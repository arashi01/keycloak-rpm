%define debug_package %{nil}
%define __jar_repack  %{nil}
%define jboss_home    /opt/jboss

Name:           keycloak
Version:        3.1.0
Release:        1%{?dist}
Summary:        Keycloak is an open source identity and access management solution.

Group:          System Environment/Base
License:        APLv2.0
URL:            http://www.keycloak.org/
Source0:        https://downloads.jboss.org/%{name}/%{version}.Final/%{name}-%{version}.Final.tar.gz
Source1:        keycloak.service
Source2:        keycloak.sysconfig
Source3:        LICENSE

BuildRequires: systemd tar gzip

Requires(pre): shadow-utils
Requires:      systemd java-headless

%description
Keycloak is an open source Identity and Access Management solution aimed at 
modern applications and services. It makes it easy to secure applications and 
services with little to no code.

%prep

%build

%install
install -d %{buildroot}%{jboss_home}/%{name}-%{version}
tar --strip-components=1 -C %{buildroot}%{jboss_home}/%{name}-%{version} -xvf %{SOURCE0}
ln -sf %{name}-%{version}.Final %{buildroot}%{jboss_home}/%{name}
install -D %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
install -D %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
install -D %{SOURCE3} %{buildroot}/%{_docdir}/%{name}/LICENSE

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "%{name} user" %{name}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
getent passwd %{name} >/dev/null && userdel %{name}
getent group %{name} >/dev/null && groupdel %{name}
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %attr(-, %{name}, %{name}) %{jboss_home}/%{name}-%{version}
%attr(-, %{name}, %{name}) %{jboss_home}/%{name}-%{version}/*
%attr(-, %{name}, %{name}) %{jboss_home}/%{name}
%attr(644, root, root) %{_unitdir}/%{name}.service
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/sysconfig/%{name}
%doc %{_docdir}/%{name}/LICENSE

%changelog
* Thu Jun 01 2017 Arun Babu Neelicattu <arun.neelicattu@gmail.com> - 3.1.0-1
- Initial packaing source.
