import pygeoip
import leftTop_frame 
import leftBottom_frame

gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')
target = ""

def printRecord(target):
	leftTop_frame.printText("[*]Find IP Program Initiated.\n")
	try:
		rec = gi.record_by_name(target)
		city = rec['city']
		#region = rec['region_name']
		country = rec['country_name']
		longitude = rec['latitude']
		lat = rec['latitude']
		result = '[*]Target: ' + target + ' located at: \n'
		result += '[+]City: ' + str(city) + ', Country: ' + country + '\n'
		result += '[+]Longitude: ' + str(longitude) + ', Latitude: ' + str(lat)
		return result
	except:
		pass
	leftTop_frame.printText("[-]Error with arguments or connection. \n")


def specs():
	leftTop_frame.focus()

	leftTop_frame.number_args = 1
	spec = "[?]Find IP Address Program loaded"
	text = spec + "\n[*]Enter IP Address \n"
	leftBottom_frame.printTextHistory(spec + "\n")
	leftTop_frame.printText(text)
	leftTop_frame.loadedProgram = printRecord

#"172.5.97.204"
#curl ifconfig.me