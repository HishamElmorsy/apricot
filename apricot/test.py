import requests

url = "https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15&pageSize=60"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.text)
