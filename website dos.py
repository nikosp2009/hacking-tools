import requests

url = 'https://example.com'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
count = 1000000000000000000000000000000000000000000000000000000000000000

for i in range(count):
    r = requests.get(url, headers=headers)
    print("Request", i+1, "sent. Response code:", r.status_code)
