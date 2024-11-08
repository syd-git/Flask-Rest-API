import requests


BASE = "http://127.0.0.1:5000/"
header = {"content-type": "application/json"}

user4 = {"name": "user4", "age": 101}

response = requests.post(BASE + "users", {"name": "user4", "age": 101}, headers=header)
print(response)



