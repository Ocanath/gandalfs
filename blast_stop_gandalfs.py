import socket
import argparse
import time


if __name__ == "__main__":
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	client_socket.settimeout(0.0)

	subnets = [1, 2, 3, 4, 5, 6, 7, 8]
	port = 3576

	# target = (args.ip, 3576)
	for repeat in range(0,3):
		for subnet in subnets:
			for host in range(0, 256):
				target = (f"10.0.{subnet}.{host}", port)
				pld = bytearray("YOU SHALL NOT PASS",encoding='utf8')
				try:
					client_socket.sendto(pld,target)
				except:
					print("sending failed")
        time.sleep(1)
	client_socket.close()
