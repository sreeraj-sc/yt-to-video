import os
import pytube
from moviepy.editor import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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

# Email the converted file
fromaddr = "your_email_address@gmail.com"
toaddr = "recipient_email_address@gmail.com"

# Create a multipart message object and set headers
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Converted Video"

# Attach the converted file
attachment = open(output_path, "rb")
p = MIMEBase('application', 'octet-stream')
p.set_payload((attachment).read())
encoders.encode_base64(p)
p.add_header('Content-Disposition', "attachment; filename= %s" % output_file_name)
msg.attach(p)

# Login to Gmail and send email
smtp_username = "your_email_address@gmail.com"
smtp_password = "your_app_password"
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(smtp_username, smtp_password)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()

print("Email sent!")
