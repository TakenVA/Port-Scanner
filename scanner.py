import socket
#This imports the socket which talks to the other layers

target = "127.0.0.1"
port = 22

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#We are using TCP for this since it isn't a datastream which would be used for UDP

sock.settimeout(1)
#Making sure we don't linger on one port for too long

result = sock.connect_ex((target, port))
#Tries the TCP handshake it returns 0 on success

if result == 0:
	print(f"Port {port} is open")
else:
	print(f"Port {port} is closed")

sock.close()
