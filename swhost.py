import pygame
import cv2
import socket
import os
import sys
import ctypes
import ctypes.wintypes

try:
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
except Exception:
    print("pycaw not available, volume forcing disabled")

try:
	import pyautogui
except:
	print("Failed to import autogui")

HWND_TOPMOST = -1
SWP_NOMOVE   = 0x0002
SWP_NOSIZE   = 0x0001
SW_SHOW      = 5

def get_data_file_path(filename):
	if getattr(sys, 'frozen', False):
		# If the application is running in frozen mode (e.g., as an executable)
		base_path = sys._MEIPASS
	else:
		# If the application is running in a normal Python environment
		base_path = os.path.dirname(__file__)
	
	return os.path.join(base_path, filename)

try:
	import winreg as reg

	def add_to_startup():
		# Get the path to the current executable
		exe_path = os.path.abspath(sys.argv[0])
		print(exe_path)
		
		key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
		value_name = "GANDALF"
		try:
			with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE) as registry_key:
				reg.SetValueEx(registry_key, value_name, 0, reg.REG_SZ, exe_path)
		except Exception as e:
			print(f"Failed to add to startup: {e}")
except:
	print("registry load failed")


def force_foreground_windows(hwnd):
	user32 = ctypes.windll.user32

	# Layer 1: HWND_TOPMOST — bypasses foreground lock entirely (Win10 + Win11)
	try:
		user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
	except Exception as e:
		print(f"SetWindowPos failed: {e}")

	# Layer 2: AttachThreadInput trick — grants keyboard focus
	try:
		fg_hwnd   = user32.GetForegroundWindow()
		fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
		own_thread = ctypes.windll.kernel32.GetCurrentThreadId()

		if fg_thread and fg_thread != own_thread:
			user32.AttachThreadInput(fg_thread, own_thread, True)

		user32.SetForegroundWindow(hwnd)
		user32.BringWindowToTop(hwnd)
		user32.ShowWindow(hwnd, SW_SHOW)

		if fg_thread and fg_thread != own_thread:
			user32.AttachThreadInput(fg_thread, own_thread, False)

	except Exception as e:
		print(f"AttachThreadInput focus trick failed: {e}")
		# Layer 3: pyautogui fallback (only if ctypes fails entirely)
		try:
			pyautogui.click()
		except Exception:
			print("Failed to focus with a gui hack")


def set_max_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        volume_interface = devices.EndpointVolume
        volume_interface.SetMute(0, None)
        volume_interface.SetMasterVolumeLevelScalar(1.0, None)
    except Exception as e:
        print(f"set_max_volume failed: {e}")


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
	try:
		add_to_startup()
	except:
		print("add to startup failed")
	server_socket = create_and_bind_gandalf_socket()
	while(True):

		block_pending_udp_message(server_socket)
		
		# Initialize Pygame
		pygame.init()

		# Replace 'your_video.mp4' with the path to your video file
		video_path = "GANDALFS.mp4"

		# Load video using OpenCV
		cap = cv2.VideoCapture(get_data_file_path(video_path))

		# Get video dimensions
		width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
		height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

		# Set up Pygame window
		screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('Video Player')
		
		# Load and play audio
		pygame.mixer.init()
		mp3_path = get_data_file_path("audio.mp3")
		pygame.mixer.music.load(mp3_path)  # Use the extracted audio file
		set_max_volume()
		pygame.mixer.music.play(-1)  # Loop audio

		pygame.event.set_grab(True)
		hwnd = pygame.display.get_wm_info()['window']
		force_foreground_windows(hwnd)

		exit_flag = 0
		while True:
			loop_begin_ms = pygame.time.get_ticks()

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
				while(pygame.time.get_ticks() - loop_begin_ms < 33):
					pass
		
		# Clean up
		cap.release()
		pygame.quit()
