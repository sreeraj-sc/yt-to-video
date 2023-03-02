import os
import pytube
from moviepy.editor import *
import smtplib
from email.message import EmailMessage

# Ask user for the YouTube video URL
video_url = input("Enter the YouTube video URL: ")

# Download the YouTube video
yt = pytube.YouTube(video_url)
stream = yt.streams.filter(only_audio=True).first()
stream.download()

# Convert the downloaded video to MP3 format
video_file_name = stream.default_filename
mp3_file_name = os.path.splitext(video_file_name)[0] + ".mp3"
video_path = os.path.join(os.getcwd(), video_file_name)
mp3_path = os.path.join(os.getcwd(), mp3_file_name)
AudioFileClip(video_path).write_audiofile(mp3_path)
os.remove(video_path)

# Create a new video with black background and downloaded audio
audio = AudioFileClip(mp3_path)
duration = audio.duration
fps = 25
size = (640, 360)
black_bg = ColorClip(size, color=(0, 0, 0), duration=duration)
video = black_bg.set_audio(audio)
output_file_name = os.path.splitext(mp3_file_name)[0] + ".mp4"
output_path = os.path.join(os.getcwd(), output_file_name)
video.fps = fps
video.write_videofile(output_path, audio_codec="aac", threads=4)

# Clean up temporary files
os.remove(mp3_path)

print("Done! Video saved to", output_path)

# Send email with the video file as attachment
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'username'  # Replace with your Gmail address
smtp_password = 'password'  # Replace with the App Password generated earlier

msg = EmailMessage()
msg['From'] = smtp_username
msg['To'] = 'email'  # Replace with the recipient's email address
msg['Subject'] = 'Your converted video'
msg.set_content('Please find attached the converted video.')
with open(output_path, 'rb') as f:
    file_data = f.read()
msg.add_attachment(file_data, maintype='video', subtype='mp4', filename=output_file_name)

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.send_message(msg)

print('Email sent!')
