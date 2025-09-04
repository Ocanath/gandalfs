import socket
import argparse



if __name__ == "__main__":
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	client_socket.settimeout(0.0)

	ips = [
		("10.0.1.255", 3576),
		("10.0.3.255", 3576),
		("10.0.4.255", 3576),
		("10.0.5.255", 3576),
		("10.0.6.255", 3576),
		("10.0.7.255", 3576),
		("10.0.8.255", 3576)
		]

	# target = (args.ip, 3576)
	for repeat in range(0,3):
		for target in ips:
			pld = bytearray("THEY'RE TAKING THE HOBBITS TO ISENGARD",encoding='utf8')
			try:
				client_socket.sendto(pld,target)
			except:
				print("sending failed")

	client_socket.close()
