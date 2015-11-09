from Tkinter import *
from botnet import msfrpca
from threading import Semaphore
import pymongo

#DB_CLIENT = pymongo.MongoClient()
root = Tk()
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight() * 0.8
screenLock = Semaphore(value=1)

token = ''
PROGRAM_NAME = "BOT ARMY"
PROGRAM_AUTHOR = "Abraham Adberstein"

try:
	token = msfrpca.login('msf','123')
	print "[+] Connected to metasploit."
except:
	pass
	print "[-] Start msfconsole"
	print "[-] load msgrpc Pass=123"
	sys.exit()

try:
	DB_CLIENT = pymongo.MongoClient('localhost', 27017)
	print "[+] Connected to Database."
except:
	pass
	print "[-] Start Mongo Database"
	sys.exit()


#------------Commands and Exploits----------