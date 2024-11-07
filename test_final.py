import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"name": "john", "age": 13},
    {"name": "alex", "age": 14},
    {"name": "timo", "age": 16}
]

user4 = {"name": "user4", "age": 101}

# create 3 users using the list data, so ids 0, 1, 2

for i in range(len(data)):
    response = requests.put(BASE + "users/" + str(i), data[i])
    print(response.json())

input()
# create one more user 3
response = requests.put(BASE + "users/3", user4)
print(response.json())

input()
# delete first three users
for i in range(len(data)):
    response = requests.delete(BASE + "users/" + str(i))
    print(response)

input()
# get the userid 3 which should be ok
response = requests.get(BASE + "users/3")
print(response.json())

input()
# get the userid 1 which does not exist
response = requests.get(BASE + "users/1")
print(response.json())
#

# response = requests.put(BASE + "users/1", {"name": "john", "age": "13"})
# print(response.json())
#
# input()

# response = requests.get(BASE + "users/1")
# print(response.json())



# response = requests.get(BASE + "hello/petr/234")
# print(response.json())

# input()
# response = requests.post(BASE + "hello/petr/234")
# print(response.json())