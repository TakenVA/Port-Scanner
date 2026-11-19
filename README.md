# Port-Scanner
This is a lightweight, multithreaded TCP port scanner written inside an Ubuntu Linux Virtual Machine with Python. It uses CLI flags to define ports in a range, it then reports which are open, and grabs the service banner to display what exactly is running.

## Features
- **TCP connect scanning** using only the standard library
- **Command-line interface** (`-t` target, `-p` port range) built using argeparse
- **Multithreading** with `ThreadPoolExecutor` (using a pool of 100 workers)
- **Banner grabbing** for services that announce themselves (SSH) and for services that require a request (HTTP)
- **Input validation** used to maintain correct formating with clean error messages

## Usage 
```
python3 scanner.py -t 127.0.0.1 -p 1-1024
python3 scanner.py -t 192.168.1.5 -p 1-65535
python3 scanner.py -h
```
If `-p` is not defined, ports 1-1024 are scanned by default. 


## Sample output
```
Port 22 is open  SSH-2.0-OpenSSH_9.6p1 Ubuntu
Port 631 is open  HTTP/1.0 400 Bad Request
Port 8000 is open  HTTP/1.0 200 OK
```
## Engineering notes

**Concurrency** The original problem was that each port was being scanned sequentially, which wastes a lot of time. Using `ThreadPoolExecutor` with 100 workers lets many connection attemps occur at the same time.

**Order Results** `executor.map` returns results in the same order as the input ports. Despite the fact that the work could finish in a random order.

**Input Handling** Initally, I realized that without any input handling someone could input `abc,def`, which would cause the program to crash. Because of this I added it to where the input must follow a certain amount of rules. If for whatever reason the input doesn't follow these rules then there will be a rejection message with a clear usage message instead of a traceback.
 
## Legal and ethical use

**ONLY SCAN SYSTEMS YOU OWN OR HAVE EXPLICIT PERMISSION TO TEST**


## Source Code 
[See Code Here!](https://github.com/TakenVA/Port-Scanner/blob/main/scanner.py)
