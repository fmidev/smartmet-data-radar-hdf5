%define smartmetroot /smartmet

Name:           smartmet-data-radar-hdf5
Version:        18.4.27
Release:        1%{?dist}.fmi
Summary:        SmartMet Data Radar HDF5 Odim
Group:          System Environment/Base
License:        MIT
URL:            https://github.com/fmidev/smartmet-data-radar-hdf5
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%{?el6:Requires: smartmet-qdconversion}
%{?el7:Requires: smartmet-qdtools}

%description
TODO

%prep

%build

%pre

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT

mkdir -p .%{smartmetroot}/cnf/cron/{cron.d,cron.hourly}
mkdir -p .%{smartmetroot}/editor/radar
mkdir -p .%{smartmetroot}/logs/data
mkdir -p .%{smartmetroot}/run/data/radar/bin
mkdir -p .%{smartmetroot}/data/incoming/radar

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.d/radar.cron <<EOF
* * * * * /smartmet/run/data/radar/bin/doradar.sh 
EOF

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.hourly/clean_data_radar <<EOF
#!/bin/sh
# Clean RADAR HDF5 data
cleaner -maxage 12 '_radar_' /smartmet/editor/radar
find /smartmet/data/incoming/radar -type f -mmin +180 -delete
EOF

install -m 755 %_topdir/SOURCES/smartmet-data-radar-hdf5/doradar.sh %{buildroot}%{smartmetroot}/run/data/radar/bin/

%post

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,smartmet,smartmet,-)
%config(noreplace) %{smartmetroot}/cnf/cron/cron.d/radar.cron
%config(noreplace) %attr(0755,smartmet,smartmet) %{smartmetroot}/cnf/cron/cron.hourly/clean_data_radar
%{smartmetroot}/*

%changelog
* Fri Apr 27 2018 Mikko Rauhala <mikko.rauhala@fmi.fi> 18.4.27-1.el7.fmi
- Initial Version
