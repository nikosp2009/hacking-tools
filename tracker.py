import requests

ip_address = input("Enter the IP address: ")

# Get information on the IP address using ipinfo.io
response = requests.get(f"https://ipinfo.io/{ip_address}/json")
ip_data = response.json()

# Print IP address information
print(ip_data)

# Get user information using WHOIS
response = requests.get(f"http://whois.arin.net/rest/ip/{ip_address}")
user_data = response.text

# Print user information
print(user_data)
