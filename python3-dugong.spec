#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	dugong
Summary:	A HTTP 1.1 client module
# Name must match the python module/package name (as in 'import' statement)
Name:		python3-%{module}
Version:	3.0
Release:	1
License:	PSF
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/d/dugong/dugong-%{version}.tar.bz2#md5=f81bc01e7656ced466e1eb059952c21f
# Source0-md5:	f81bc01e7656ced466e1eb059952c21f
URL:		https://bitbucket.org/nikratio/python-dugong
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A HTTP 1.1 client module.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
# CC/CFLAGS is only for arch packages - remove on noarch packages
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

# in case there are examples provided
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif