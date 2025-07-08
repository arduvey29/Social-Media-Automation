import streamlit as st
from instagrapi import Client
import os

# Streamlit UI
st.set_page_config(page_title="📸 Instagram Auto Poster", layout="centered")
st.title("📸 Instagram Auto Poster")

# Input fields
username = st.text_input("Instagram Username")
password = st.text_input("Instagram Password", type="password")
caption = st.text_area("Caption", height=150)
image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

# Post button
if st.button("🚀 Upload to Instagram"):
    if not username or not password or not caption or not image:
        st.warning("All fields are required.")
    else:
        try:
            # Save uploaded image to temp file
            image_path = f"temp_{image.name}"
            with open(image_path, "wb") as f:
                f.write(image.read())

            # Login to Instagram
            cl = Client()
            cl.login(username, password)

            # Upload photo
            cl.photo_upload(image_path, caption)
            st.success("✅ Post uploaded successfully to Instagram!")

            # Cleanup
            os.remove(image_path)
        except Exception as e:
            st.error(f"❌ Error: {e}")
