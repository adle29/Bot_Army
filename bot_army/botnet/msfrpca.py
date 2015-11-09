import time
import msgpack
import httplib
import sys
import g_module

headers = {"Content-type" : "binary/message-pack" }

class MConsole:
	def __init__(self):
		self.id = ""
		self.token = g_module.token
		self.client = httplib.HTTPConnection('localhost',55552)

	def request(self, args):
		params = msgpack.packb(args)
		self.client.request("POST", "/api/", params, headers)
		response = self.client.getresponse()
		return response

	def console_create(self):
		response = self.request(['console.create',self.token])
		if response.status == 200:
			resdata=msgpack.unpackb(response.read())
			self.id = resdata['id']
		else:
			print("Console.create failed")
			sys.exit()
		self.console_read(False)

	def console_write(self, command):
		response = self.request(['console.write',self.token,self.id,command])
		if response.status!=200:
			print("Console.write failed")
			sys.exit()
		time.sleep(2)

	def console_reads(self):
		response = self.request(['console.read',self.token,self.id])
		if response.status == 200:
			resdata=msgpack.unpackb(response.read())
			print resdata['data']
		else:
			print("Console.read failed")
			sys.exit()	

	def console_read(self, prints=True):	
		while True:
			response = self.request(['console.read',self.token,self.id])
			if response.status == 200:
				resdata=msgpack.unpackb(response.read())
				if resdata['busy']==True and len(resdata['data'])==0:
					print('waiting..')
					time.sleep(2)
				else:
					if prints:
						return resdata['data']
					break
			else:
				print("Console.read failed")
				sys.exit()	


	def console_destroy(self):
		token = self.token
		consoleid = self.id

		params=msgpack.packb(['console.destroy',token,consoleid])
		self.client.request("POST","/api/",params, headers)
		response = self.client.getresponse()
		resdata=msgpack.unpackb(response.read())
		if resdata['result'] == 'success':
			print("Console closed")

	def get_consoles(self):
		response = self.request(['console.list',self.token])
		if response.status == 200:
			resdata=msgpack.unpackb(response.read())
			print(resdata) 
		else:
			print("Console.create failed")
			sys.exit()

	def get_sessions(self):
		response = self.request(['session.list',self.token])
		if response.status == 200:
			resdata=msgpack.unpackb(response.read())
			return resdata
		else:
			print("Sessions returned failed")
			sys.exit()

	def session_write(self, id, command):
		response = self.request(['session.shell_write', self.token, id, command])
		if response.status != 200:
			print("Shell failed")
			sys.exit()
		time.sleep(2)

	def session_read(self, id):
		response = self.request(['session.shell_read', self.token, id])
		if response.status == 200:
			resdata=msgpack.unpackb(response.read())
			return resdata['data']
		else:
			print("Sessions read failed")
			sys.exit()

	def single_meterpreter_write(self, id, command):
		response = self.request(['session.meterpreter_run_single', self.token, id, command])
		if response.status != 200:
			print("Shell failed")
			sys.exit()
		time.sleep(2)

	def meterpreter_write(self, id, command):
		response = self.request(['session.meterpreter_write', self.token, id, command])
		if response.status != 200:
			print("Shell failed")
			sys.exit()
		time.sleep(2)

	def meterpreter_kill(self, id, command):
		response = self.request(['session.meterpreter_session_detach', self.token, id])
		if response.status != 200:
			print("Shell failed")
			sys.exit()
		time.sleep(2)


	def meterpreter_read(self, id):
		while True:
			response = self.request(['session.meterpreter_read', self.token, id])
			if response.status == 200:
				resdata=msgpack.unpackb(response.read())
				if resdata['busy']==True and len(resdata['data'])==0:
					print('waiting..')
					time.sleep(2)
				else:
					if prints:
						return resdata
					break
			else:
				print("Console.read failed")
				sys.exit()

def login(user, password):
	client =  httplib.HTTPConnection('localhost',55552)
	params = msgpack.packb(['auth.login', user, password])
	client.request("POST", "/api/", params, headers)
	response = client.getresponse()

	if response.status == 200:
	        data = response.read()
	else:
	        print("Connection Failed")
	        sys.exit()

	res = msgpack.unpackb(data)
	if res['result'] == 'success':
	        return res['token']
	else:
	        print("Auth failed")
	        sys.exit()


# newConsole = MConsole()

# newConsole.login(user, password)
# newConsole.createConsole()

# newConsole.console_write("version\n")
# newConsole.console_read()
# newConsole.console_destroy
# newConsole.get_sessions()