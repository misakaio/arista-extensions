Summary: BIRD Internet Routing Daemon
Name: bird
Version: 1.6.0
Release: 1
License: GPL
Group: Networking/Daemons
Source: https://github.com/BIRD/bird/archive/v%{version}.tar.gz
Source1: https://raw.githubusercontent.com/choco-loo/arista-extensions/master/bird/arista-bird.init
Url: http://bird.network.cz
Requires: /sbin/chkconfig
BuildRequires: readline-devel ncurses-devel flex bison autoconf gcc make

%description
BIRD is dynamic routing daemon supporting IPv4 and IPv6 versions of routing
protocols BGP, RIP and OSPF.

%prep
%setup -n bird-%{version}

%build
if [ ! -f bird6 ] || [ ! -f birdc6 ]; then
    autoconf
    ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --enable-ipv6
    make
    mv bird bird6
    mv birdc birdc6
fi

if [ ! -f bird ] || [ ! -f birdc ] || [ ! -f birdcl ] || [ ! -f bird.conf ]; then
    make clean
    autoconf
    ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var
    make
fi


%install
rm -rf $RPM_BUILD_ROOT/*

make install prefix=$RPM_BUILD_ROOT/usr sysconfdir=$RPM_BUILD_ROOT/etc localstatedir=$RPM_BUILD_ROOT/var

rm $RPM_BUILD_ROOT/etc/bird.conf

install birdc6 $RPM_BUILD_ROOT/usr/sbin
install bird6 $RPM_BUILD_ROOT/usr/sbin
install birdcl $RPM_BUILD_ROOT/usr/sbin

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/mnt/flash/bird
install -d $RPM_BUILD_ROOT/etc/ProcMgr.d/inst

install $RPM_BUILD_DIR/bird-%{version}/misc/bird.init $RPM_BUILD_ROOT/etc/rc.d/init.d/bird
install bird.conf $RPM_BUILD_ROOT/mnt/flash/bird/bird.conf.dist
install $RPM_SOURCE_DIR/bird.init $RPM_BUILD_ROOT/etc/ProcMgr.d/inst/Bird

%post
ln -s /mnt/flash/bird/bird.conf /etc/bird.conf
sed -i -E 's>(.+route .+::/.+)>#\1>g' /mnt/flash/bird/bird.conf.dist
[ ! -f /mnt/flash/bird/bird.conf ] && cp /mnt/flash/bird/bird.conf{.dist,}
ldconfig
chkconfig --add bird
chkagent --add Bird
service ProcMgr reload

%preun
if [ $1 = 0 ] ; then
    /sbin/chkconfig --del bird
fi

%files
%attr(755,root,root) /usr/sbin/bird
%attr(755,root,root) /usr/sbin/bird6
%attr(755,root,root) /usr/sbin/birdc
%attr(755,root,root) /usr/sbin/birdc6
%attr(755,root,root) /usr/sbin/birdcl
%attr(755,root,root) /etc/rc.d/init.d/bird
%attr(755,root,root) /etc/ProcMgr.d/inst/Bird
%attr(664,root,eosadmin) /mnt/flash/bird/bird.conf.dist
