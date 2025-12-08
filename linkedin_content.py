# linkedin_content.py
import os
import smtplib
from email.mime.text import MIMEText
from google.generativeai import ChatModel

# --- 1. Load memory of used topics ---
memory_file = "memory.txt"
if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        used_topics = [line.strip() for line in f.readlines()]
else:
    used_topics = []

# --- 2. Generate content with Gemini ---
model = ChatModel(model="models/gemini-2.5-flash")

prompt = f"""
Give me a most interesting and engaging topic and content to post on LinkedIn on technology topics in 150 words.
Use catchy emojis and give related image links.
Do NOT repeat any of these topics: {', '.join(used_topics)}
"""

response = model.generate_message(
    messages=[{"content": prompt}]
)

content = response.candidates[0].content

# --- 3. Extract new topic/title (first line) ---
new_topic = content.split("\n")[0].strip()

# --- 4. Update memory ---
if new_topic not in used_topics:
    with open(memory_file, "a") as f:
        f.write(new_topic + "\n")

# --- 5. Send email ---
SENDER_EMAIL = os.environ["SENDER_EMAIL"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
RECEIVER_EMAIL = os.environ["RECEIVER_EMAIL"]

msg = MIMEText(content)
msg['Subject'] = "Today's Content for LinkedIn Post"
msg['From'] = SENDER_EMAIL
msg['To'] = RECEIVER_EMAIL

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(SENDER_EMAIL, EMAIL_PASSWORD)
    server.send_message(msg)

print("Email sent successfully!")
