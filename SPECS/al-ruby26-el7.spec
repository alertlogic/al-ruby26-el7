#################
#
# Author:      Des Jones (dejones@alertlogic.com)
# Project:     defender automation
# Date:        Fri 14 Feb 17:39:51 GMT 2020
# Version:     1.0
# Git:         git@github.com:alertlogic/al-ruby26-el7.git
# Notes:       rpmbuild -ba al-ruby26-el7
#              please manage versioning automagically with git tags
# 
###################################################

Name:       al-ruby26-el7
Version:    %{version}
Release:    %{release}
Summary:    AlertLogic al-ruby26-el7
License:    AlertLogic (c). All rights reserved.
BuildArch:  noarch
Requires:   al-s3repo
Requires(pre):   rh-ruby26-ruby
Requires(pre):   rh-ruby26-ruby-devel
Requires(pre):   rh-ruby26-rubygems-devel
Requires(pre):   gcc
Requires(pre):   make
Requires(pre):   libffi-devel
Requires(pre):   rpm-build

%description
Install and configure al-ruby26-el7

%prep
# add sources
cp -R %{_sourcedir}/%{name}/* .

%build
cat > %{name}.sh <<'EOF'
#!/bin/bash

# rpm macro variables
NAME=%{name}
VERSION=%{version}

# install/update logic
if [ "${1}" == 1 ]; then # if install
  for arg in $(ls /opt/rh/rh-ruby26/root/bin/*); do
    bin=$(basename $arg)
    ln -sf $arg /usr/bin/${bin}26
    if [ ! -f /usr/bin/${bin} ]; then
      ln -s $arg /usr/bin/${bin}
    fi
  done
  # add man pages
  if ! egrep -q "^\s*MANDATORY_MANPATH\s*/opt/rh/rh-ruby26/root/usr/local/share/man\s*$" /etc/man_db.conf; then
    echo "MANDATORY_MANPATH                       /opt/rh/rh-ruby26/root/usr/local/share/man" >> /etc/man_db.conf
  fi
  if ! egrep -q "^\s*MANDATORY_MANPATH\s*/opt/rh/rh-ruby26/root/usr/share/man\s*$" /etc/man_db.conf; then
    echo "MANDATORY_MANPATH                       /opt/rh/rh-ruby26/root/usr/share/man" >> /etc/man_db.conf
  fi
  # update libraries
  ldconfig
  # install gems
  /usr/local/sbin/al-ruby26-gem-install.sh || echo "Could not download gems! Please run /usr/local/sbin/al-ruby26-gem-install.sh" 1>&2
  echo "script installed and ran sucessfully" 1>&2
elif [ "${1}" == 2 ]; then # if update
  # update libraries
  ldconfig
  echo "script updated and ran sucessfully" 1>&2
fi

# if update or install
echo "install or update ran succesfully" 1>&2
EOF

%install
cp -R {usr,etc}/ %{buildroot}/
install -m 755 %{name}.sh %{buildroot}/usr/local/sbin/%{name}.sh

%files
/usr/local/sbin/*
/usr/local/share/%{name}/*
%config(noreplace) /etc/ld.so.conf.d/*

%pre

%post
/usr/local/sbin/%{name}.sh $1

%preun
if [ $1 == 0 ]; then
  # remove man pages
  sed -i '/^\s*MANDATORY_MANPATH\s*\/opt\/rh\/rh-ruby26\/root\/usr\/local\/share\/man\s*$/d' /etc/man_db.conf
  sed -i '/^\s*MANDATORY_MANPATH\s*\/opt\/rh\/rh-ruby26\/root\/usr\/share\/man\s*$/d' /etc/man_db.conf
  # remove symlinks
  for arg in $(ls /opt/rh/rh-ruby26/root/bin/*); do
    bin=$(basename $arg)
    if [ "$(readlink /usr/bin/${bin}26)" == "${arg}" ]; then
      rm -f /usr/bin/${bin}26
    fi
    if [ "$(readlink /usr/bin/${bin})" == "${arg}" ]; then
        rm -f /usr/bin/${bin}
    fi
  done
fi

%preun

%clean
if [ -d %{buildroot} ] ; then
  rm -rf %{buildroot}/*
fi

%changelog
# date "+%a %b %d %Y"
* Thu Mar 26 2020 desmond jones <dejones@alertlogic.com> %{version}-%{release}
- initial release

