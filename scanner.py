import argparse
import socket
from concurrent.futures import ThreadPoolExecutor



def check_port(target, port):
	"""Return True if a TCP connection to a target succeeds."""
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	result = sock.connect_ex((target, port)) #Returns 0 on success
	sock.close()
	return result == 0


def grab_banner(target,port):
	"""Return the first line a service sends, or "" if it sends nothing."""
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.settimeout(2)
			sock.connect((target, port))
			try:
				data = sock.recv(1024) #waits for the server to speak first (Servers like SSH, FTP, and etc.  answer here)
			except socket.timeout:
				sock.send(b"HEAD / HTTP/1.0\r\n\r\n") #Sends a minimal HTTP request and only asks for the response headers (b means bytes)
				data = sock.recv(1024)
			text = data.decode(errors="ignore").strip()
			return text.splitlines()[0] if text else ""
	except OSError: #Caches network problems
		return ""






def scan(target, port):
	if check_port(target, port):
		return (port, grab_banner(target,port))
	return None


def parse_ports(text):
	"""Turn a string like 20-25 into (20, 25).


	Raised a ValueError if the text is malformed or out of range
	"""

	start, end = text.split("-")
	start, end = int(start), int(end)
	"""This helps fix our ABC,DEF problem"""
	if not 1 <= start <= end <= 65535: #This makes it to where start has to be at least 1 and start is at most end. And end is at most 65535
		raise ValueError("port range out of bounds")
	return start, end

def main():
	parser = argparse.ArgumentParser(description="Simple TCP port scanner")
	parser.add_argument("-t", "--target", required=True, help="IP address or hostname")
	parser.add_argument("-p", "--ports", default="1-1024", help="port range, e.g. 1-1024")
	args = parser.parse_args()

	try:
		start, end = parse_ports(args.ports)
	except ValueError:
		parser.error("ports must look like: 1-1024 (start before end)") #prints the usage line plus the message and exits cleanly so users never see a trace back

	ports = range(start, end + 1)
	with ThreadPoolExecutor(max_workers=100) as executor:
		results = executor.map(lambda p: scan(args.target, p), ports)


	for result in results:
		if result is not None:
			port, banner = result
			print(f"Port {port} is open {banner}")


if __name__ == "__main__":
	main()


