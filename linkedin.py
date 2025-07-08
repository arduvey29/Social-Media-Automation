import streamlit as st
import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlencode

# Load environment variables
load_dotenv()
CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# OAuth and API URLs
AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
ME_URL = "https://api.linkedin.com/v2/me"
POST_URL = "https://api.linkedin.com/v2/ugcPosts"

# Streamlit App UI
st.set_page_config(page_title="🔗 LinkedIn Poster", layout="centered")
st.title("Post to LinkedIn Feed")

# Step 1: Authorization
if "access_token" not in st.session_state:
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "w_member_social r_liteprofile"
    }
    auth_url = f"{AUTH_URL}?{urlencode(params)}"
    st.markdown(f"[🔐 Click here to authorize LinkedIn]({auth_url})")

    # After redirection, get code
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
            token_data = token_res.json()
            st.session_state["access_token"] = token_data["access_token"]
            st.success("✅ Authorized with LinkedIn!")
            st.experimental_rerun()
        else:
            st.error("❌ Failed to retrieve access token.")

# Step 2: Post to feed
if "access_token" in st.session_state:
    headers = {
        "Authorization": f"Bearer {st.session_state['access_token']}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Get your own LinkedIn user URN
    user_res = requests.get(ME_URL, headers=headers)
    if user_res.status_code == 200:
        user_urn = f"urn:li:person:{user_res.json()['id']}"
        post_text = st.text_area("📝 Write your LinkedIn post", height=150)

        if st.button("📤 Post to LinkedIn"):
            if not post_text.strip():
                st.warning("⚠️ Post content cannot be empty.")
            else:
                post_payload = {
                    "author": user_urn,
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {
                                "text": post_text
                            },
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
                    st.success("✅ Post successfully published to LinkedIn!")
                else:
                    st.error(f"❌ Failed to post: {post_res.text}")
    else:
        st.error("❌ Couldn't fetch your LinkedIn profile.")
