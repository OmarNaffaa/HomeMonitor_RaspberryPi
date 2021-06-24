import time
import Adafruit_DHT
import requests

# Declare Constants
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
MIN_TO_SEC = 60
uploadUrl = 'https://api.thingspeak.com/update?api_key=I4BV5Q70NNDWH0SP'

# Poll sensor and upload data once every 30 minutes
while True:
	tempC = None
	humidity, tempC = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

	# Poll until valid temperature is received
	while (tempC is None):
		humidity, tempC = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

		if (tempC is not None):
			tempF = (tempC * 1.8) + 32

	# Upload temperature to ThingSpeak
	payload = {'field1': tempF}
	r = requests.get(uploadUrl, payload);
	
	while (not r.ok):
		r = requests.get(uploadUrl, payload)

	print ('Uploaded at: ' + time.ctime())
	time.sleep(30 * MIN_TO_SEC)
