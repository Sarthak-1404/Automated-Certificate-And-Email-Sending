import os
import time
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import smtplib
from email.message import EmailMessage

# ================= CONFIG =================
EMAIL = "londhesarthakkiran@gmail.com"
PASSWORD = "dpdohgmfpextqnan"   # Gmail App Password

TEMPLATE = "certificate.png"
FONT_PATH = "GreatVibes-Regular.ttf"   # use better font if possible
OUTPUT_DIR = "output"

EVENT_NAME = "Startup Mania"

# ==========================================

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load Excel
df = pd.read_excel("data.xlsx")

for index, row in df.iterrows():
    name = str(row['Name']).strip()
    receiver = row['Email']

    safe_name = name.replace(" ", "_")
    filename = f"{safe_name}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # ===== Generate Certificate =====
    img = Image.open(TEMPLATE)
    draw = ImageDraw.Draw(img)

    img_width, img_height = img.size

    # ===== AUTO FONT SIZE (for long names) =====
    font_size = 48
    while True:
        name_font = ImageFont.truetype(FONT_PATH, font_size)
        text_width = draw.textbbox((0, 0), name, font=name_font)[2]
        if text_width < img_width * 0.75:
            break
        font_size -= 2

    event_font = ImageFont.truetype(FONT_PATH, 38)

    # ===== NAME POSITION =====
    name_bbox = draw.textbbox((0, 0), name, font=name_font)
    name_width = name_bbox[2] - name_bbox[0]

    name_x = ((img_width - name_width) // 2) + 60
    name_y = int(img_height * 0.535) - 30   # tuned for your certificate

    draw.text((name_x, name_y), name, fill="#1a1a1a", font=name_font)

    # ===== EVENT POSITION =====
    event_bbox = draw.textbbox((0, 0), EVENT_NAME, font=event_font)
    event_width = event_bbox[2] - event_bbox[0]

    event_x = (img_width - event_width) // 2
    event_y = int(img_height * 0.615) - 70
    draw.text((event_x, event_y), EVENT_NAME, fill="#1a1a1a", font=event_font)

    # Save certificate
    img.save(filepath)

    # ===== Send Email =====
    msg = EmailMessage()
    msg['Subject'] = "Your Certificate - Tesseract 2K26"
    msg['From'] = EMAIL
    msg['To'] = receiver

    msg.set_content(f"""
Hello {name},

Congratulations on your participation in {EVENT_NAME}! 🎉

Please find your certificate attached.

Regards,
Team Tesseract
""")

    with open(filepath, 'rb') as f:
        msg.add_attachment(f.read(), maintype='image', subtype='png', filename=filename)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)

        print(f"✅ Sent to {name}")

    except Exception as e:
        print(f"❌ Failed for {name}: {e}")

    # Prevent Gmail blocking
    time.sleep(3)

print("🎉 All certificates generated and emails sent!")