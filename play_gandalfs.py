from moviepy.editor import VideoFileClip

def play_video(video_path):
    # Load the video file
    video = VideoFileClip(video_path)

    # Preview the video with audio
    video.preview()

if __name__ == "__main__":
    # Replace 'your_video.mp4' with the path to your video file
    video_path = 'GANDALFS.mp4'
    play_video(video_path)