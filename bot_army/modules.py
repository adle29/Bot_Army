from forensics import *
from intel import *
from botnet import *
from network import *
import database
from threading import Thread

# def run_module_commad(method):
# 	t=Thread(target=bot.assign, args=(host, PORTS))
# 	t.start()

def m1():
	find_ip.specs()
	
def intel_1():
	nmap_scanner.specs()

def add_bot():
	bot_network.add_Bot()

def add_existant_bot(bot):
	bot_network.add_existant_Bot(bot)

def add_existant_host(host):
	hosts.add_existant_Host(host)

def add_host(address):
	hosts.create_host(address)

def add_host_property(id, property, values):
	database.update_host_property(id, property, values)

def print_hosts():
	hosts.print_hosts()

def add_hosts_from_file(filename):
	hosts.create_hosts_from_file(filename)

def bot_action_host(id, action, host):
	bot_network.bot_command(id, action, host)

def bot_ping_sweep(id, subnet):
	bot_network.bot_ping_sweep(id, subnet)

def erase_bots():
	bot_network.erase_bots()
	show_bots()

def erase_hosts():
	hosts.erase_hosts()
	show_hosts()

def load_bot_config():
	bot_network.load_bot_config()

def get_bot(id):
	return bot_network.get_bot(id)

def get_bots():
	return bot_network.get_bots()

def get_host(id):
	return hosts.get_host(id)	

def get_hosts():
	return hosts.get_hosts()

def show_bot(id):
	bot_network.show_bot(id)

def show_bots():
	bot_network.show_bots()

def show_shells():
	bot_network.show_shells()

def show_host(id):
	hosts.show_host(id)

def show_hosts():
	hosts.print_hosts()

def show_full_mode_bot_record(id):
	bot_network.show_full_mode_bot_record(id)

def update_all_bot():
	bots = get_bots()
	database.update_all_bots(bots)

def update_all_host():
	hosts = get_hosts()
	database.update_all_hosts(hosts)

def update_hosts_and_bots():
	bots = get_bots()
	hosts = get_hosts()
	database.update_all_hosts_and_bots(bots, hosts)

def bot_permanent_assignment(bot_id, host_id):
	bot_network.bot_permanent_assignment(bot_id, host_id)

def bot_command(id, action, host):
	bot_network.bot_command(id, action, host)

def net_1():
	hosts.specs()


	# simple attacks, permanent assignment, scan network