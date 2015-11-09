import g_module
import center_frame 
import leftBottom_frame 
import database
import events

def main():
	print "[+] "+g_module.PROGRAM_NAME+" Initiated."
	center_frame.main()
	leftBottom_frame.main()
	database.load_database()
	#events.main()
	g_module.root.mainloop()

if __name__ == '__main__':
	main()






