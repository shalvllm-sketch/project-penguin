import streamlit as st
import random
import time
import requests
import os
from datetime import date
from openai import AzureOpenAI

# --- CONFIGURATION ---
st.set_page_config(page_title="For My Capybara", page_icon="🥔", layout="centered")

# --- AI SETUP ---
try:
    client = AzureOpenAI(
        api_key=st.secrets["AZURE_OPENAI_API_KEY"],
        api_version=st.secrets["AZURE_OPENAI_VERSION"],
        azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"]
    )
    deployment_name = st.secrets["AZURE_DEPLOYMENT_NAME"]
except:
    client = None

# --- HELPER FUNCTIONS ---
def send_notification(message):
    try:
        requests.post("https://ntfy.sh/shalv_penguin_alert", 
                      data=message.encode(encoding='utf-8'))
    except:
        pass

def get_ai_love_note():
    if not client: return "I love you more than code! (AI Offline)"
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a romantic boyfriend named Shalv. Write a 1-sentence witty, cute love note for your girlfriend 'Capybara'. Use emojis."},
                {"role": "user", "content": "Write a note for today."}
            ]
        )
        return response.choices[0].message.content
    except:
        return "You are my favorite notification ❤️"

def get_food_suggestion(vibe):
    if not client: return "Order Domino's! (AI Offline)"
    try:
        prompt_text = f"Suggest 1 specific VEGETARIAN dish from a REAL restaurant near Sector 48 Gurgaon (within 45 mins drive). Cost must be UNDER ₹500. Format: 'Dish Name' at 'Restaurant Name' (~Price). Add a short witty reason why it fits the '{vibe}' vibe."
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a local Gurgaon food guide. You know the best hidden gems near Sector 48, Sohna Road, and Nirvana Country."},
                {"role": "user", "content": prompt_text}
            ]
        )
        return response.choices[0].message.content
    except:
        return "Just get Chole Bhature from Civil Lines. It never fails."

