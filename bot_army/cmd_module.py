import modules
import leftBottom_frame
import center_frame 
import re
import database
import shlex 

from threading import Thread
from multiprocessing import Process
from tabulate import tabulate
from global_variables import *
import __builtin__

printM = center_frame.main_tx_box_print
printMB = center_frame.bottom_tx_box_print
printB = leftBottom_frame.printTextHistory
speak = leftBottom_frame.speak

def pre_start():
	print "[+]Presets loaded"
	cmd = "add ssh, 192.168.132.144, admin"
	printB(cmd)
	cmd_assert(cmd)

	#cmd = "bot:0 scan host:0"
	#cmd_assert(cmd)

	# cmd = "bot:1 assign host:1"
	# cmd_assert(cmd)

def cmd_assert(cmd):
	cmd_array = ""

	#SOME FORMATTING
	if ',' in cmd:
		cmd_array = cmd.split(',')
	else:
		cmd_array = cmd.split(' ')

	#REGEX MATCHING
	if re.match("add\sbot\s[0-9]", cmd, flags=0):
		num = int(cmd_array[2])

		for i in range(0, num):
			modules.add_bot()

		modules.show_bots()

	elif re.match("add\shost\s\d{1,3}\.\d{1,3}\.\d{1,3}", cmd, flags=0):
		addr = cmd_array[2]
		modules.add_host(addr)
		modules.print_hosts()

	elif re.match("add\shosts\s-f\s", cmd, flags=0):
		filename = cmd_array[3]
		modules.add_hosts_from_file(filename)
		modules.print_hosts()

	elif re.match("add\shost\s[0-9]", cmd, flags=0):
		printB("Command in construction")

	elif re.match("add\sssh", cmd, flags=0):
		message = """[+] Specific command: %s\n[+] Address/host id: %s\n[+] Account: %s
		""" % (cmd_array[0], cmd_array[1], cmd_array[2])

		printB(message)


	elif re.match("bot [0-9]\sscan\shost [0-9]", cmd, flags=0):
		bot_id = cmd_array[1]
		action = "scan"
		host_id = cmd_array[4]
		printB("[+] Bot("+ str(bot_id)+ ") making " + action + " on host(" + host_id+")")

		t=Thread(target=modules.bot_action_host, args=(bot_id, action, [host_id]))
		#t.daemon=True
		t.start()
	
	elif re.match("bot [0-9]\sattack\shost [0-9]", cmd, flags=0):
		bot_id = cmd_array[1]
		action = "attack"
		host_id = cmd_array[4]
		printB("[+] Bot("+ str(bot_id)+ ") making " + action + " on host(" + host_id +")")


		t=Thread(target=modules.bot_action_host, args=(bot_id, action, [host_id]))
		t.start()

	elif re.match("bot [0-9]\sassign\shost [0-9]", cmd, flags=0):
		bot_id = cmd_array[1]
		action = "assign"
		host_id = cmd_array[4]
		printB("[+] Bot:"+ str(bot_id)+ " "+ action + "ed to host:" + host_id)

		t=Thread(target=modules.bot_action_host, args=(bot_id, action, [host_id]))
		t.start()

	elif re.match("bot [0-9]\sprotect\shost [0-9]", cmd, flags=0):
		bot_id = cmd_array[1]
		action = "protect"
		host_id = cmd_array[4]
		printB("[+] Bot:"+ str(bot_id)+ " "+ action + "ing to host:" + host_id)

		t=Thread(target=modules.bot_action_host, args=(bot_id, action, [host_id]))
		t.start()

	elif re.match("bot [0-9]\sstick\shost [0-9]", cmd, flags=0):
		bot_id = cmd_array[1]
		host_id = cmd_array[4]
		printB("[+] Bot("+ str(bot_id)+ ") permanently assigned to host(" + host_id + ")")

		modules.bot_permanent_assignment(bot_id, [host_id])

	elif re.match("bot [0-9]\sping\shost [0-9]", cmd, flags=0):
		bot_id = cmd_array[1]
		action = "ping"
		host_id = cmd_array[4]
		printB("[+] Bot:"+ str(bot_id)+ " is pinging host:" + host_id)

		t=Thread(target=modules.bot_action_host, args=(bot_id, action, [host_id]))
		t.start()

	elif re.match("bot [0-9]\spsweep\s\d{1,3}\.\d{1,3}\.\d{1,3}", cmd, flags=0):
		bot_id = cmd_array[1]
		subnet = cmd_array[3]
		printB("[+] Bot:"+ str(bot_id)+ " is pinging range:" + subnet)

		t=Thread(target=modules.bot_ping_sweep, args=(bot_id, subnet))
		t.daemon=True
		t.start()

	elif re.match("delete\sbot\s[0-9]", cmd, flags=0):
		printB("Command in construction")

	elif re.match("delete\shost\s[0-9]", cmd, flags=0):
		printB("Command in construction")

	elif re.match("restart system", cmd, flags=0):
		database.erase_all_data()
		modules.erase_bots()
		modules.erase_hosts()

	elif re.match("save", cmd, flags=0):
		modules.update_hosts_and_bots()

	elif re.match("show\sbot\s[0-9]", cmd, flags=0):
		id = cmd_array[2]
		modules.show_bot(id)

	elif re.match("show\srecord\sbot\s[0-9]", cmd, flags=0):
		id = cmd_array[3]
		modules.show_full_mode_bot_record(id)

	elif re.match("show\srecords", cmd, flags=0):
		txt = "[+] Ping Sweep Hosts\n"
		# for key in hosts.keys():
		# 	state = hosts[key]['nmap']['scanstats']['uphosts']
		# 	if state == '1':
		# 		txt += "[+] Host " + key + " is UP " 
		# printB(txt)

	elif re.match("show\shost\s[0-9]", cmd, flags=0):
		id = cmd_array[2]
		modules.show_host(id)

	elif "show hosts" == cmd:
		modules.show_hosts()

	elif "show bots" == cmd:
		modules.show_bots()

	elif "show shells" == cmd:
		modules.show_shells()

	elif "help" == cmd or "h" == cmd:
		table = [["*add bot <num>"],
				["*add host <ip address>"],
				["*add hosts -f <file path>"],
				["*bot <num> scan host <num>"],
				["*bot <num> attack host <num>"],
				["*bot <num> assign host <num>"],
				["*bot <num> stick host <num>"],
				["*bot <num> psweep <ip></range>"],
				["*bot <num> ping host <num>"],
				["*help"],
				["*restart system"],
				["*show bot <num>"],
				["*show bots"],
				["*show host <num>"],
				["show hosts"],
				["show shells"],
				["show records"],
				["preset"]]

		headers = tabulate(table, 
               headers=["HELP"], 
               tablefmt="grid")

		printB(headers)

	elif "preset" == cmd:
		pre_start()

	else:
		printB("[-]No methods available.")

