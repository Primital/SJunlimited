# UPDATE 2018
SJ has removed the data limit on the on-board WiFi, obviating the need for this script. Thus, it will no longer be maintained.

# SJunlimited 
python2.7 script for unix to reconnect your wifi with new mac adress when you run out of data on SJ network

Use:

sudo python sjunlimited.py



Dependencies:

macchanger

nmcli


Known issues:

Sometimes the script will fail to up the interface, terrible solution:

sudo ifconfig [your interface] down; sudo ifconfig [your interface] up


Not sure what happens if your device has more than one wireless interface. I guess you better just die then.


