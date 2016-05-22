# arista-extensions > bird

Arista provides a good BGP daemon, but Bird can offer significantly more flexibility.

## Configuration

After installation, the main `bird.conf` can be found in

    /mnt/flash/bird/bird.conf

This will persist over reboots, and the service is automatically monitored for startup/crashes etc. by the main EOC monitoring dameon.

## Create the RPM and SWIX

Using the [spec file](https://raw.githubusercontent.com/choco-loo/arista-extensions/master/bird/arista-bird.spec), create the RPM

~~~~
yum install rpmdevtools readline-devel ncurses-devel flex bison autoconf gcc make
rpmdev-setuptree
cd /root/rpmbuild
wget --no-check-certificate -O SPECS/bird.spec https://raw.githubusercontent.com/choco-loo/arista-extensions/master/bird/arista-bird.spec
wget --no-check-certificate -O SOURCES/bird.init https://raw.githubusercontent.com/choco-loo/arista-extensions/master/bird/arista-bird.init
wget --no-check-certificate -O SOURCES/v1.6.0.tar.gz https://github.com/BIRD/bird/archive/v1.6.0.tar.gz
rpmbuild --target=i686 -v -bb --clean SPECS/bird.spec
~~~~

Then make the RPM/SWIX

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
