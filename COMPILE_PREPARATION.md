# arista-extensions > self compilation

## Initial preparation

 1. Download and set up a VEOS instance with the matching EOS version
 1. Create a 3GB disk and attack to the VEOS instance (used as a scratch disk)
 1. Boot the VEOS guest

## After boot

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

## Final cleanup

Umount the filesystems

    umount -l /usr /bin /var/cache/yum
