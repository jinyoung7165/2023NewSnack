import requests

print("run~~~~~~~~~~~~~~~~~~")
try:
    print(requests.get("http://newsnack-spring.Newsnack:8080"))
except Exception as e:
    print("hey", e)