Summary: BIRD Internet Routing Daemon
Name: bird
Version: 1.6.8
Release: 1
License: GPL
Group: Networking/Daemons
Source: ftp://bird.network.cz/pub/bird/bird-%{version}.tar.gz
Source1: https://raw.githubusercontent.com/misakaio/arista-extensions/master/bird/bird.service
Source2: https://raw.githubusercontent.com/misakaio/arista-extensions/master/bird/bird6.service
Source3: https://raw.githubusercontent.com/misakaio/arista-extensions/master/bird/etc_bird.conf
Source4: https://raw.githubusercontent.com/misakaio/arista-extensions/master/bird/etc_bird6.conf
Url: http://bird.network.cz
Requires: /sbin/chkconfig
BuildRequires: readline-devel ncurses-devel flex bison autoconf gcc make
AutoReqProv: no

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

install -d $RPM_BUILD_ROOT/mnt/flash/bird
install -d $RPM_BUILD_ROOT/lib/systemd/system

install $RPM_SOURCE_DIR/bird.service $RPM_BUILD_ROOT/lib/systemd/system/bird.service
install $RPM_SOURCE_DIR/bird6.service $RPM_BUILD_ROOT/lib/systemd/system/bird6.service
install $RPM_SOURCE_DIR/etc_bird.conf $RPM_BUILD_ROOT/mnt/flash/bird/bird.conf.dist
install $RPM_SOURCE_DIR/etc_bird6.conf $RPM_BUILD_ROOT/mnt/flash/bird/bird6.conf.dist

%post
ln -s /mnt/flash/bird /etc/bird
ln -s /mnt/flash/bird/bird.conf /etc/bird.conf
ln -s /mnt/flash/bird/bird6.conf /etc/bird6.conf
[ ! -f /mnt/flash/bird/bird.conf ] && cp /mnt/flash/bird/bird.conf{.dist,}
[ ! -f /mnt/flash/bird/bird6.conf ] && cp /mnt/flash/bird/bird6.conf{.dist,}
ldconfig
systemctl enable bird bird6
systemctl start bird bird6

%preun
if [ $1 = 0 ] ; then
    systemctl stop bird bird6
    systemctl disable bird bird6
fi

%files
%attr(755,root,root) /usr/sbin/bird
%attr(755,root,root) /usr/sbin/bird6
%attr(755,root,root) /usr/sbin/birdc
%attr(755,root,root) /usr/sbin/birdc6
%attr(755,root,root) /usr/sbin/birdcl
%attr(755,root,root) /lib/systemd/system/bird.service
%attr(755,root,root) /lib/systemd/system/bird6.service
%attr(664,root,eosadmin) /mnt/flash/bird/bird.conf.dist
%attr(664,root,eosadmin) /mnt/flash/bird/bird6.conf.dist
