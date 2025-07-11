import os
from dotenv import load_dotenv
from twilio.rest import Client
import streamlit as st

# Load .env
load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

# Streamlit config
st.set_page_config(page_title="📞Voice Call", layout="centered")

# Title
st.markdown("<h1>Make a Voice Call</h1>", unsafe_allow_html=True)

# Inputs
to_number = st.text_input("Enter recipient phone number (e.g., +91XXXXXXXXXX)", "")
message = st.text_area("Voice Message to Speak", "Hello! This is a test call from Streamlit + Twilio.")

# Call button
if st.button("Make Call"):
    if not to_number:
        st.warning("⚠️ Please enter a phone number.")
    else:
        try:
            client = Client(account_sid, auth_token)
            call = client.calls.create(
                twiml=f'<Response><Say>{message}</Say></Response>',
                from_=twilio_number,
                to=to_number
            )
            st.success(f"📞 Call initiated! SID: {call.sid}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
