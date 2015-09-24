%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%define sname	oracle_fdw

Summary:	A PostgreSQL Foreign Data Wrapper for Oracle.
Name:		%{sname}%{pgmajorversion}
Version:	1.2.0
Release:	2%{?dist}
Group:		Applications/Databases
License:	PostgreSQL
URL:		http://oracle-fdw.projects.postgresql.org/
Source0:	https://github.com/laurenz/oracle_fdw/archive/ORACLE_FDW_1_2_0.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	postgresql%{pgmajorversion}-server
BuildRequires:	oracle-instantclient11.2-basic
BuildRequires:	oracle-instantclient11.2-devel
Requires:	postgresql%{pgmajorversion}-server
Requires:	oracle-instantclient11.2-basic
AutoReqProv:    no

# Override RPM dependency generation to filter out libclntsh.so.
# http://fedoraproject.org/wiki/PackagingDrafts/FilteringAutomaticDependencies
#%global		_use_internal_dependency_generator 0

%description
Provides a Foreign Data Wrapper for easy and efficient read access from
PostgreSQL to Oracle databases, including pushdown of WHERE conditions and
required columns as well as comprehensive EXPLAIN support.

%prep
#%setup -q -n %{sname}-%{version}
%setup -q -n oracle_fdw-ORACLE_FDW_1_2_0

%build
make PG_CONFIG=%{pginstdir}/bin/pg_config %{?_smp_mflags}

%install
%{__rm} -rf  %{buildroot}
make install DESTDIR=%{buildroot} PG_CONFIG=%{pginstdir}/bin/pg_config %{?_smp_mflags}
mv %{buildroot}/usr/share/doc/pgsql/extension/README.oracle_fdw %{buildroot}%{pginstdir}/share/extension
mkdir -p %{buildroot}/etc/ld.so.conf.d/
cp %{_specdir}/oracle-instantclient11-x86_64.conf %{buildroot}/etc/ld.so.conf.d/

# This option performs regression tests which need some preparations
#%check
#make installcheck PG_CONFIG=%{pginstdir}/bin/pg_config %{?_smp_mflags} PGUSER=postgres

%clean
%{__rm} -rf  %{buildroot}

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/README.*
/etc/ld.so.conf.d/oracle-instantclient11-x86_64.conf

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Wed Jun 10 2015 Vitaly Agapov <v.agapov@quotix.com> 1.2.0-2
- Added /etc/ld.so.conf.d/oracle-instantclient11-x86_64.conf

* Tue Jun 9 2015 Vitaly Agapov <v.agapov@quotix.com> 1.2.0-1
- Initial RPM
