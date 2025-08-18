
from moviepy import VideoFileClip, TextClip, CompositeVideoClip


# Load the video file (replace 'sample.mp4' with your video file)
video = VideoFileClip("../youtube/sample.mp4").subclip(0, 5)  # Trim to 5 seconds

# Create a text overlay
txt = TextClip("Hello, MoviePy!", fontsize=50, color='white')
txt = txt.set_position(('center', 'bottom')).set_duration(5)

# Overlay text on video
final_video = CompositeVideoClip([video, txt])

# Save the output (convert to mp4)
final_video.write_videofile("output.mp4", codec="libx264", fps=24)

print("Video editing complete! Check output.mp4")

