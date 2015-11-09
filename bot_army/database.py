import leftBottom_frame
from g_module import DB_CLIENT
import modules
import global_variables

printB = leftBottom_frame.printTextHistory
DB = DB_CLIENT['mikasa_database']
collection_hosts = DB['hosts']
collection_bots = DB['bots']

def load_configurations():
	modules.load_bot_config()

def load_database():
	printB("[+] Hosts and Bots loaded")
	global_variables.BOT_COUNT = collection_bots.count()

	for host in collection_hosts.find():
		modules.add_existant_host(host)

	for bot in collection_bots.find():
		modules.add_existant_bot(bot)

	modules.show_bots()
	modules.print_hosts()

def save_bot(bot):
	bot_JSON = {"stype":"bot", 
				"status":"SLEEPING",
				"full_mode_record": [],
				"targetHost": {},
				"record": [],
				"bot_id":bot.id}
	collection_bots.insert_one(bot_JSON).inserted_id

def save_host(host):
	host_JSON = { "address" : host.address,
	        "id": host.id,
	        "hostname": host.hostname,
	        "os_type" : '',
	        "os_vendor" : '',
	        "os_family" : '',
	        "os_gen" : '',
	        "os_accuracy" : '',
	        "openPorts" : [],
	        "controlled" : False,
	        "bot_assigned" : -1,
	        "scanned" : False,
	        "hashes" : '',
	        "hardened" : False }

	collection_hosts.insert_one(host_JSON).inserted_id

def erase_bots_data():
	collection_bots.drop()

def erase_hosts_data():
	collection_hosts.drop()

def erase_all_data():
	collection_bots.drop()
	collection_hosts.drop()
	printB("[+] System restarted")

def update_all_bots(bots):
	for key in bots:
		update_bot(bots[key])

	printB("[+] Bot Army saved.")

def update_all_hosts(hosts):
	for key in hosts:
		update_host(hosts[key])

	printB("[+] Hosts saved.")

def update_all_hosts_and_bots(bots, hosts):
	update_all_bots(bots)
	update_all_hosts(hosts)	

def update_bot(bot):
	collection_bots.update(
    	{ 'bot_id': bot.id }, 	
		{ '$set': {
			'status': bot.status,
			'full_mode_record': bot.full_mode_record,
			'record': bot.record,
			'targetHost': bot.targetHost }
		}
	)

def update_property_host(host_property, host_id, value):
	collection_hosts.update(
    	{ 'id': host_id }, 	
		{ '$set': {
			host_property: value }
		}
	)

def update_host(host):
	collection_hosts.update(
    	{ 'id': host.id }, 	
		{ '$set': {
			"hostname": host.hostname,
			'os_type': host.os_type,
			"os_type" : host.os_type,
	        "os_vendor" : host.os_vendor,
	        "os_family" : host.os_family,
	        "os_gen" : host.os_gen,
	        "os_accuracy" : host.os_accuracy,
	        "openPorts" : host.openPorts,
	        "controlled" : host.controlled,
	        "bot_assigned" : host.bot_assigned,
	        "scanned" : host.scanned,
	        "hashes" : host.hashes,
	        "hardened" : host.hardened }
		}
	)