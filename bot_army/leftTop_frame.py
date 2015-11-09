from Tkinter import *
from itertools import cycle
import g_module

#------global variables-------
# root = g_module.root
# window_width = g_module.window_width
# window_height = g_module.window_height

# #------custom variables-------
# mainWidth = window_width * 0.4
# mainHeight = window_height / 2.1

# #------gui variables-------
# leftWindow = Toplevel(root, width=mainWidth, height=mainHeight)
# textBox = Text(leftWindow, bg="black", fg="yellow")
# scrollBar = Scrollbar(leftWindow)
# txt = StringVar()
# leftTopEntry = Entry(leftWindow, textvariable=txt)

# #------ modules/print variables-------
# loadedProgram = ""
# loadedProgram_args = []
# number_args = 0
# entered_args = 0

# def main():
# 	leftWindow.title("Launchpad")
# 	leftWindow.geometry('%dx%d+%d+%d' % (mainWidth,mainHeight,0,0))
# 	textBox.place(x=0, y=0, width=window_width, height=mainHeight*0.93)

# 	scrollBar.pack(side=RIGHT)
# 	scrollBar.config(command=textBox.yview)
# 	textBox.config(yscrollcommand=scrollBar.set)
# 	leftTopEntry.place(x=0, y=mainHeight*0.93, width=window_width)

# def printText(text):
# 	textBox.insert(END, text)

# def focus():
# 	leftTopEntry.focus_set()
# 	cleanProgramLine()

# def cleanProgramLine():
# 	global entered_args
# 	global number_args
# 	global loadedProgram_args
# 	global loadedProgram

# 	loadedProgram = ""
# 	loadedProgram_args = []
# 	entered_args = 0
# 	number_args = 0


# def runProgram(event):
# 	global entered_args
# 	global number_args
# 	global loadedProgram_args
# 	global loadedProgram

# 	s = txt.get()
# 	leftTopEntry.delete(0, END)
# 	printText("[*]Arg: " + s + "\n")

# 	if s == "exit":
# 		printText("[+]Programs unloaded.\n")
# 		cleanProgramLine()

# 	elif loadedProgram != "":
# 		if entered_args == number_args:
# 			loadedProgram(loadedProgram_args)
# 			cleanProgramLine()

# 		else:
# 			if s != None:
# 				entered_args += 1
# 				loadedProgram_args.append(s)
# 				if entered_args == number_args:
# 					loadedProgram(loadedProgram_args)
# 					cleanProgramLine()
# 	else:
# 		printText("[!]Command not found.\n")

# leftTopEntry.bind('<Return>', runProgram)

