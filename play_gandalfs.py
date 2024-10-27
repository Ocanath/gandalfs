import pygame
import cv2
import socket

def create_and_bind_gandalf_socket():
	udp_server_addr = ('0.0.0.0', 3576)
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	server_socket.settimeout(0.0) #make non blocking
	print("binding: "+udp_server_addr[0]+", "+str(udp_server_addr[1]))
	server_socket.bind(udp_server_addr)
	print("Bind successful")
	return server_socket

def block_pending_udp_message(socket):
	received = 0
	while received == 0:
		try:
			pkt,source_addr = socket.recvfrom(512)
			# print("From: "+source_addr[0]+":"+str(source_addr[1])+": "+str(pkt))
			if(pkt == bytearray("THEY'RE TAKING THE HOBBITS TO ISENGARD",encoding='utf8')):
				received = 1
			else:
				print("mismatch: " + str(pkt))
		except BlockingIOError:
			pass

def nonblocking_catch_stop_signal(socket):
	received = 0
	try:
		pkt,source_addr = socket.recvfrom(512)
		# print("From: "+source_addr[0]+":"+str(source_addr[1])+": "+str(pkt))
		if(pkt == bytearray("YOU SHALL NOT PASS",encoding='utf8')):
			received = 1
		else:
			print("mismatch: " + str(pkt))
	except BlockingIOError:
		pass
	return received

if __name__ == "__main__":
	server_socket = create_and_bind_gandalf_socket()
	while(True):

		block_pending_udp_message(server_socket)
		
		# Initialize Pygame
		pygame.init()

		# Replace 'your_video.mp4' with the path to your video file
		video_path = 'GANDALFS.mp4'

		# Load video using OpenCV
		cap = cv2.VideoCapture(video_path)

		# Get video dimensions
		width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
		height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

		# Set up Pygame window
		screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('Video Player')

		# Load and play audio
		pygame.mixer.init()
		pygame.mixer.music.load('audio.mp3')  # Use the extracted audio file
		pygame.mixer.music.play(-1)  # Loop audio

		exit_flag = 0
		while True:
			
			exit_flag = nonblocking_catch_stop_signal(server_socket)	#catch a stop message

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					print("...nah")
					pygame.quit()
					cap.release()
					exit_flag = 1
					break
					# exit()
			
			if(exit_flag != 0):
				break
			
			if(exit_flag == 0):
				ret, frame = cap.read()
				if not ret:
					cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video
					continue

				#why must we do this? we don't ask
				frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
				# Convert frame to RGB (Pygame uses RGB, OpenCV uses BGR)
				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				frame_surface = pygame.surfarray.make_surface(frame)

				# Display the frame
				screen.blit(frame_surface, (0, 0))
				pygame.display.flip()
				pygame.time.delay(33)  # Delay for frame rate
		
		# Clean up
		cap.release()
		pygame.quit()
