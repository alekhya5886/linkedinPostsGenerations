import os
from google import genai
import smtplib
from email.mime.text import MIMEText

# -------------------------------------------------
# 1. Create Gemini Client (NEW SDK)
# -------------------------------------------------
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

# -------------------------------------------------
# 2. Memory to avoid repeating topics
# -------------------------------------------------
MEMORY_FILE = "memory.txt"
used_topics = set()

if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        used_topics = set(line.strip() for line in f if line.strip())

# -------------------------------------------------
# 3. Prompt
# -------------------------------------------------
prompt = f"""
Generate a UNIQUE and engaging LinkedIn post on technology.

Avoid repeating these topics:
{list(used_topics)}

Requirements:
- Exactly ~150 words
- Catchy emojis 🚀🤖📊
- Focus on emerging technologies
- Include 2 royalty-free image links (Unsplash / Pexels)
- Start with a clear topic/title line
"""

# -------------------------------------------------
# 4. Generate content using Gemini
# -------------------------------------------------
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

content = response.text.strip()

# -------------------------------------------------
# 5. Save topic to memory
# -------------------------------------------------
topic = content.split("\n")[0]
with open(MEMORY_FILE, "a") as f:
    f.write(topic + "\n")

# -------------------------------------------------
# 6. Send Email
# -------------------------------------------------
msg = MIMEText(content)
msg["Subject"] = "📢 LinkedIn Tech Post Content"
msg["From"] = os.environ["SENDER_EMAIL"]
msg["To"] = os.environ["RECEIVER_EMAIL"]

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(
        os.environ["SENDER_EMAIL"],
        os.environ["EMAIL_PASSWORD"]
    )
    server.send_message(msg)

print("✅ LinkedIn content generated and emailed successfully")
