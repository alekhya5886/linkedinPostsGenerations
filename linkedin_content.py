import os
from groq import Groq
import smtplib
from email.mime.text import MIMEText

# -------------------------------
# 1. Groq Client
# -------------------------------
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# -------------------------------
# 2. Memory (avoid repeat topics)
# -------------------------------
MEMORY_FILE = "memory.txt"
used_topics = set()

if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        used_topics = set(line.strip() for line in f if line.strip())

# -------------------------------
# 3. Prompt
# -------------------------------
prompt = f"""
You are a professional tech content writer and social media strategist. 

Write a 150–200 word engaging LinkedIn post about a trending tech topic. The content can be related to software, hardware, or interesting “Did you know?” tech facts. Make sure the post is:

1. Friendly, professional, and easy to read.
2. Starts with a hook that grabs attention.
3. Includes informative details or examples.
4. Ends with a subtle call-to-action (like inviting comments or shares).

After the post, provide 3 related image ideas that can be used to visualize the content. Format the image suggestions as short, descriptive phrases suitable for AI image generation (e.g., “A futuristic AI-powered robot in an office”).

Output format:

Post: [Your 150–200 word content here]

Image Ideas:
1. …
2. …
3. …


Avoid repeating these topics:
{list(used_topics)}

Requirements:
- Around 150 words
- Catchy emojis 🚀🤖📊
- Emerging technology topic
- Include 2 royalty-free image links (Unsplash / Pexels)
- Start with a clear topic/title line
"""

# -------------------------------
# 4. Generate content
# -------------------------------
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",  # updated model
    messages=[{"role": "user", "content": "Write a LinkedIn post about AI"}]
)


content = response.choices[0].message.content.strip()

# -------------------------------
# 5. Save topic to memory
# -------------------------------
topic = content.split("\n")[0]
with open(MEMORY_FILE, "a") as f:
    f.write(topic + "\n")

# -------------------------------
# 6. Send Email
# -------------------------------
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

print("✅ LinkedIn content generated & emailed successfully")
