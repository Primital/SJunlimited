# SJunlimited
unix script to reconnect your wifi with new mac adress when you run out of data on SJ network

Dependencies:
macchanger
nmcli


Known issues:
Sometimes the script will fail to up the interface, solution is:
sudo ifconfig [your interface] down; sudo ifconfig [your interface] up


Not sure what happens if your device has more than one wireless interface. I guess you better just die then.


