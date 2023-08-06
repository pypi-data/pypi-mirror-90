#!/bin/bash

GITHUB_DIR=~/evo-track/ingress/client
#NEW_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
NEW_DIR=~/ingress

rm "$NEW_DIR"
ln -s "$GITHUB_DIR" "$NEW_DIR"

sudo rm /etc/systemd/system/evo-track.service
sudo ln -s "$NEW_DIR"/evo-track.service /etc/systemd/system/evo-track.service

sudo systemctl enable evo-track.service
sudo systemctl start evo-track.service
sudo systemctl status evo-track.service

#sudo mkdir -p /var/evo-track/ingress

#sudo ln -s "$NEW_DIR"/delivered/ /var/evo-track/ingress/
#sudo ln -s "$NEW_DIR"/queue/ /var/evo-track/ingress/

