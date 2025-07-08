
import streamlit as st
from pathlib import Path
import os
from dotenv import load_dotenv
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import pywhatkit
from instagrapi import Client
import tweepy
from urllib.parse import urlencode

# Load .env values
load_dotenv()

# ---------- Global Styling ----------
st.markdown("""
    <style>
        .main {
            background: linear-gradient(to right, #fdfbfb, #ebedee);
        }
        .stApp {
            font-family: 'Segoe UI', sans-serif;
        }
        .sidebar .sidebar-content {
            background: linear-gradient(to right, #c6ffdd, #fbd786, #f7797d);
            padding: 1rem;
            border-radius: 10px;
        }
        .css-1d391kg {
            color: #2e3d49;
        }
        button[kind="primary"] {
            background-color: #6A0572 !important;
            color: white !important;
            font-weight: bold;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Sidebar Navigation ----------
st.sidebar.title("📱 Multi-Platform Toolkit")
choice = st.sidebar.selectbox("Choose a Service", [
    "📩 Send SMS",
    "📞 Voice Call",
    "💬 WhatsApp Message",
    "📧 Send Email",
    "📸 Instagram Post",
    "🐦 Twitter Post",
    "🔗 LinkedIn Post",
    "📘 Facebook Page Post"
])

# ---------- 1. SMS ----------
if choice == "📩 Send SMS":
    from twilio.rest import Client
    st.title("📩 Send SMS with Twilio")
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
    to_number = st.text_input("Recipient Number (+91...)")
    msg = st.text_area("💬 Message", "Hello! Test SMS from Streamlit + Twilio.")
    if st.button("Send SMS 🚀"):
        try:
            client = Client(account_sid, auth_token)
            sms = client.messages.create(body=msg, from_=twilio_number, to=to_number)
            st.success(f"✅ SMS sent! SID: {sms.sid}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ---------- 2. Voice Call ----------
elif choice == "📞 Voice Call":
    from twilio.rest import Client
    st.title("📞 Make a Voice Call")
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
    to_number = st.text_input("📱 Recipient Number")
    message = st.text_area("🗣️ Message to Speak")
    if st.button("Make Call 📞"):
        try:
            client = Client(account_sid, auth_token)
            call = client.calls.create(
                twiml=f'<Response><Say>{message}</Say></Response>',
                from_=twilio_number,
                to=to_number
            )
            st.success(f"📞 Call initiated! SID: {call.sid}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ---------- 3. WhatsApp ----------
elif choice == "💬 WhatsApp Message":
    st.title("💬 Send WhatsApp Message with PyWhatKit")
    phone = st.text_input("Phone (+91...)", "+91")
    message = st.text_area("Message", height=100)
    hour = st.number_input("Hour (24h)", 0, 23, value=datetime.datetime.now().hour)
    minute = st.number_input("Minute", 0, 59, value=(datetime.datetime.now().minute + 2) % 60)
    if st.button("🚀 Schedule Message"):
        try:
            pywhatkit.sendwhatmsg(phone, message, int(hour), int(minute), wait_time=10)
            st.success(f"✅ Message scheduled for {hour:02}:{minute:02}")
            st.info("ℹ️ Keep browser open and logged into WhatsApp Web.")
        except Exception as e:
            st.error(f"❌ Failed: {e}")

# ---------- 4. Email ----------
elif choice == "📧 Send Email":
    st.title("📧 Send Email with Mailjet")
    smtp_user = os.getenv("MAILJET_API_KEY")
    smtp_pass = os.getenv("MAILJET_SECRET_KEY")
    sender_email = os.getenv("MAILJET_SENDER_EMAIL")
    receiver_email = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    body = st.text_area("Message")
    if st.button("🚀 Send Email"):
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
            st.success("✅ Email sent successfully!")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")

# ---------- 5. Instagram ----------
elif choice == "📸 Instagram Post":
    st.title("📸 Instagram Auto Poster")
    username = st.text_input("Instagram Username")
    password = st.text_input("Password", type="password")
    caption = st.text_area("Caption")
    image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if st.button("🚀 Post to Instagram"):
        try:
            image_path = f"temp_{image.name}"
            with open(image_path, "wb") as f:
                f.write(image.read())
            cl = Client()
            cl.login(username, password)
            cl.photo_upload(image_path, caption)
            os.remove(image_path)
            st.success("✅ Posted to Instagram!")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ---------- 6. Twitter ----------
elif choice == "🐦 Twitter Post":
    st.title("🐦 Post a Tweet")
    API_KEY = os.getenv("X_API_KEY")
    API_SECRET = os.getenv("X_API_SECRET")
    ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
    ACCESS_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    tweet = st.text_area("What's happening?", max_chars=280)
    if st.button("Tweet"):
        try:
            api.update_status(tweet)
            st.success("✅ Tweet posted successfully!")
        except Exception as e:
            st.error(f"❌ Failed: {e}")

# ---------- 7. LinkedIn ----------
elif choice == "🔗 LinkedIn Post":
    st.title("🔗 LinkedIn Poster")
    CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
    CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
    TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
    ME_URL = "https://api.linkedin.com/v2/me"
    POST_URL = "https://api.linkedin.com/v2/ugcPosts"
    if "access_token" not in st.session_state:
        params = {
            "response_type": "code",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "scope": "w_member_social r_liteprofile"
        }
        auth_url = f"{AUTH_URL}?{urlencode(params)}"
        st.markdown(f"[🔐 Click to Authorize LinkedIn]({auth_url})")
        query_params = st.experimental_get_query_params()
        if "code" in query_params:
            code = query_params["code"][0]
            token_res = requests.post(TOKEN_URL, data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET
            })
            if token_res.status_code == 200:
                st.session_state["access_token"] = token_res.json()["access_token"]
                st.experimental_rerun()
            else:
                st.error("❌ Token error.")
    else:
        headers = {
            "Authorization": f"Bearer {st.session_state['access_token']}",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        user_res = requests.get(ME_URL, headers=headers)
        if user_res.status_code == 200:
            user_urn = f"urn:li:person:{user_res.json()['id']}"
            post_text = st.text_area("Write your LinkedIn post")
            if st.button("📤 Post"):
                post_payload = {
                    "author": user_urn,
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {"text": post_text},
                            "shareMediaCategory": "NONE"
                        }
                    },
                    "visibility": {
                        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                    }
                }
                post_res = requests.post(
                    POST_URL,
                    headers={**headers, "Content-Type": "application/json"},
                    json=post_payload
                )
                if post_res.status_code == 201:
                    st.success("✅ Post published!")
                else:
                    st.error(f"❌ Failed: {post_res.text}")

# ---------- 8. Facebook ----------
elif choice == "📘 Facebook Page Post":
    st.title("📘 Facebook Page Poster")
    PAGE_ID = os.getenv("FB_PAGE_ID")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    message = st.text_area("Message to post")
    link = st.text_input("Optional link")
    if st.button("Post to Facebook Page"):
        post_url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/feed"
        data = {
            "message": message,
            "access_token": ACCESS_TOKEN
        }
        if link:
            data["link"] = link
        res = requests.post(post_url, data=data)
        if res.status_code == 200:
            st.success("✅ Post published to Page!")
        else:
            st.error(f"❌ Error: {res.text}")
