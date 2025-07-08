import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get Mailjet credentials
smtp_user = os.getenv("MAILJET_API_KEY")
smtp_pass = os.getenv("MAILJET_SECRET_KEY")
sender_email = os.getenv("MAILJET_SENDER_EMAIL")

# Streamlit UI setup
st.set_page_config(page_title="📧 Send Email via Mailjet", layout="centered")

# Fancy minimal CSS
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #f6d365, #fda085);
            padding: 2rem;
            border-radius: 16px;
            max-width: 700px;
            margin: auto;
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            color: #6A0572;
            text-align: center;
            margin-bottom: 2rem;
        }
        .stTextInput input, .stTextArea textarea {
            border-radius: 10px !important;
        }
        button[kind="primary"] {
            background-color: #6A0572 !important;
            color: white !important;
            font-weight: bold;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>📧 Send Email with Mailjet</h1>", unsafe_allow_html=True)

# Form inputs
with st.form("email_form"):
    receiver_email = st.text_input("✉️ Recipient Email")
    subject = st.text_input("📝 Email Subject")
    body = st.text_area("💬 Email Message", height=150)
    submitted = st.form_submit_button("🚀 Send Email")

# Send email
if submitted:
    if not receiver_email or not subject or not body:
        st.warning("⚠️ Please fill in all fields.")
    elif not smtp_user or not smtp_pass or not sender_email:
        st.error("❌ Mailjet credentials missing. Please check your .env file.")
    else:
        try:
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP("in-v3.mailjet.com", 587)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()

            st.success(f"✅ Email successfully sent to {receiver_email}")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