# --- CUSTOM CSS (FALLING HEARTS & FIXES) ---
st.markdown("""
    <style>
    /* 1. FALLING HEARTS BACKGROUND */
    .stApp {
        background-color: #FFC0CB;
        background-image: url("https://www.transparenttextures.com/patterns/hearts.png");
        /* This animation moves the background down to look like falling rain/hearts */
        animation: falling 10s linear infinite;
    }
    
    @keyframes falling {
        from { background-position: 0 0; }
        to { background-position: 0 500px; }
    }

    /* 2. BUTTON FIX - STRICT HIGH CONTRAST */
    .stButton > button {
        background-color: #ffffff !important; /* Pure White */
        color: #000000 !important; /* Pure Black Text */
        border: 2px solid #000000 !important; /* Thick Black Border */
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 900 !important; /* Extra Bold */
        text-transform: uppercase;
        box-shadow: 4px 4px 0px #000000 !important; /* Comic Shadow */
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px #000000 !important;
        background-color: #ffe6e6 !important;
    }

    /* 3. GLASSMORPHISM TABS (Make text readable on hearts) */
    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(255, 255, 255, 0.85); /* High opacity white */
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 2px solid #000;
        box-shadow: 5px 5px 0px rgba(0,0,0,0.2);
    }

    /* 4. TEXT COLORS */
    h1, h2, h3 {
        color: #D63384 !important; /* Hot Pink Titles */
        text-shadow: 2px 2px 0px #ffffff;
        font-family: 'Arial Black', sans-serif;
    }
    p, div, label, span, li {
        color: #000000 !important; /* Black Body Text */
        font-weight: 600;
    }

    /* Hide Streamlit Elements */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- AUTHENTICATION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("🔒 Login")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.write("Password hint: What do I call you?")
        password = st.text_input("Password", type="password", label_visibility="collapsed")
        if st.button("Unlock ❤️", use_container_width=True):
            if password.lower() == "capybara123": 
                st.session_state.authenticated = True
                st.rerun()
            elif password:
                st.error("Access Denied! 🤨")
    st.stop() 

# --- MAIN APP ---
st.title("Hey Capybara 🥔")

# Capybara GIF
c1, c2, c3 = st.columns([1,2,1])
with c2:
    st.image("https://media.giphy.com/media/Q8OPrlvICzjajupr2T/giphy.gif")

tab1, tab2, tab3, tab4 = st.tabs(["🏠 Us", "🍽️ Food", "🎰 Play", "💌 Vent"])

# --- TAB 1: DASHBOARD ---
with tab1:
    st.markdown("### 💑 Our Timeline")
    start_date = date(2024, 9, 7) 
    today = date.today()
    delta = today - start_date
    
    c1, c2 = st.columns(2)
    c1.info(f"**{delta.days}** Days")
    c2.info(f"**{delta.days * 24}** Hours")

    st.markdown("---")
    
    # --- PHOTO GALLERY ---
    st.markdown("### 📸 Memory Lane")
    photo_dir = "photos"
    if os.path.exists(photo_dir) and len(os.listdir(photo_dir)) > 0:
        images = [f for f in os.listdir(photo_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        if images:
            random_image = random.choice(images)
            st.image(f"{photo_dir}/{random_image}", caption="Look at us! ❤️")
            if st.button("Another Memory 🔄", use_container_width=True):
                st.rerun()
    else:
        st.info("💡 (Upload photos to GitHub to see them here!)")

    st.markdown("---")
    
    st.markdown("### 💌 Daily Note")
    if "daily_note" not in st.session_state:
        with st.spinner("Writing..."):
            st.session_state.daily_note = get_ai_love_note()
            
    st.success(f"✨ {st.session_state.daily_note}")
    if st.button("New Note 🎲", use_container_width=True):
        del st.session_state.daily_note
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 🎵 Jukebox")
    songs = {
        "Mere Bina (Crook)": "https://www.youtube.com/watch?v=f9PKHVesfDc",
        "I Wanna Be Yours (AM)": "https://www.youtube.com/watch?v=nyuo9-OjNNg",
        "Die For You (Weeknd)": "https://www.youtube.com/watch?v=2AH5l-vrY9Q",
        "Take Me to the River": "https://www.youtube.com/watch?v=6ar2VHW1i2w" 
    }
    selected_song = st.selectbox("Vibe Check:", list(songs.keys()))
    st.video(songs[selected_song])

# --- TAB 2: GURGAON CHEF ---
with tab2:
    st.markdown("### 🥗 Sector 48 Foodie")
    st.write("Vegetarian. Under ₹500. Near You.")
    
    vibe = st.select_slider("Craving?", options=["Comfort 🧸", "Spicy 🌶️", "Healthy 🥗", "Fancy 🍷", "Sweet 🍩"])
    
    if st.button("Find me food 🥘", use_container_width=True):
        with st.spinner("Searching Sector 48..."):
            suggestion = get_food_suggestion(vibe)
            st.success(suggestion)

# --- TAB 3: THE SLOT MACHINE GAME (18+) ---
with tab3:
    st.markdown("### 🎰 Naughty Slots")
    st.write("Spin for a prize. (10 items = Harder to win!)")
    
    if st.button("SPIN IT! 🎲", use_container_width=True):
        # 10 OPTIONS
        items = ["😈", "🍑", "🥔", "🫦", "❤️", "🍆", "🧸", "💋", "🔥", "🧊"]
        
        with st.spinner("Spinning..."):
            time.sleep(1)
        
        a = random.choice(items)
        b = random.choice(items)
        c = random.choice(items)
        
        st.markdown(f"<h1 style='text-align: center; color: black !important;'>{a} | {b} | {c}</h1>", unsafe_allow_html=True)
        
        # LOGIC
        if a == b == c:
            st.balloons()
            st.success("JACKPOT! 🫦🫦🫦 Reward: Bedroom 'Yes' Day (I do whatever you say) 😈")
            st.markdown("*Screenshot this coupon immediately!*")
        elif a == b or b == c or a == c:
            st.info("Mini Win! Reward: Sensual Body Massage (Oil included) 🧴")
        elif "❤️" in [a, b, c] or "💋" in [a, b, c]:
            st.success("Love Win! Reward: 10 mins of Neck Kisses 💋")
        elif "🥔" in [a, b, c]:
            st.warning("You got a potato! Reward: I buy you fries. 🍟")
        else:
            st.error("No match! Strip... I mean, spin again. 😉")

# --- TAB 4: VENT ---
with tab4:
    st.markdown("### 🛡️ Safe Space")
    reason = st.selectbox("What's up?", ["Work Stress", "Miss You", "Anxious", "Just Venting"])
    details = st.text_area("Tell me more:", placeholder="...")
    
    if st.button("Send to Shalv 📨", use_container_width=True):
        st.warning(f"I hear you. Sending a virtual hug.")
        st.video("https://www.youtube.com/watch?v=f9PKHVesfDc")
        send_notification(f"🚨 Capybara Alert! {reason}: {details}")
        st.toast("Shalv notified!", icon="✅")
