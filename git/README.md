# arista-extensions > git

## Create the SWIX from the Fedora Git RPM

Install the Yum Utilities to download the RPM and resolve dependencies automatically,

~~~~
yum install yum-utils
~~~~

Then make the RPM/SWIX

~~~~
mkdir -p /mnt/sdb1/{downloads/git,git}
yumdownloader --resolve --destdir=/mnt/sdb1/downloads/git git
cp /mnt/sdb1/downloads/git/*.rpm /mnt/sdb1/git
~~~~

Create the manifest file

~~~~
cd /mnt/sdb1/git
cat > manifest.txt <<EOF
format: 1
EOF

for file in *.rpm; do
    echo $(ls "$file")-sha1: $(cat "$file" | sha1sum | cut -f 1 -d " ") >> manifest.txt
done
~~~~

Create the SWIX

    swix create git-1.7.4.4-1.swix *.rpm

Then return to the CLI and load the SWIX and set it to run on boot

~~~~
exit
copy file:/mnt/sdb1/git/git-1.7.4.4-1.swix extension:
extension git-1.7.4.4-1.swix
copy installed-extensions boot-extensions
~~~~
