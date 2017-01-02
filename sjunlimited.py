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

def macchangerParser(text):
  adr = re.compile(r'(..:..:..:..:..:..)')  #REGEX for MAC address
  cMac = adr.findall(text)
  return cMac

def wlanInterface():
  with open('/proc/net/wireless', 'r') as f:
    f.readline() #2 useless rows of crap
    f.readline()
    winterface = f.readline().split()[0]
    return winterface[0:-1]


device = wlanInterface()


#Strings for getOutput()
#This was a lot faster than rewriting getOutput to take extra arguments so.. just ignore this. :)
macacmd = "macchanger -a %s" % device
macscmd = "macchanger -s %s" % device
iwcmd = "iwlist %s scan" % device

#Settings
hardMac = macchangerParser(getOutput(macscmd))[1]
currentMac = hardMac

#---------------



#control you are near the network
essids = getOutput(iwcmd)
if essids.find("SJ") == (-1):
  sys.exit("Not near SJ network. Aborting")



#main program
print "Spoofing mac address"
attempts = 0

"""An issue with macchanger, where it assigns a new MAC address but then changes back to the permanent MAC before connecting.
This loop will run until it has made sure it's connected using a new MAC
""" 
while currentMac==hardMac:
  call(["ifconfig", device, "down"])
  getOutput(macacmd) #shh, this is obviously intended
  call(["ifconfig", device, "up"])
  time.sleep(1)
  attempts += 1
  print "Connecting to SJ after %d attempts" % attempts
  Popen(["nmcli", "device", "wifi", "connect", "SJ"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  checkMac = getOutput(macscmd)
  currentMac = macchangerParser(checkMac)[0]

print "Connected with MAC: ", currentMac
print "go to ombord.sj.se to activate"


#uncomment to make default browser open the activation page.
#webbrowser.open("http://ombord.sj.se/",new=2)
