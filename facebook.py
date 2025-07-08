import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load .env values
load_dotenv()
PAGE_ID = os.getenv("FB_PAGE_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

st.set_page_config(page_title="Facebook Page Poster", layout="centered")
st.title("Facebook Page Poster (Official Graph API)")

message = st.text_area("Write your Facebook post", height=150)
link = st.text_input("🔗 (Optional) Add a link to share")

if st.button("Post to Facebook Page"):
    if not message:
        st.warning("⚠️ Message cannot be empty.")
    else:
        post_url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/feed"
        data = {
            "message": message,
            "access_token": ACCESS_TOKEN
        }
        if link:
            data["link"] = link

        res = requests.post(post_url, data=data)

        if res.status_code == 200:
            st.success("✅ Post published successfully to your Page!")
        else:
            st.error(f"❌ Error: {res.text}")
