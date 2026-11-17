import socket
#This imports the socket which talks to the other layers


def check_port(target, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#We are using TCP for this since it isn't a datastream which would be used for UDP

	sock.settimeout(1)
	#Making sure we don't linger on one port for too long

	result = sock.connect_ex((target, port))
	#Tries the TCP handshake it returns 0 on success

	sock.close()

	return result == 0
	#This returns either True or False depending on if the TCP was established. If It is it will return a 0 via the sock.connect, which will then make the return a boolean either True or False
target = "127.0.0.1"


#Loop through all the ports and checks if each one is open

for i in range (1, 1025):
	if check_port(target, i):
		print(f"Port {i} is open")

