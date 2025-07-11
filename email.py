import os
import smtplib
from email.mime.text import MIMEText
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Mailjet SMTP credentials
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
MAILJET_SENDER_EMAIL = os.getenv("MAILJET_SENDER_EMAIL")

# Streamlit UI
st.set_page_config(page_title="📧 Send Email", layout="centered")
st.title("📤 Send Email via Mailjet SMTP")

with st.form("email_form"):
    to_email = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    message = st.text_area("Message")
    send = st.form_submit_button("Send Email")

if send:
    if not (to_email and subject and message):
        st.warning("Please fill in all the fields.")
    elif not (MAILJET_API_KEY and MAILJET_SECRET_KEY and MAILJET_SENDER_EMAIL):
        st.error("❌ Missing Mailjet credentials. Check your .env file.")
    else:
        try:
            # Create MIMEText message
            msg = MIMEText(message, 'plain')
            msg['Subject'] = subject
            msg['From'] = MAILJET_SENDER_EMAIL
            msg['To'] = to_email

            # Setup SMTP connection
            server = smtplib.SMTP("in-v3.mailjet.com", 587)
            server.starttls()
            server.login(MAILJET_API_KEY, MAILJET_SECRET_KEY)
            server.sendmail(MAILJET_SENDER_EMAIL, to_email, msg.as_string())
            server.quit()

            st.success(f"✅ Email sent successfully to {to_email}")
        except Exception as e:
            st.error(f"❌ Failed to send email: {str(e)}")
