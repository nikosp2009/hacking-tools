import socks
import socket
import requests

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket

url = "http://example.onion"
response = requests.get(url)

print(response.content)
