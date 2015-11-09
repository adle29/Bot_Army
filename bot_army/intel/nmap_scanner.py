import nmap
import leftTop_frame 
import leftBottom_frame
from threading import Thread

tgtHost = ""
tgtPorts = ""

def nmapScan(tgtHost, tgtPort):
  tgtHost = tgtHost
  nmScan = nmap.PortScanner()
  nmScan.scan(tgtHost, tgtPort)
  state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
  leftTop_frame.printText("[*] " + tgtHost + " tcp/" + tgtPort + " " + state +"\n")

def inititate_nmap_scanner(args):
  leftTop_frame.printText("[*]Nmap Scanner Program Initiated.\n")
  tgtHost = args[0]
  tgtPorts = args[1].split(',')
  
  if (tgtHost == None) | (tgtPorts[0] == None):
    leftTop_frame.printText("[-]Missing Arguments")
    exit(0)
  
  for tgtPort in tgtPorts:
    t = Thread(target=nmapScan, args=(tgtHost, tgtPort))
    t.start()
  
