#!/bin/sh
sudo ifconfig wlp3s0 down
sudo macchanger -a wlp3s0
sleep 1
sudo ifconfig wlp3s0 up
