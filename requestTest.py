import requests

payload = {'field1': 100, 'field2': 50}
r = requests.get('https://api.thingspeak.com/update?api_key=I4BV5Q70NNDWH0SP', payload)

print(r.ok)
