# arista-bird

Arista provides a good BGP daemon, but Bird can offer significantly more flexibility. This repo contains a pre-compiled SWIX and instructions to make your own.

## Download

| Version | Download Link |
| --- | --- |
| 4.13.14M | [bird-1.6.0-1.i386.swix](swix/bird-1.6.0-1.swix) |

## Configuration

After installation, the main `bird.conf` can be found in

    /mnt/flash/bird/bird.conf

This will persist over reboots, and the service is automatically monitored for startup/crashes etc. by the main EOC monitoring dameon.

## Self Compile

### Initial preparation

 1. Download and set up a VEOS instance with the matching EOS version
 1. Create a 3GB disk and attack to the VEOS instance (used as a scratch disk)
 1. Boot the VEOS guest

### After boot

Partition the second disk to use for additional space,

~~~~
bash sudo su
fdisk /dev/sdb
mkfs.ext2 /dev/sdb1
~~~~

Mount the new partition and bind mount directories,

~~~~
mkdir -p /mnt/sdb1
mount /dev/sdb1 /mnt/sdb1
mkdir -p /mnt/sdb1/{bin,var/cache/yum,usr}
rsync -axpHSD --numeric-ids -vP --delete /var/cache/yum/ /mnt/sdb1/var/cache/yum/
rsync -axpHSD --numeric-ids -vP --delete /usr/ /mnt/sdb1/usr/
rsync -axpHSD --numeric-ids -vP --delete /bin/ /mnt/sdb1/bin/

mount --bind /mnt/sdb1/var/cache/yum /var/cache/yum
mount --bind /mnt/sdb1/usr /usr
mount --bind /mnt/sdb1/bin /bin
~~~~

Add the Fedora repos

~~~~
cd /etc/yum.repos.d/

cat > fedora.repo <<EOF
[fedora]
name=Fedora 14 - i686
failovermethod=priority
baseurl=http://dl.fedoraproject.org/pub/archive/fedora/linux/releases/14/Everything/i386/os/
exclude=kernel,fedora-logos
exclude=kernel,fedora-logos
enabled=1
gpgcheck=0
diskspacecheck=0
EOF

cat > fedora-updates.repo <<EOF
[fedora-updates]
name=Fedora 14 Updates - i686
failovermethod=priority
baseurl=http://dl.fedoraproject.org/pub/archive/fedora/linux/updates/14/i386/
exclude=kernel,fedora-logos
exclude=kernel,fedora-logos
enabled=1
gpgcheck=0
diskspacecheck=0
EOF

echo diskspacecheck=0 >> /etc/yum.conf
~~~~

### Create the RPM and SWIX

Using the [spec file](https://raw.githubusercontent.com/choco-loo/arista-bird/master/arista-bird.spec), create the RPM

~~~~
yum install rpmdevtools readline-devel ncurses-devel flex bison autoconf gcc make
rpmdev-setuptree
cd /root/rpmbuild
wget --no-check-certificate -O SPECS/bird.spec https://raw.githubusercontent.com/choco-loo/arista-bird/master/arista-bird.spec
wget --no-check-certificate -O SOURCES/bird.init https://raw.githubusercontent.com/choco-loo/arista-bird/master/arista-bird.init
wget --no-check-certificate -O SOURCES/v1.6.0.tar.gz https://github.com/BIRD/bird/archive/v1.6.0.tar.gz
rpmbuild --target=i686 -v -bb --clean SPECS/bird.spec
~~~~

Then make the bird RPM/SWIX

~~~~
mkdir -p /mnt/sdb1/bird
cp /root/rpmbuild/RPMS/i686/bird*.rpm /mnt/sdb1/bird
~~~~

Create the manifest file

~~~~
cd /mnt/sdb1/bird
cat > manifest.txt <<EOF
format: 1
EOF

for file in *.rpm; do
    echo $(ls "$file")-sha1: $(cat "$file" | sha1sum | cut -f 1 -d " ") >> manifest.txt
done
~~~~

Create the SWIX

    swix create bird-1.6.0-1.swix *.rpm

Then return to the CLI and load the SWIX and set it to run on boot

~~~~
exit
copy file:/mnt/sdb1/bird/bird-1.6.0-1.swix extension:
extension bird-1.6.0-1.swix
copy installed-extensions boot-extensions
~~~~
