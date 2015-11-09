import g_module
import leftBottom_frame
from Tkinter import *
from modules import *
from threading import Thread
from text_module import *

#------global variables-------
root = g_module.root
window_width = g_module.window_width
window_height = g_module.window_height

#------gui variables-------
menubar = Menu(root)
mainFrame = Frame(root)
mainTextInput = StringVar()
mainEntryBox = Entry(root, textvariable=mainTextInput)
mainFrameBottom = Frame(root)
mainTextBox2 = CustomText(mainFrameBottom, bg="black", fg="yellow")

#------print variables-------
linesText = ["Bots:\n"]
linesText2 = ["Hosts:\n"]
commandsUsed = []
command_index = 0

mainTextBox = CustomText(mainFrame, bg="black", fg="green")

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()


def main():
	w = window_width * 0.59
	x = (window_width / 2) + (w/2)
	y = 0

	root.title("Data Central")
	root.geometry('%dx%d+%d+%d' % (w,window_height,x,y))

	addMenu()

	mainFrame.place(x=0,y=0, height=window_height*0.45, width=window_width)

	mainTextBox.pack(fill=X)
	mainTextBox.insert(END, "Bots:\n")

	mainEntryBox.place(x=0,y=window_height*0.45, width=window_width)
	
	mainFrameBottom.place(x=0,y=window_height*0.48, height=window_height/1.8, width=window_width)

	mainTextBox2.pack(fill=X)
	mainTextBox2.insert(END, "Hosts:\n")

	mainTextBox.tag_configure("red", foreground="#ff0000")
	mainTextBox.tag_configure("green", foreground="#00ff00")
	mainTextBox.tag_configure("blue", foreground="#00c5ff")
	mainTextBox.tag_configure("yellow", foreground="#fff400")
	mainTextBox.tag_configure("b-back", background="blue")

	mainTextBox2.tag_configure("red", foreground="#ff0000")
	mainTextBox2.tag_configure("green", foreground="#00ff00")
	mainTextBox2.tag_configure("blue", foreground="#00c5ff")
	mainTextBox2.tag_configure("yellow", foreground="#fff400")
	mainTextBox2.tag_configure("b-back", background="blue")

def addMenu():
	mainMenu = Menu(menubar, tearoff=0)
	mainMenu.add_command(label="About", command=donothing)
	mainMenu.add_command(label="Preferences", command=donothing)
	mainMenu.add_command(label="Save", command=update_hosts_and_bots)
	mainMenu.add_separator()
	mainMenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="Configuration", menu=mainMenu)

	intelMenu = Menu(menubar, tearoff=0)
	intelMenu.add_command(label="Nmap Scanner", command=intel_1)
	menubar.add_cascade(label="Intel", menu=intelMenu)

	attackMenu = Menu(menubar, tearoff=0)
	attackMenu.add_command(label="Add Host", command=net_1)
	attackMenu.add_command(label="Add Bot", command=add_bot)

	menubar.add_cascade(label="Attack", menu=attackMenu)

	defenseMenu = Menu(menubar, tearoff=0)
	defenseMenu.add_command(label="Secure Box", command=donothing)
	defenseMenu.add_command(label="Inject Malware", command=donothing)
	menubar.add_cascade(label="Defense", menu=defenseMenu)

	networkMenu = Menu(menubar, tearoff=0)
	networkMenu.add_command(label="DPKT", command=donothing)
	menubar.add_cascade(label="Network", menu=networkMenu)

	forensicsMenu = Menu(menubar, tearoff=0)
	forensicsMenu.add_command(label="Find IP Address Location", command=m1)
	menubar.add_cascade(label="Forensics", menu=forensicsMenu)

	root.config(menu=menubar)
	mainEntryBox.bind('<Return>', command)
	mainEntryBox.bind('<Up>', show_commands_u)
	mainEntryBox.bind('<Down>', show_commands_d)
	root.bind('<Escape>', exit)
	mainEntryBox.focus_set()	

#-----------------DATA CENTAL-----------------
def color():
	mainTextBox.highlight_pattern("Request", "b-back")
	mainTextBox.highlight_pattern("[+]", "yellow")
	mainTextBox.highlight_pattern("[-]", "red")
	mainTextBox.highlight_pattern("[!]", "red")
	mainTextBox.highlight_pattern("[*]", "blue")
	mainTextBox.highlight_pattern("[=]", "yellow")
	mainTextBox.highlight_pattern("|", "yellow")
	mainTextBox.highlight_pattern("-", "yellow")
	mainTextBox.highlight_pattern("=>", "yellow")
	mainTextBox.highlight_pattern("=", "yellow")
	mainTextBox.highlight_pattern("+", "yellow")
	# mainTextBox.highlight_pattern("\xe2", "yellow")

	mainTextBox2.highlight_pattern("Request", "b-back")
	mainTextBox2.highlight_pattern("[+]", "yellow")
	mainTextBox2.highlight_pattern("[-]", "red")
	mainTextBox2.highlight_pattern("[*]", "blue")
	mainTextBox2.highlight_pattern("[=]", "yellow")
	mainTextBox2.highlight_pattern("|", "yellow")
	mainTextBox2.highlight_pattern("-", "yellow")
	mainTextBox2.highlight_pattern(":", "yellow")
	mainTextBox2.highlight_pattern("=", "yellow")
	mainTextBox2.highlight_pattern("+", "yellow")
	# mainTextBox2.highlight_pattern("\xe2", "yellow")

def clear_main_tx_box():
	mainTextBox.delete("1.0", END)

def clear_main_bottom_tx_box():
	mainTextBox2.delete("1.0", END)

def exit(event):
	from global_variables import PROGRAM_QUIT
	PROGRAM_QUIT = True
	root.quit()

def main_tx_box_print(text):
	clear_main_tx_box()
	mainTextBox.insert(END, text)
	color()

def bottom_tx_box_print(text):
	clear_main_bottom_tx_box()
	mainTextBox2.insert(END, text)
	color()

def command(event):
	import cmd_module
	command_index = 0
	s = mainTextInput.get()
	commandsUsed.append(s)
	mainEntryBox.delete(0, END)
	leftBottom_frame.printTextHistory("[*] Command: " + s)

	p=Thread(target=cmd_module.cmd_assert, args=(s,))
	p.start()
	# cmd_module.cmd_assert(s)

def show_commands_u(event):
	global command_index

	mainEntryBox.delete(0, END)
	last = len(commandsUsed) - 1
	num = last-command_index
	cmd = ""

	if num >= 0:
		cmd = commandsUsed[num]
		command_index += 1
		mainEntryBox.insert(END, cmd)
	else:
		cmd = ""
		mainEntryBox.insert(END, cmd)
		command_index = 0

def show_commands_d(event):
	global command_index
	command_index -= 1

	mainEntryBox.delete(0, END)
	last = len(commandsUsed) - 1
	num = last-command_index
	cmd = ""

	if num >= 0 and num <= last:
		cmd = commandsUsed[num]
		mainEntryBox.insert(END, cmd)
	else:
		cmd = ""
		mainEntryBox.insert(END, cmd)
		command_index = 0



