import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

API_KEY = os.getenv("GOOGLE_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

prompt = """
Give me an engaging technology topic and a LinkedIn post in 150 words 
with catchy emojis and image links.
"""

response = model.generate_content(prompt)
content = response.text

msg = MIMEMultipart()
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL
msg["Subject"] = "Today's LinkedIn Content 🚀"

msg.attach(MIMEText(content, "plain"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER_EMAIL, EMAIL_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

print("Email sent successfully!")
