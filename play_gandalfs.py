import pygame
import cv2

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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cap.release()
            exit()

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
    pygame.time.delay(25)  # Delay for frame rate

# Clean up
cap.release()
pygame.quit()
