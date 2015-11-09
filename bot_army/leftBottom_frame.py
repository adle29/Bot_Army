from Tkinter import *
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel

import g_module
from threading import Thread
from multiprocessing import Process
from os import system
import pyttsx
import time
from text_module import *
from time import sleep

engine = pyttsx.init()
engine.setProperty('rate', 110)
voices = engine.getProperty('voices')
user = "Abraham"

#------global variables-------
root = g_module.root
window_width = g_module.window_width
window_height = g_module.window_height

#------gui variables-------
mainWidth = window_width * 0.4
mainHeight = window_height 

bottomWindow = Toplevel(root, width=mainWidth, height=mainHeight)
scrollBar = Scrollbar(bottomWindow)

textBox = CustomText(bottomWindow, bg="black", fg="white")

def main():
	bottomWindow.title("History")
	bottomWindow.geometry('%dx%d+%d+%d' % (mainWidth,mainHeight,0, 0))
	
	textBox.place(x=0, y=0, width=window_width, height=mainHeight)

	scrollBar.pack(side=RIGHT, fill=Y)
	scrollBar.config(command=textBox.yview)
	textBox.config(yscrollcommand=scrollBar.set)
	textBox.tag_configure("red", foreground="#ff0000")
	textBox.tag_configure("green", foreground="#00ff00")
	textBox.tag_configure("blue", foreground="#00c5ff")
	textBox.tag_configure("b-back", background="blue")
	textBox.tag_configure("yellow", foreground="#fff400")

def color():
	textBox.highlight_pattern("Command", "b-back")
	textBox.highlight_pattern("[+]", "green")
	textBox.highlight_pattern("[-]", "red")
	textBox.highlight_pattern("[!]", "red")
	textBox.highlight_pattern("[*]", "blue")
	textBox.highlight_pattern("(", "yellow")
	textBox.highlight_pattern(")", "yellow")

def printTextHistory(text):
	# from global_variables import LOCK_LEFT_TERMINAL

	# while LOCK_LEFT_TERMINAL == True:
	# 	sleep(0.1)

	# LOCK_LEFT_TERMINAL = True
	# ADD THREADING 
	textBox.insert(END, text + "\n")
	textBox.yview(END)
	color()

	LOCK_LEFT_TERMINAL = False

def speak(text):
	txt = 'echo "'+text+'" | festival --tts'
	system(txt)
	# def s():
	# 	engine.say(user + text)
	# 	engine.runAndWait()

	# t = Process(target=s(), args=())
	# t.start()

def print_bottom_panel(text):

	def run():
		time.sleep(1)
		textBox.insert(END, text + "\n")
		textBox.yview(END)
		color()


	t = Thread(target=run(), args=())
	t.start()

