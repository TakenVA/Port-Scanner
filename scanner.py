import socket
import argparse 

#The problem is the IP is encoded into the code itself, we need to user to type what machine they want to scan into the command line itself.
#argparse is a helper that reads the lines after the python file and splits it up into pieces



parser = argparse.ArgumentParser(description="Simple TCP port scanner")
#This creaters a parser object, which describes which inputs this program accepts. 
#description is the text that will show if someone runs <python3 scanner.py -h>, also it will show any help messages that it set.


parser.add_argument("-t", "--target", required=True, help="IP address or hostname")
#-t, and --target make it to where the user can have the flexibility of doing either  <-t 127.0.0.1> or <--target 127.0.0.1>
#this flag also  tells the parser that the next word is the target. Without this flag parser wont know that 127.0.0.1 is a port or something else

#required = True, this means that the program WILL NOT RUN without this. Obviously you need an IP address to send a TCP handshake.

parser.add_argument("-p", "--ports", default="1-1024", help="port range, e.g. 1-1024")
#since this isn't mandatory if the user doesn't set the -p value then the parser will default on the vaule from 1-1024
#NOTE I AM PRETTY SURE TYPING IN ABC-CDE WOULD CRASH THIS

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

args = parser.parse_args()
#reads what the user typed and puts it into args
#so target would be args.target, and ports would be args.ports

start, end = args.ports.split("-")
#since we have it defined as the port being <somenumber-somenumber> when it is actually ran though this line of code will seperate the two numbers via the split
#so "20-25" would end up becoming ["20", "25"]
#this is called unpacking, so 20 would become start and 25 would become end

start = int(start)
end = int(end)
#int turns the strings into integers

for port in range(start, end + 1):
	if check_port(args.target, port):
		print(f"Port {port} is open")
