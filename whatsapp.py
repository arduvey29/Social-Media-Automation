import streamlit as st
import pywhatkit
import datetime

# Streamlit Page Config
st.set_page_config(page_title="📱 WhatsApp Message Sender", layout="centered")
st.title("📱 Send WhatsApp Message with PyWhatKit")

# Input fields
phone = st.text_input("Enter phone number (with country code)", value="+91")
message = st.text_area("Enter your message", height=100)

col1, col2 = st.columns(2)
with col1:
    hour = st.number_input("⏰ Hour (24h format)", min_value=0, max_value=23, value=datetime.datetime.now().hour)
with col2:
    minute = st.number_input("⏱️ Minute", min_value=0, max_value=59, value=(datetime.datetime.now().minute + 2) % 60)

# Schedule button
if st.button("🚀 Send Message"):
    if not phone or not message:
        st.warning("⚠️ Phone number and message are required.")
    else:
        try:
            pywhatkit.sendwhatmsg(phone, message, int(hour), int(minute), wait_time=10)
            st.success(f"✅ Message scheduled for {hour:02}:{minute:02} to {phone}")
            st.info("ℹ️ Keep the browser open and logged into WhatsApp Web.")
        except Exception as e:
            st.error(f"❌ Failed to send message: {e}")
