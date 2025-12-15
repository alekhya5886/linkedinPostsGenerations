import os
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText

# 1. Configure Gemini (IMPORTANT)
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# 2. Load memory
memory_file = "memory.txt"
used_topics = set()

if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        used_topics = set(f.read().splitlines())

# 3. Prompt
prompt = f"""
Generate a NEW LinkedIn tech post topic not in this list:
{list(used_topics)}

Requirements:
- 150 words
- Catchy emojis
- Include 2 image links
- Emerging technology topic
"""

# 4. Model (THIS IS THE KEY FIX)
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)

content = response.text

# 5. Save topic to memory
first_line = content.split("\n")[0]
with open(memory_file, "a") as f:
    f.write(first_line + "\n")

# 6. Send email
msg = MIMEText(content)
msg["Subject"] = "LinkedIn Post Content"
msg["From"] = os.environ["SENDER_EMAIL"]
msg["To"] = os.environ["RECEIVER_EMAIL"]

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(
        os.environ["SENDER_EMAIL"],
        os.environ["EMAIL_PASSWORD"]
    )
    server.send_message(msg)

print("✅ Email sent successfully!")
