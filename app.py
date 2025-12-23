import streamlit as st
import random
import requests # For notifications
from datetime import date
from openai import AzureOpenAI

# --- CONFIGURATION ---
st.set_page_config(page_title="For My Penguin", page_icon="🐧", layout="centered")

# --- AI SETUP ---
# Tries to get secrets, falls back to empty if running locally without config
try:
    client = AzureOpenAI(
        api_key=st.secrets["AZURE_OPENAI_API_KEY"],
        api_version=st.secrets["AZURE_OPENAI_VERSION"],
        azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"]
    )
    deployment_name = st.secrets["AZURE_DEPLOYMENT_NAME"]
except:
    st.error("Secrets not set up! Tell Shalv to fix the API keys.")
    st.stop()

# --- HELPER FUNCTIONS ---

def send_notification(message):
    """Sends a push notification to Shalv's phone via ntfy.sh"""
    # This sends a POST request to a public topic. 
    # You can subscribe to 'shalv_penguin_alert' on the ntfy app.
    try:
        requests.post("https://ntfy.sh/shalv_penguin_alert", 
                      data=message.encode(encoding='utf-8'))
    except:
        pass

def get_ai_love_note():
    """Generates a dynamic love note"""
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a romantic boyfriend named Shalv. Write a 1-sentence witty, cute, and deeply romantic note for your girlfriend (call her Penguin). Do not be cringy. Be charming."},
                {"role": "user", "content": "Write a note for today."}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return "I love you more than Python code. (AI Error, but the feeling is real)"

def get_food_suggestion(vibe):
    """Generates food options based on vibe"""
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a Michelin star chef and relationship coach. The user will give you a 'vibe'. Suggest 1 specific dish and a cute reason why it fits the mood. Keep it short."},
                {"role": "user", "content": f"The vibe is {vibe}"}
            ]
        )
        return response.choices[0].message.content
    except:
        return "Let's just order Pizza. The AI is hungry."

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* ANIMATED GRADIENT BACKGROUND */
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

    /* GLASSMORPHISM TABS */
    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(255, 255, 255, 0.25); /* More opaque */
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }

    /* HEADERS */
    h1, h2, h3 {
        color: white !important;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.2);
    }
    
    p, div, label {
        color: white !important;
        font-weight: 500;
    }

    /* BUTTON FIX - DARK PINK TEXT */
    .stButton > button {
        background-color: white !important;
        color: #D63384 !important; /* DARK PINK TEXT - HIGH CONTRAST */
        font-weight: 900 !important;
        border-radius: 30px;
        border: none;
        padding: 12px 25px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        background-color: #f8f9fa !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    /* HIDE DEFAULT ELEMENTS */
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
        password = st.text_input("Password", type="password", placeholder="🐧 magic word", label_visibility="collapsed")
        if st.button("Unlock", use_container_width=True):
            if password == "penguin123": 
                st.session_state.authenticated = True
                st.rerun()
            elif password:
                st.error("Try again beautiful 🤨")
    st.stop() 

# --- MAIN APP ---
st.title("Hey Penguin ❤️")

tab1, tab2, tab3 = st.tabs(["   🏠 Home   ", "   🍽️ Food AI   ", "   💌 Vent   "])

# --- TAB 1: DASHBOARD ---
with tab1:
    st.markdown("### 💑 Us")
    
    start_date = date(2024, 9, 7) 
    today = date.today()
    delta = today - start_date
    
    c1, c2 = st.columns(2)
    c1.markdown(f"<h2 style='text-align: center;'>{delta.days}</h2><p style='text-align: center;'>Days Together</p>", unsafe_allow_html=True)
    c2.markdown(f"<h2 style='text-align: center;'>{delta.days * 24}</h2><p style='text-align: center;'>Hours of Love</p>", unsafe_allow_html=True)

    st.markdown("---")
    
    # AI GENERATED LOVE NOTE
    st.markdown("### 📝 Note of the Day")
    if "daily_note" not in st.session_state:
        with st.spinner("Writing you a poem..."):
            st.session_state.daily_note = get_ai_love_note()
            
    st.info(f"✨ {st.session_state.daily_note}")
    
    if st.button("Generate New Note 🎲"):
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
    selected_song = st.selectbox("", list(songs.keys()), label_visibility="collapsed")
    st.video(songs[selected_song])

# --- TAB 2: AI FOOD CHEF ---
with tab2:
    st.markdown("### 👨‍🍳 Chef Shalv AI")
    st.write("Don't know what to eat? Tell me the vibe.")
    
    vibe = st.select_slider("What's the mood?", options=["Comfort Food 🧸", "Spicy/Adventure 🌶️", "Healthy-ish 🥗", "Fancy Date 🍷", "Sweet Tooth 🍩"])
    
    if st.button("Consult the Chef 🍳", use_container_width=True):
        with st.spinner("Analyzing your cravings..."):
            suggestion = get_food_suggestion(vibe)
            st.success(suggestion)

# --- TAB 3: VENT & NOTIFY ---
with tab3:
    st.markdown("### 🛡️ Safe Space")
    st.write("I'm listening.")
    
    reason = st.selectbox("What's wrong?", 
                          ["I had a bad day at work", "I miss you", "I'm just anxious", "Someone was mean", "I need attention"])
    
    details = st.text_area("Want to type it out?", placeholder="Vent here...")
    
    if st.button("Send to Shalv 📨", use_container_width=True):
        # 1. Show UI Feedback
        st.warning(f"I'm sorry you feel this way regarding '{reason}'.")
        st.write("Listening to this usually helps:")
        st.video("https://www.youtube.com/watch?v=f9PKHVesfDc")
        
        # 2. Send Notification
        alert_msg = f"🚨 Penguin Alert! Reason: {reason}. Note: {details}"
        send_notification(alert_msg)
        st.toast("Notification sent to Shalv's phone!", icon="✅")
