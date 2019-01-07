%if 0%{?fedora} > 12 || 0%{?rhel} >= 7
%bcond_without python3
%else
%bcond_with python3
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif
%if %{with python3}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif  # with python3

%define  pkgname inflection

Name:    python-%pkgname
Version: 0.3.1
Release: 2%{?dist}
Summary: A port of Ruby on Rails inflector to Python

Group:   Development/Tools
License: MIT
URL:     http://github.com/jpvanhal/inflection
Source:  https://pypi.python.org/packages/source/i/%pkgname/%pkgname-%version.tar.gz

BuildRequires: python2-devel
BuildRequires: python-setuptools
%if %{with python3}
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools
%endif  # with python3

BuildArch:     noarch

%description
Inflection is a string transformation library. It singularizes and pluralizes
English words, and transforms strings from CamelCase to underscored string.
Inflection is a port of Ruby on Rails' inflector to Python.


%if %{with python3}
%package -n python%{python3_pkgversion}-%pkgname
Summary: A port of Ruby on Rails inflector to Python

%description -n python%{python3_pkgversion}-%pkgname
Inflection is a string transformation library. It singularizes and pluralizes
English words, and transforms strings from CamelCase to underscored string.
Inflection is a port of Ruby on Rails' inflector to Python.
%endif  # with python3


%prep
%setup -q -n %pkgname-%version


%build
%py2_build
%if %{with python3}
%py3_build
%endif  # with python3


%install
[ "%buildroot" = "/" ] || rm -rf "%buildroot"

%py2_install
%if %{with python3}
%py3_install
%endif  # with python3


%files
%defattr(-,root,root,-)
%{python2_sitelib}/inflection.py*
%{python2_sitelib}/inflection-%{version}-*.egg-info

%doc README.rst CHANGES.rst

%if %{with python3}
%files -n python%{python3_pkgversion}-%pkgname
%defattr(-,root,root,-)
%{python3_sitelib}/inflection.py
%{python3_sitelib}/__pycache__/inflection.*.py*
%{python3_sitelib}/inflection-%{version}-*.egg-info

%doc README.rst CHANGES.rst
%endif  # with python3


%clean
[ "%buildroot" = "/" ] || rm -rf "%buildroot"


%changelog
* Tue Jan 08 2019 Mikhail Ushanov <gm.mephisto@gmail.com> - 0.3.1-2
- Build python3 package for epel7
- Use python build and install macros

* Tue Apr 12 2016 Mikhail Ushanov <gm.mephisto@gmail.com> - 0.3.1-1
- Initial build.
