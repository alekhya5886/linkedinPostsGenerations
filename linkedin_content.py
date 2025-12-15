import os
import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai

# ---------------- CONFIG ----------------
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

SENDER_EMAIL = os.environ["SENDER_EMAIL"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
RECEIVER_EMAIL = os.environ["RECEIVER_EMAIL"]

MEMORY_FILE = "memory.txt"

# ---------------- MEMORY ----------------
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        used_topics = f.read()
else:
    used_topics = ""

# ---------------- GEMINI ----------------
model = genai.GenerativeModel("gemini-1.0-pro")

prompt = f"""
Generate a unique and engaging LinkedIn post on a technology topic.
- 150 words
- Catchy emojis
- Include image links
- DO NOT repeat topics from this list:
{used_topics}
Start with a clear title in the first line.
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
