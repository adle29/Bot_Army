import leftBottom_frame
import center_frame

import database 
import types

from tabulate import tabulate

from botnet import bot
import global_variables

host_count = 0
hosts = {}

printB = leftBottom_frame.printTextHistory

class Host:
  def __init__(self, address, id, hostname=""):
    self.address = address
    self.id = id
    self.os_type = ''
    self.os_vendor = ''
    self.os_family = ''
    self.os_gen = ''
    self.os_accuracy = ''
    self.status = 'UP'
    self.openPorts = []
    self.controlled = False
    self.bot_assigned = -1
    self.scanned = False
    self.hashes = ""
    self.hardened = False
    self.hostname = hostname
    self.ssh = []

  def something():
    print self.address

def add_existant_Host(host):
  global host_count

  newHost = Host(host['address'], host['id'])
  newHost.hostname = host['hostname']
  newHost.os_type = host['os_type']
  newHost.os_vendor = host['os_vendor']
  newHost.os_family = host['os_family']
  newHost.os_gen = host['os_gen']
  newHost.os_accuracy = host['os_accuracy']
  newHost.openPorts = host['openPorts']
  newHost.controlled = host['controlled']
  newHost.bot_assigned = host['bot_assigned']
  newHost.scanned = host['scanned']
  newHost.hashes = host['hashes']
  newHost.hardened = host['hardened']
  newHost.hostname = host['hostname']

  hosts[str(host['id'])] = newHost
  host_count += 1


def create_host(addr, hostname=""):
  global host_count

  if is_there_host_with_address(addr) == False:
    newHost = Host(addr, host_count, hostname=hostname)
    hosts[str(host_count)] = newHost
    database.save_host(newHost)
    host_count += 1

def erase_hosts():
  global host_count
  global hosts

  host_count = 0
  hosts = {}


def show_host(id):
  host = get_host(id)
  if host != None:
      txt = ("[+] HOST:" + str(host.id) + " | IP address: " + host.address + "\n" +
           " [+] SPECIFICATIONS:" + "\n" +
           "  [*] hostname: " +host.hostname + "\n" +
           "  [*] os_type: " +host.os_type + "\n" +
           "  [*] os_vendor: " +host.os_vendor + "\n" +
           "  [*] os_family: " +host.os_family + "\n" +
           "  [*] os_gen: " +host.os_gen + "\n" +
           "  [*] os_accuracy: " +host.os_accuracy + "\n")

      ports = host.openPorts
      txt += " [+] PORTS opened:" + "\n"
      if len(ports) != 0:
        for p in ports:
          txt += "   [*] Port: " + p + " open." + "\n"

      center_frame.bottom_tx_box_print(txt)
  else:
    txt = "[!] No Host with ID: " + str(id) 
    center_frame.bottom_tx_box_print(txt)

def print_hosts():

  if len(hosts.keys()) == 0:
    center_frame.bottom_tx_box_print("[-] No targets in the scope yet.")

  else: 
    table = []
    for hst in hosts.keys():
      selected_host = hosts[hst]
      table.append([selected_host.id, 
                    selected_host.address, 
                    selected_host.hostname,
                    global_variables.SCANNED[selected_host.scanned],
                    global_variables.SCANNED[selected_host.controlled],
                    global_variables.SCANNED[selected_host.hardened]])

    headers = tabulate(table, 
               headers=["ID","IP ADDRESS", "HOSTNAME", "SCANNED", "CONTROLLED", "HARDENED"], 
               tablefmt="fancy_grid", 
               stralign="center",
               numalign="center")
    center_frame.bottom_tx_box_print(headers)

def create_hosts_from_file(filename):
  hostsFile = open(filename, 'r')
  for host in hostsFile.readlines():
    host = host.strip('\n')
    create_host(host)


def get_host(id):
  if id in hosts.keys():
    return hosts[id]
  else:
    return None

def get_host_by_address(address):
  for id in hosts.keys():
    if host[id].address == address:
      return hosts[id]

  return None

def is_there_host_with_address(address):
  for key in hosts.keys():
    if hosts[key].address == address:
      return True

  return False

def get_hosts():
  return hosts

