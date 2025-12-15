import os
import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai

# ---------------- CONFIG ----------------
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

SENDER_EMAIL = os.environ["SENDER_EMAIL"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
RECEIVER_EMAIL = os.environ["RECEIVER_EMAIL"]

MEMORY_FILE = "memory.txt"

# ---------------- MEMORY ----------------
used_topics = ""
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        used_topics = f.read()

# ---------------- GEMINI (FIXED MODEL) ----------------
model = genai.GenerativeModel("models/gemini-pro")

prompt = f"""
Generate a UNIQUE LinkedIn post on a technology topic.

Rules:
- 150 words
- Catchy emojis
- Include 2–3 image links
- Start with a TITLE in the first line
- DO NOT repeat topics from below:

{used_topics}
"""

response = model.generate_content(prompt)
content = response.text

# ---------------- SAVE MEMORY ----------------
topic = content.split("\n")[0].strip()
with open(MEMORY_FILE, "a") as f:
    f.write(topic + "\n")

# ---------------- EMAIL ----------------
msg = MIMEText(content)
msg["Subject"] = "LinkedIn Content Idea 🚀"
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER_EMAIL, EMAIL_PASSWORD)
    server.send_message(msg)

print("✅ Email sent successfully")
