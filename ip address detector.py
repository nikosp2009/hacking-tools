import psutil

connections = psutil.net_connections(kind='inet')

for conn in connections:
    if conn.status == 'ESTABLISHED':
        print(f"IP address: {conn.laddr.ip} Reason: {conn.raddr}")
