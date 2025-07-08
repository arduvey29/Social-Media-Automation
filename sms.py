import os
from dotenv import load_dotenv
from twilio.rest import Client
import streamlit as st

# Load .env
load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

# Streamlit setup
st.set_page_config(page_title="📨 Send SMS", layout="centered")
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #f6d365, #fda085);
            padding: 2rem;
            border-radius: 20px;
            max-width: 600px;
            margin: auto;
            color: #333;
        }
        h1 {
            color: #7b1fa2;
            text-align: center;
        }
        .stTextInput>div>div>input, textarea {
            border-radius: 12px;
            padding: 0.5rem;
            font-size: 1rem;
        }
        button[kind="primary"] {
            background: #7b1fa2 !important;
            color: white !important;
            font-weight: bold;
            border-radius: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>📨 Send SMS with Twilio</h1>", unsafe_allow_html=True)

# Inputs
to_number = st.text_input("📞 Enter recipient phone number (e.g., +91XXXXXXXXXX)")
msg = st.text_area("💬 Enter your message", "Hello! This is a test SMS from Streamlit + Twilio.")

# Send Button
if st.button("Send SMS 🚀"):
    if not to_number:
        st.warning("⚠️ Please enter a phone number.")
    else:
        try:
            client = Client(account_sid, auth_token)
            sms = client.messages.create(
                body=msg,
                from_=twilio_number,
                to=to_number
            )
            st.success(f"✅ SMS sent successfully! SID: {sms.sid}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
