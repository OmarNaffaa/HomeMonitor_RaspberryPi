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
	tempC = [-100, -100]
	humidity = [-100, -100]
	
	for i in range(3):
		humidity[i], tempC[i] = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

	# Poll until valid temperature is received across 2 samples
	while (tempC[0] == -100 or tempC[1] == -100):
		if (tempC[0] == -100):
			humidity[0], tempC[0] = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
		elif (tempC[1] == -100):
			humidity[1], tempC[1] = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
		elif (abs(tempC[1] - tempC[0]) > 5):
			tempC[0] = -100
			tempC[1] = -100
		else:
			tempC_avg = (tempC[0] + tempC[1]) / 2
			tempF = (tempC_avg * 1.8) + 32

	# Upload temperature to ThingSpeak
	payload = {'field2': tempF}
	r = requests.get(uploadUrl, payload);
	
	while (not r.ok):
		r = requests.get(uploadUrl, payload)

	print ('Uploaded at: ' + time.ctime())
	time.sleep(30 * MIN_TO_SEC)
