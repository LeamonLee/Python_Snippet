import requests

res = requests.get("https://xkcd.com/353/")
print(res)

# If you ever want to see all of the properties and methods available to you from a specific object.
# print(dir(res))
# print(help(res))

print(res.text)
print(res.status_code)
print(res.ok)
print(res.headers)

# ======================

res2 = requests.get("https://imgs.xkcd.com/comics/python.png")
# print(res2.content)
with open("comic.png", 'wb') as f:
    f.write(res2.content)

# ======================

payload = {"page": 2, "count": 25}
# https://httpbin.org/get?page=2&count=25
res3 = requests.get("https://httpbin.org/get", params=payload)
print(res3.url)
print(res3.text)

# ======================

payload2 = {"username": "Leamon", "password": "Testing"}

res4 = requests.post("https://httpbin.org/post", data=payload2)
print(res4.text)
print(res4.json())  # .json() method returns a python dictionary, so we can store it into a variable and use it like python dictionary.
r_dict = res4.json()
print(r_dict["form"])

# ======================

res5 = requests.get("https://httpbin.org/basic-auth/leamon/testing", auth=("leamon", "testing"))

print(res5)
print(res5.text)

# ======================

res6 = requests.get("https://httpbin.org/delay/6", timeout=3)

print(res6)