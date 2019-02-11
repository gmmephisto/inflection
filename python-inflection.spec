%if 0%{?fedora} > 12 || 0%{?epel} >= 6
%bcond_without python3
%else
%bcond_with python3
%endif

%if 0%{?epel} >= 7
%bcond_without python3_other
%endif

%if 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif
%if 0%{with python3}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python3_pkgversion: %global python3_pkgversion 3}
%endif  # with python3

%global  project_name inflection
%global  project_description %{expand:
Inflection is a string transformation library. It singularizes and pluralizes
English words, and transforms strings from CamelCase to underscored string.
Inflection is a port of Ruby on Rails' inflector to Python.}

%bcond_without tests

Name:    python-%project_name
Version: 0.3.1
Release: 2%{?dist}
Summary: A port of Ruby on Rails inflector to Python

Group:   Development/Tools
License: MIT
URL:     http://github.com/jpvanhal/inflection
Source:  https://pypi.python.org/packages/source/i/%project_name/%project_name-%version.tar.gz

BuildRequires: python2-devel
BuildRequires: python-setuptools
%if 0%{with tests}
BuildRequires: pytest
%endif  # with tests

BuildArch:     noarch

%description %{project_description}


%if 0%{with python3}
%package -n python%{python3_pkgversion}-%project_name
Summary: %{summary}
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools
%if 0%{with tests}
BuildRequires: python%{python3_pkgversion}-pytest
%endif  # with tests

%description -n python%{python3_pkgversion}-%project_name %{project_description}
%endif  # with python3


%if 0%{with python3_other}
%package -n python%{python3_other_pkgversion}-%project_name
Summary: %{summary}
BuildRequires: python%{python3_other_pkgversion}-devel
BuildRequires: python%{python3_other_pkgversion}-setuptools
%if 0%{with tests}
BuildRequires: python%{python3_other_pkgversion}-pytest
%endif  # with tests

%description -n python%{python3_other_pkgversion}-%project_name %{project_description}
%endif  # with python3_other


%prep
%setup -q -n %project_name-%version


%build
%py2_build
%if 0%{with python3}
%py3_build
%endif  # with python3
%if 0%{with python3_other}
%py3_other_build
%endif  # with python3_other


%check
%if 0%{with tests}
py.test-%{python2_version}
%if 0%{with python3}
py.test-%{python3_version}
%endif  # with python3
%if 0%{with python3_other}
py.test-%{python3_other_version}
%endif  # with python3_other
%endif  # with tests


%install
[ "%buildroot" = "/" ] || rm -rf "%buildroot"

%if 0%{with python3_other}
%py3_other_install
%endif  # with python3_other
%if 0%{with python3}
%py3_install
%endif  # with python3
%py2_install


%files
%defattr(-,root,root,-)
%{python2_sitelib}/inflection.py*
%{python2_sitelib}/inflection-%{version}-*.egg-info

%doc README.rst CHANGES.rst

%if 0%{with python3}
%files -n python%{python3_pkgversion}-%project_name
%defattr(-,root,root,-)
%{python3_sitelib}/inflection.py
%{python3_sitelib}/__pycache__/inflection.*.py*
%{python3_sitelib}/inflection-%{version}-*.egg-info

%doc README.rst CHANGES.rst
%endif  # with python3

%if 0%{with python3_other}
%files -n python%{python3_other_pkgversion}-%project_name
%defattr(-,root,root,-)
%{python3_other_sitelib}/inflection.py
%{python3_other_sitelib}/__pycache__/inflection.*.py*
%{python3_other_sitelib}/inflection-%{version}-*.egg-info

%doc README.rst CHANGES.rst
%endif  # with python3_other


%clean
[ "%buildroot" = "/" ] || rm -rf "%buildroot"


%changelog
* Tue Jan 08 2019 Mikhail Ushanov <gm.mephisto@gmail.com> - 0.3.1-2
- Build python3 package for epel7
- Use python build and install macros

* Tue Apr 12 2016 Mikhail Ushanov <gm.mephisto@gmail.com> - 0.3.1-1
- Initial build.
