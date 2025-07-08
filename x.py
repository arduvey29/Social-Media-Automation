import streamlit as st

# Streamlit Page Config
st.set_page_config(page_title="🐦 Twitter Poster", layout="centered")

# Custom CSS for minimalistic design
st.markdown("""
    <style>
        /* Body and background styles */
        .stApp {
            background: linear-gradient(to right, #e0eafc, #cfdef3); /* Light gradient background */
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #333;
            font-family: 'Helvetica', sans-serif;
            padding: 0 15px; /* Reduced padding for a tighter layout */
        }
        
        /* Title styling */
        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            color: #333;
            text-align: center;
            margin-bottom: 25px; /* Reduced margin between title and input */
        }

        /* Text Area (tweet input field) styling */
        .stTextArea textarea {
            font-size: 1rem;
            border-radius: 12px;
            padding: 1rem;
            width: 100%;
            max-width: 800px; /* Max width for proper alignment */
            margin-bottom: 50px; /* Reduced bottom margin */
            border: 1px solid #ddd;
            background-color: rgba(255, 255, 255, 0.9);
            resize: none; /* Disable resizing */
        }

        /* Button styling */
        .stButton>button {
            background-color: #1DA1F2; /* Twitter blue */
            color: white;
            border-radius: 12px;
            padding: 14px 24px;
            font-size: 16px;
            width: 100%;
            max-width: 600px; /* Match width of input field */
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.3s ease;
            font-weight: 600;
            margin-top: 15px; /* Reduced top margin for button */
        }

        .stButton>button:hover {
            background-color: #1991db; /* Darker blue on hover */
            transform: scale(1.05);
        }

        .stButton>button:active {
            background-color: #1477c2; /* Active state */
        }

        /* Ensuring proper spacing and alignment */
        .stTextInput, .stTextArea {
            margin-left: auto;
            margin-right: auto;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Post a Tweet on Twitter")

# Text area to input the tweet
tweet = st.text_area("What's happening?", max_chars=280, height=150)

# Button click logic
if tweet.strip():  # Only generate link if tweet isn't empty
    tweet_url = f"https://twitter.com/intent/tweet?text={tweet.replace(' ', '%20')}"
    
    # HTML Link with a smooth button design
    st.markdown(f'''
        <a href="{tweet_url}" target="_blank">
            <button style="
                background-color: #1DA1F2; 
                color: white; 
                border-radius: 12px; 
                padding: 14px 24px; 
                font-size: 16px; 
                width: 100%;
                max-width: 600px;
                border: none;
                cursor: pointer;
                transition: background-color 0.3s ease, transform 0.3s ease;
                font-weight: 600;
                margin-top: 15px;
            ">
                🚀 Post your Tweet!
            </button>
        </a>
    ''', unsafe_allow_html=True)
else:
    st.warning("⚠️ Please enter your tweet before posting.")
