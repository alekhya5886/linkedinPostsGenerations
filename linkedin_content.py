import google.generativeai as genai
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash-latest")

prompt = """
Give me an engaging trending technology topic and a 150-word LinkedIn post 
with emojis and image links.
"""

response = model.generate_content(prompt)
content = response.text

sender = os.getenv("SENDER_EMAIL")
password = os.getenv("EMAIL_PASSWORD")
receiver = os.getenv("RECEIVER_EMAIL")

msg = MIMEMultipart()
msg["From"] = sender
msg["To"] = receiver
msg["Subject"] = "Today's LinkedIn Post ✨"

msg.attach(MIMEText(content, "plain"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())

print("Email sent successfully!")
