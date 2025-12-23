import streamlit as st
import random
from datetime import date

# --- CONFIGURATION (MUST BE FIRST) ---
st.set_page_config(page_title="For My Penguin", page_icon="🐧", layout="centered")

# --- CUSTOM CSS (THE UI MAGIC) ---
# This block injects custom HTML/CSS to change how everything looks
st.markdown("""
    <style>
    /* IMPORT GOOGLE FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Poppins:wght@300;500;700&display=swap');

    /* BACKGROUND GRADIENT */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* CUSTOM FONTS */
    h1 {
        font-family: 'Pacifico', cursive;
        color: white !important;
        text-align: center;
        font-size: 3.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    h2, h3 {
        font-family: 'Poppins', sans-serif;
        color: white !important;
    }
    
    p, div {
        font-family: 'Poppins', sans-serif;
        color: white;
    }

    /* GLASSMORPHISM CARDS */
    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }

    /* BUTTON STYLING */
    .stButton > button {
        background-color: white !important;
        color: #e73c7e !important;
        border-radius: 30px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    /* INPUT FIELD STYLING */
    .stTextInput > div > div > input {
        border-radius: 20px;
        text-align: center;
        background-color: rgba(255, 255, 255, 0.8);
        color: #333;
    }

    /* REMOVE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- AUTHENTICATION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<br><br><br>", unsafe_allow_html=True) # Spacer
    st.title("Login ❤️")
    st.markdown("<p style='text-align: center;'>For the prettiest girl in the world</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        password = st.text_input("Password", type="password", placeholder="🐧 magic word", label_visibility="collapsed")
        if st.button("Unlock My Gift", use_container_width=True):
            if password == "penguin123": 
                st.session_state.authenticated = True
                st.rerun()
            elif password:
                st.error("Nuh uh! Wrong password! 🤨")
    st.stop() 

# --- MAIN APP ---
st.title("Hey Penguin ❤️")

# Tabs with Emojis
tab1, tab2, tab3 = st.tabs(["   🏠 Home   ", "   🍽️ Decisions   ", "   💌 Vent   "])

# --- TAB 1: DASHBOARD ---
with tab1:
    st.markdown("### 💑 Our Timeline")
    
    # METRICS IN COLUMNS
    start_date = date(2024, 9, 7) 
    today = date.today()
    delta = today - start_date
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"<h2 style='text-align: center;'>{delta.days}</h2><p style='text-align: center;'>Days Together</p>", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"<h2 style='text-align: center;'>{delta.days * 24}</h2><p style='text-align: center;'>Hours of Love</p>", unsafe_allow_html=True)

    st.markdown("---")
    
    # JUKEBOX CARD
    st.markdown("### 🎵 Our Jam")
    songs = {
        "Mere Bina (Crook)": "https://www.youtube.com/watch?v=f9PKHVesfDc",
        "I Wanna Be Yours (AM)": "https://www.youtube.com/watch?v=nyuo9-OjNNg",
        "Die For You (Weeknd)": "https://www.youtube.com/watch?v=2AH5l-vrY9Q",
        "Take Me to the River": "https://www.youtube.com/watch?v=6ar2VHW1i2w" 
    }
    selected_song = st.selectbox("", list(songs.keys()), label_visibility="collapsed")
    st.video(songs[selected_song])

    st.markdown("---")
    st.markdown(f"**Daily Note:** {random.choice(['You are my favorite notification.', 'I love you more than cricket.', 'You look cute today.'])}")

# --- TAB 2: FOOD ---
with tab2:
    st.markdown("### 🤷‍♀️ Can't Decide?")
    st.write("Click the button and let fate decide our dinner.")
    
    food_options = ["Pizza 🍕", "Sushi 🍣", "Burgers 🍔", "Biryani 🥘", "Chinese 🍜", "Maggi 🍝"]
    
    if st.button("✨ Spin the Wheel ✨", use_container_width=True):
        choice = random.choice(food_options)
        st.markdown(f"<h2 style='text-align: center; color: #fff;'>We are eating: <br>✨ {choice} ✨</h2>", unsafe_allow_html=True)
        st.balloons()

# --- TAB 3: EMOTIONS ---
with tab3:
    st.markdown("### 💬 Safe Space")
    st.write("How is your heart doing right now?")
    
    mood = st.selectbox("", ["Happy", "Sad", "Angry", "Tired", "Miss You"], label_visibility="collapsed")
    
    if st.button("Tell me", use_container_width=True):
        if mood == "Sad":
            st.warning("I'm sorry baby. Remember I'm just a call away.")
            st.video("https://www.youtube.com/watch?v=f9PKHVesfDc") # Auto-play comfort song
            
        elif mood == "Angry":
            st.error("Deep breaths. I'm on your team. Always.")
            
        elif mood == "Miss You":
            st.info("I miss you too. Look at your gallery, I'm right there.")
            
        elif mood == "Tired":
            st.write("Put the phone down. Close your eyes. I love you.")
            
        elif mood == "Happy":
            st.success("Yay! Keep smiling, it suits you!")
            st.balloons()
