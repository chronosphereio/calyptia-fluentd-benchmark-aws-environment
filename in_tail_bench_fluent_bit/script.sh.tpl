#!/bin/sh

sudo mkfs -t ext4 ${mount_point}
sudo mkdir /data
sudo chown ${connecting_user} /data
sudo chgrp ${connecting_user} /data
sudo chmod 755 /data
sudo mount ${mount_point} /data