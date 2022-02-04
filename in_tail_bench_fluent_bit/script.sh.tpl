#!/bin/sh

sudo mkfs -t ext4 /dev/xvdf
sudo mkdir /data
sudo chown ${connecting_user} /data
sudo chgrp ${connecting_user} /data
sudo chmod 755 /data
sudo mount /dev/xvdf /data