import socket
import argparse



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Chat Parser')
	parser.add_argument('--port', type=int, help="enter port", default=0)
	parser.add_argument("--ip", type=str, help="cmd line argument for ip to send messages to", default='')
	args = parser.parse_args()

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	client_socket.settimeout(0.0)
	
	if(args.ip == ''):
		ips = socket.gethostbyname_ex(socket.gethostname())[2]
		for address in ips:
			bkst_ip = address.split('.')
			bkst_ip[3] = '255'
			bkst_ip = '.'.join(bkst_ip)
			print("Using bkst ip: "+bkst_ip)
			target = (bkst_ip, 3576)
			pld = bytearray("YOU SHALL NOT PASS",encoding='utf8')
			try:
				client_socket.sendto(pld,target)
			except:
				print("sending failed")
	else:
		target = (args.ip, 3576)
		pld = bytearray("YOU SHALL NOT PASS",encoding='utf8')
		try:
			client_socket.sendto(pld,target)
		except:
			print("sending failed")

	client_socket.close()
