import streamlit as st
import random
import time
import requests
import os
import pandas as pd
import pydeck as pdk
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
    if not client: return "Just go to Bhai Ji Shawarma!"
    try:
        prompt_text = f"Suggest 1 specific VEGETARIAN street food/snack dish near Sector 48 Gurgaon (Sohna Road). Cost must be UNDER ₹300. Think places like 'Bhai Ji Shawarma', 'Pushkar Raj Momos', 'Civil Lines'. Format: 'Dish Name' at 'Restaurant Name' (~Price). Add a witty reason why it fits the '{vibe}' vibe."
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a Gurgaon street food expert. You know the best budget spots."},
                {"role": "user", "content": prompt_text}
            ]
        )
        return response.choices[0].message.content
    except:
        return "Just get Kurkure Momos from Pushkar Raj. Classic."

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

    /* DYNAMIC BACKGROUND */
    .stApp {
        background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #ffd1ff, #a1c4fd);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    .stApp::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("https://www.transparenttextures.com/patterns/hearts.png");
        opacity: 0.6;
        pointer-events: none;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* TITLE STYLE */
    .title-text {
        font-family: 'Pacifico', cursive;
        font-size: 60px;
        color: white;
        text-align: center;
        text-shadow: 3px 3px 0px #ff0066, 6px 6px 0px rgba(0,0,0,0.2);
        margin-bottom: 10px;
        animation: bounce 2s infinite;
    }
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
        40% {transform: translateY(-20px);}
        60% {transform: translateY(-10px);}
    }

    /* BUTTONS */
    .stButton > button {
        background-color: #ffffff !important; 
        color: #000000 !important; 
        border: 2px solid #000000 !important;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 900 !important;
        text-transform: uppercase;
        box-shadow: 4px 4px 0px #000000 !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px #000000 !important;
        background-color: #ffe6e6 !important;
    }

    /* TABS */
    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 2px solid #000;
        box-shadow: 5px 5px 0px rgba(0,0,0,0.2);
    }

    h1, h2, h3 { color: #D63384 !important; text-shadow: 2px 2px 0px #ffffff; font-family: 'Arial Black', sans-serif; }
    p, div, label, span, li { color: #000000 !important; font-weight: 600; }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- AUTHENTICATION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<p class="title-text">Locked 🔒</p>', unsafe_allow_html=True)
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
st.markdown('<p class="title-text">My Capybara ❤️</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1,2,1])
with c2:
    st.image("https://media.giphy.com/media/Q8OPrlvICzjajupr2T/giphy.gif")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Us", "🍽️ Food", "🎰 Play", "💌 Vent", "📍 Map"])

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
    
    st.markdown("### 📸 Memories")
    photo_dir = "photos"
    if os.path.exists(photo_dir) and len(os.listdir(photo_dir)) > 0:
        images = [f for f in os.listdir(photo_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        if images:
            random_image = random.choice(images)
            st.image(f"{photo_dir}/{random_image}", caption="Us ❤️")
            if st.button("Next Pic 🔄", use_container_width=True):
                st.rerun()
    else:
        st.info("💡 (Upload photos to GitHub to see them here!)")
    
    st.markdown("---")
    st.markdown("### 💌 Daily Note")
    if "daily_note" not in st.session_state:
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

# --- TAB 2: STREET FOOD GUIDE ---
with tab2:
    st.markdown("### 🥟 Street Foodie")
    st.write("Tasty and Near Sector 48 (Under ₹300).")
    vibe = st.select_slider("Mood?", options=["Momos 🥟", "Spicy 🌶️", "Cheesy 🧀", "Desi 🥘", "Sweet 🍩"])
    if st.button("Find Snack 🌯", use_container_width=True):
        with st.spinner("Scanning street stalls..."):
            suggestion = get_food_suggestion(vibe)
            st.success(suggestion)

# --- TAB 3: SPICY SLOTS ---
with tab3:
    st.markdown("### 🎰 Naughty Slots")
    st.write("Spin to unlock a reward. (18+)")
    
    spicy_gifts = [
        "😈 Coupon: I go down on you (No questions asked)",
        "🧴 Reward: Full Body Oil Massage (30 mins)",
        "🚿 Reward: Shower Together Voucher",
        "👙 Reward: You pick my underwear/outfit today",
        "💋 Reward: 100 Kisses anywhere you want",
        "👀 Reward: I strip for you (Don't laugh)",
        "🧞‍♂️ Coupon: One Bedroom 'Wish' (I do anything)",
        "🍑 Reward: A good hard spanking",
        "💤 Reward: We sleep naked tonight"
    ]
    
    if st.button("SPIN IT! 🎲", use_container_width=True):
        items = ["😈", "🍑", "🥔", "🫦", "❤️", "🍆"]
        with st.spinner("Spinning..."):
            time.sleep(1)
        
        force_win = False
        if random.random() < 0.40:
            force_win = True
            
        if force_win:
            a = "😈"
            b = "😈"
            c = "❤️" 
        else:
            a = random.choice(items)
            b = random.choice(items)
            c = random.choice(items)
        
        st.markdown(f"<h1 style='text-align: center; color: black !important;'>{a} | {b} | {c}</h1>", unsafe_allow_html=True)
        
        if a == b == c:
            st.balloons()
            prize = "🧞‍♂️ JACKPOT: I do ANYTHING you say today."
            st.success(f"{prize}")
        elif force_win:
             st.info("Lucky Spin! 🥈")
             st.success("🤫 Reward: Roleplay Night (You choose the script)")
             st.caption("Valid for 24 hours!")
        elif a == b or b == c or a == c:
            st.info("Mini Win! 🥈")
            prize = random.choice(spicy_gifts)
            st.write(f"You won: **{prize}**")
        else:
            st.error("No Match! 😢 But I still love you.")
            st.write("Spin again baby.")

# --- TAB 4: VENT ---
with tab4:
    st.markdown("### 🛡️ Safe Space")
    reason = st.selectbox("What's up?", ["Work Stress", "Miss You", "Anxious", "Just Venting"])
    details = st.text_area("Tell me more:", placeholder="...")
    if st.button("Send to Shalv 📨", use_container_width=True):
        st.warning(f"Message sent. I love you.")
        st.video("https://www.youtube.com/watch?v=f9PKHVesfDc")
        send_notification(f"🚨 Capybara Alert! {reason}: {details}")

# --- TAB 5: MAP OF US (3 LOCATIONS) ---
with tab5:
    st.markdown("### 📍 Where it all started")
    
    # 1. Define Data
    map_data = pd.DataFrame({
        'lat': [28.4026, 28.4108, 28.3930],
        'lon': [77.0673, 77.0380, 77.0680],
        'label': ['First Date', 'First Kiss', 'First Meeting'],
        'color': [
            [255, 0, 128, 200],  # Pink (Date)
            [255, 0, 0, 200],    # Red (Kiss)
            [0, 200, 0, 200]     # Green (Meeting - Green Top)
        ]
    })
    
    # 2. Define Layers
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        map_data,
        get_position='[lon, lat]',
        get_color='color',
        get_radius=200,
        pickable=True,
    )
    
    text_layer = pdk.Layer(
        "TextLayer",
        map_data,
        get_position='[lon, lat]',
        get_text='label',
        get_size=15, 
        get_color=[0, 0, 0, 255], 
        get_angle=0,
        get_text_anchor='"middle"',
        get_alignment_baseline='"top"'
    )
    
    # 3. View State
    view_state = pdk.ViewState(
        latitude=28.405,
        longitude=77.055,
        zoom=13,
        pitch=0
    )
    
    # 4. Render
    st.pydeck_chart(pdk.Deck(
        layers=[scatter_layer, text_layer],
        initial_view_state=view_state,
        tooltip={"text": "{label}"}
    ))
    
    st.markdown("---")
    # THE LEGEND
    st.markdown("### 🗺️ Legend")
    st.markdown("""
    <div style='background-color: rgba(255,255,255,0.7); padding: 15px; border-radius: 10px; border: 2px solid black;'>
        <p style='color: green; margin:0; font-size: 16px;'>🟢 <b>First Meeting:</b> Salescode.ai (M3M Urbana); Where I first was fascinated by your Green Top</p>
        <br>
        <p style='color: #D63384; margin:0; font-size: 16px;'>🌸 <b>First Date:</b> Trippy Tequila M3M IFC; Where I realized I like you</p>
        <br>
        <p style='color: red; margin:0; font-size: 16px;'>🔴 <b>First Kiss:</b> Parking of Vega Schools; Where I realized I love you</p>
    </div>
    """, unsafe_allow_html=True)
