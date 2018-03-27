#!/bin/bash
set -ex

image=$1

if [[ $image =~ ^centos: ]]
then
    pkgcmd="yum"
    builddep="yum-builddep"
    sed -i '/^tsflags=/d' /etc/yum.conf
    yum install -y epel-release
    yum install -y @buildsys-build
    yum install -y yum-utils
    yum install -y git
    yum install -y rpmdevtools
    yum install -y yum-plugin-copr
    yum install -y pv
    yum copr enable -y edigiacomo/test
elif [[ $image =~ ^fedora: ]]
then
    pkgcmd="dnf"
    builddep="dnf builddep"
    sed -i '/^tsflags=/d' /etc/dnf/dnf.conf
    dnf install -y @buildsys-build
    dnf install -y 'dnf-command(builddep)'
    dnf install -y git
    dnf install -y rpmdevtools
    dnf install -y pv
    dnf copr enable -y edigiacomo/test
fi

$builddep -y libemos.spec

if [[ $image =~ ^fedora: || $image =~ ^centos: ]]
then
    pkgname="$(rpmspec -q --qf="libemos-%{version}-%{release}\n" libemos.spec | head -n1)"
    mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
    cp libemos.spec ~/rpmbuild/SPECS/
    spectool -g -R ~/rpmbuild/SPECS/libemos.spec
    rpmbuild -ba ~/rpmbuild/SPECS/libemos.spec 2>&1 | pv -q -L 3k
    find ~/rpmbuild/{RPMS,SRPMS}/ -name "${pkgname}*rpm" -exec cp -v {} . \;
    # TODO upload ${pkgname}*.rpm to github release on deploy stage
else
    echo "Unsupported image"
    exit 1
fi
