import socket
import argparse



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Chat Parser')
	parser.add_argument('--port', type=int, help="enter port", default=0)
	parser.add_argument("--ip", type=str, help="cmd line argument for ip to send messages to", default='192.168.1.255')
	args = parser.parse_args()

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	client_socket.settimeout(0.0)
	
	target = (args.ip, 3576)

	pld = bytearray("THEY'RE TAKING THE HOBBITS TO ISENGARD",encoding='utf8')
	client_socket.sendto(pld,target)
	client_socket.close()