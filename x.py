import streamlit as st
import tweepy
import os
from dotenv import load_dotenv

# Load Twitter credentials
load_dotenv()
API_KEY = os.getenv("X_API_KEY")
API_SECRET = os.getenv("X_API_SECRET")
ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

# Setup Twitter auth
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Streamlit UI
st.set_page_config(page_title="🐦 Twitter Poster")
st.title("Post a Tweet")

tweet = st.text_area("What's happening?", max_chars=280, height=150)

if st.button("Tweet"):
    if not tweet.strip():
        st.warning("Tweet cannot be empty.")
    else:
        try:
            api.update_status(tweet)
            st.success("✅ Tweet posted successfully!")
        except Exception as e:
            st.error(f"❌ Failed: {e}")
