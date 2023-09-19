from pytube import YouTube

# Take the YouTube video URL as input
video_url = "https://www.youtube.com/shorts/FMKDFp13Mx8"

# Create a YouTube object
yt = YouTube(video_url)

# Get the highest resolution stream
video_stream = yt.streams.get_highest_resolution()

# Download the video
video_path = "./video.mp4"  # Saves in the current directory
print(f"Downloading {yt.title}...")
video_stream.download(output_path=video_path)
print("Download complete!")
