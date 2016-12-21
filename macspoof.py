import os
import webbrowser
from subprocess import *
import sys
import errno
import time
import re

if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")


def getOutput(command):
  cmd = Popen(command.split(' '), stdin=PIPE, stdout=PIPE, stderr=PIPE)
  output, errors = cmd.communicate(b"")
  return output

#Settings
device = "wlp3s0" #CHANGE THIS TO YOUR WIRELESS NETWORK CARD
usedMacs = ["74:2f:68:38:01:c7"]
hardMac = "74:2f:68:38:01:c7"
currentMac = hardMac


#control you are near the network
#iwlist = Popen(['iwlist',device, 'scan'],stdin=PIPE, stdout=PIPE, stderr=PIPE)
#essids, essiderr = iwlist.communicate(b"")
essids = getOutput("iwlist wlp3s0 scan")
if essids.find("SJ") == (-1):
  sys.exit("Not near SJ network. Aborting")


def macchangerParser(text):
  adr = re.compile(r'(..:){5}..')  #REGEX for MAC address
  cMac = adr.search(text)
  return cMac.group()



#main program
print "Spoofing mac address"
attempts = 0

"""An issue with macchanger, where it assigns a new MAC address but then changes back to the permanent MAC before connecting.
This loop will run until it has made sure it's connected using a new MAC
""" 
while currentMac in usedMacs:
  call(["ifconfig", device, "down"])
  getOutput("macchanger -a wlp3s0")
  call(["ifconfig", device, "up"])
  time.sleep(1)
  attempts += 1
  print "Connecting to SJ after %d attempts" % attempts
  Popen(["nmcli", "device", "wifi", "connect", "SJ"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  checkMac = getOutput("macchanger -s wlp3s0")
  currentMac = macchangerParser(checkMac)

print "Connected with MAC: ", currentMac
print "go to ombord.sj.se to activate"
#webbrowser.open("http://ombord.sj.se/",new=2)
