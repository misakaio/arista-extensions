Summary: Network diagnostic tool combining 'traceroute' and 'ping'
Name: mtr
Version: 0.94
Release: 1
License: GPLv2
Source: https://github.com/traviscross/mtr/archive/v%{version}.tar.gz
Url: https://github.com/traviscross/mtr
BuildRequires: readline-devel ncurses-devel autoconf automake libtool git
AutoReqProv: no

%description
MTR combines the functionality of the 'traceroute' and 'ping' programs
in a single network diagnostic tool.
 
When MTR is started, it investigates the network connection between the
host MTR runs on and the user-specified destination host. Afterwards it
determines the address of each network hop between the machines and sends
a sequence of ICMP echo requests to each one to determine the quality of
the link to each machine. While doing this, it prints running statistics
about each machine.

%prep
%setup -n mtr-%{version}

%build

./bootstrap.sh
./configure --without-gtk
make

%install
install -D -p -m 0755 mtr %{buildroot}%{_sbindir}/mtr
install -D -p -m 0755 mtr-packet %{buildroot}%{_bindir}/mtr-packet

%post
setcap cap_net_raw+ep %{_bindir}/mtr-packet

%files
%{_sbindir}/mtr
%{_bindir}/mtr-packet