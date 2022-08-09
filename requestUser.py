import requests
import json
response_API = requests.get('https://randomuser.me/api/')

data = response_API.text
parse_json = json.loads(data)
data = parse_json['results'][0]
print(data.keys())