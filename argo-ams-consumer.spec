%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%define underscore() %(echo %1 | sed 's/-/_/g')
%define stripc() %(echo %1 | sed 's/el7.centos/el7/')

%if 0%{?el7:1}
%define mydist %{stripc %{dist}}
%else
%define mydist %{dist}
%endif

Name:          argo-ams-consumer
Summary:       Argo Messaging Service metric results consumer
Version:       1.0.0
Release:       1%{?mydist}
License:       ASL 2.0

BuildArch:     noarch
BuildRequires: python2-devel
Buildroot:     %{_tmppath}/%{name}-buildroot
Requires:      argo-ams-library
Requires:      avro
Requires:      python-daemon

%if 0%{?el7:1}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(post):   systemd-sysv
%else
Requires:         python-argparse
%endif

Source0:       %{name}-%{version}.tar.gz

%description
AMS consumer fetchs metric results from Argo Messaging Service and stores them
in avro serialized files

%build
env
python setup.py build

%prep
%setup -n %{name}-%{version}

%install 
%{__python} setup.py install --skip-build --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install --directory %{buildroot}/etc/%{name}/
install --directory %{buildroot}/%{_sharedstatedir}/%{name}/
install --directory --mode 755 $RPM_BUILD_ROOT/%{_localstatedir}/run/%{name}/
install --directory --mode 755 $RPM_BUILD_ROOT/%{_localstatedir}/log/%{name}/

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%attr(0755,root,root) /usr/bin/ams-consumerd
%attr(0755,root,root) %{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/ams-consumer.conf 
%dir %{python_sitelib}/%{underscore %{name}}
%{python_sitelib}/%{underscore %{name}}/*.py[co]
%dir %{_localstatedir}/log/%{name}/
%dir %{_localstatedir}/run/%{name}/

%if 0%{?el7:1}
%{_unitdir}/ams-consumer.service
%else
%attr(0755,root,root) /etc/init.d/ams-consumer
%endif

%post
%if 0%{?el7:1}
%systemd_post ams-consumer.service
%else
/sbin/chkconfig --add ams-consumer
%endif

%postun
%if 0%{?el7:1}
%systemd_postun_with_restart ams-consumer.service
%else
if [ "$1" -ge 2 ] ; then
	/sbin/service ams-consumer stop
	/sbin/service ams-consumer start 
fi
%endif

%preun
%if 0%{?el7:1}
%systemd_preun ams-consumer.service
%else
if [ "$1" = 0 ] ; then
	/sbin/service ams-consumer stop
	/sbin/chkconfig --del ams-consumer
fi
%endif

%changelog
* Thu May 10 2018 Daniel Vrcic <dvrcic@srce.hr>, Hrvoje Sute <hsute@srce.hr> - 1.0.0-1%{?dist}
- ARGO-1106 Pull interval as float
- ARGO-1092 AMS Consumer README
- ARGO-1069 AMS Consumer Centos7 support
- ARGO-1050 Connection timeout as config option 
- ARGO-869 RPM packaging metadata
- ARGO-1036 report period fix
- ARGO-1036 Message retention logic
- ARGO-790 avro serialization of fetched data
- ARGO-971 AMS messages fetching loop  
- ARGO-846 Introduce config parser with template config file 
- ARGO-845 Daemonize worker process and register signal handlers
* Tue Feb 20 2018 Daniel Vrcic <dvrcic@srce.hr> - 0.1.0-1%{?dist}
- RPM package
