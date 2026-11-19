import socket
import argparse 
from concurrent.futures import ThreadPoolExecutor


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


def grab_banner(target,port):
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.settimeout(2) #Did 2 seconds instead of 1 to give slow services more time
			sock.connect((target, port)) #uses connect rather than connect_ex since we already know the port is open
			try:
				data = sock.recv(1024) #waits for the server to speak first (Servers like SSH answer here)
			except socket.timeout: #This runs if nothing arrived in 2 second
				sock.send(b"HEAD / HTTP/1.0\r\n\r\n") #Sends a minimal HTTP request and only asks for the response headers (b means bytes)
				data = sock.recv(1024) #The servers reply, since we are waiting, gets saved into data if they reply
			text = data.decode(errors="ignore").strip() #turns the recieved bytes into a string, errors=ignore skips any bytes that aren't valid text .strip removes whitespace and newlines
			return text.splitlines()[0] if text else "" #Keeps only the first line since banners can't be long, if text check protects me from a index error on a empty list
	except OSError: #Caches network problems including a second tiemout on a server that stays silent even after we send a http request
		return""



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

def scan(port):
	if check_port(args.target, port):
		banner = grab_banner(args.target, port)
		return (port, banner)
	return None
#It returns the port number if the port is open, and it retuns the port number if it isn't too
#The return None is optional since Python automatically returns none if it ends without a return so I added it to make the intentions clear


ports = range(start, end + 1)
#Self explanatory

with ThreadPoolExecutor(max_workers=100) as executor:
	results = executor.map(scan, ports)
#I had to do a lot of research for this 
#This creates a pool of up to 100 worker threads. 
#The "as executor" gives the pool of workers a name so we can use it
#the with statement is a context manager, it sets something up, runs the indented block then cleans up automatically
#For a thread pool the cleanup is that the block waits until every worker is finished running then it shuts down the pool
#This is convenient since we don't have to worry abbout closing anything
#map means "apply this function to every item"
#It takes scan and the list of ports and hands each port to a free worker and collects the answers. 
#The results come back in the same order as ports even though the work can finish in a random order. 
#It doesn't return a plain list, it returns a iterator which is something you loop over to get the values one by one
#By the way, instead of doing scan(ports) the executor will take the ports and feed it into scan. 

#So to make this easy to understand, to begin with, 100 workers will act immediately so ports 1 to 100 will be taken up immediately, some of those ports are closed, so the workers will immediately move on


for result in results:
	if result is not None:
		port, banner = result
		print(f"Port {port} is open {banner}")
#APPARENTLY LINUX DEFAULTS TO ABOUT 1,024 CONNECTIONS BY DEFAULT SO USING MORE THAN 500 WORKERS WILL CAUSE IT TO CRASH
#I am using time to test this on the terminal to have it print out how long it took, I will have it scan every possible port which if I did that on the old port scanner it would cause it to crash. 


