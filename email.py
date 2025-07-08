import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Mailjet credentials from .env
smtp_user = os.getenv("MAILJET_API_KEY")
smtp_pass = os.getenv("MAILJET_SECRET_KEY")
sender_email = os.getenv("MAILJET_SENDER_EMAIL")

# Email content
receiver_email = input("Enter recipient email: ")
subject = input("Enter subject: ")
body = input("Enter message: ")

# Set up email
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

# Send via Mailjet SMTP
try:
    server = smtplib.SMTP("in-v3.mailjet.com", 587)
    server.starttls()
    server.login(smtp_user, smtp_pass)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("✅ Email sent successfully via Mailjet!")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
