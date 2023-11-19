# Shell code for making a ram fs, for if you don't want to destroy your ssd with creating and reciving big files.
# This might crash your system if you don't have good amounts of ram
sudo mkdir /mnt/ramfs rcv
sudo mount -t ramfs -o size=25g,maxsize=25g ramfs /mnt/ramfs
sudo chown -R $(whoami):$(whoami) /mnt/ramfs

sudo truncate -s 25G /mnt/ramfs/ramdisk.img
sudo mkfs.ext4 /mnt/ramfs/ramdisk.img
sudo mount /mnt/ramfs/ramdisk.img rcv
sudo chown -R $(whoami):$(whoami) rcv
