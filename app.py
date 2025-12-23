# import streamlit as st
# import random
# import requests # For notifications
# from datetime import date
# from openai import AzureOpenAI

# # --- CONFIGURATION ---
# st.set_page_config(page_title="For My Penguin", page_icon="🐧", layout="centered")

# # --- AI SETUP ---
# # Tries to get secrets, falls back to empty if running locally without config
# try:
#     client = AzureOpenAI(
#         api_key=st.secrets["AZURE_OPENAI_API_KEY"],
#         api_version=st.secrets["AZURE_OPENAI_VERSION"],
#         azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"]
#     )
#     deployment_name = st.secrets["AZURE_DEPLOYMENT_NAME"]
# except:
#     st.error("Secrets not set up! Tell Shalv to fix the API keys.")
#     st.stop()

# # --- HELPER FUNCTIONS ---

# def send_notification(message):
#     """Sends a push notification to Shalv's phone via ntfy.sh"""
#     # This sends a POST request to a public topic. 
#     # You can subscribe to 'shalv_penguin_alert' on the ntfy app.
#     try:
#         requests.post("https://ntfy.sh/shalv_penguin_alert", 
#                       data=message.encode(encoding='utf-8'))
#     except:
#         pass

# def get_ai_love_note():
#     """Generates a dynamic love note"""
#     try:
#         response = client.chat.completions.create(
#             model=deployment_name,
#             messages=[
#                 {"role": "system", "content": "You are a romantic boyfriend named Shalv. Write a 1-sentence witty, cute, and deeply romantic note for your girlfriend (call her Penguin). Do not be cringy. Be charming."},
#                 {"role": "user", "content": "Write a note for today."}
#             ]
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return "I love you more than Python code. (AI Error, but the feeling is real)"

# def get_food_suggestion(vibe):
#     """Generates food options based on vibe"""
#     try:
#         response = client.chat.completions.create(
#             model=deployment_name,
#             messages=[
#                 {"role": "system", "content": "You are a Michelin star chef and relationship coach. The user will give you a 'vibe'. Suggest 1 specific dish and a cute reason why it fits the mood. Keep it short."},
#                 {"role": "user", "content": f"The vibe is {vibe}"}
#             ]
#         )
#         return response.choices[0].message.content
#     except:
#         return "Let's just order Pizza. The AI is hungry."

# # --- CUSTOM CSS ---
# st.markdown("""
#     <style>
#     /* ANIMATED GRADIENT BACKGROUND */
#     .stApp {
#         background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
#         background-size: 400% 400%;
#         animation: gradient 15s ease infinite;
#     }
#     @keyframes gradient {
#         0% { background-position: 0% 50%; }
#         50% { background-position: 100% 50%; }
#         100% { background-position: 0% 50%; }
#     }

#     /* GLASSMORPHISM TABS */
#     .stTabs [data-baseweb="tab-panel"] {
#         background: rgba(255, 255, 255, 0.25); /* More opaque */
#         backdrop-filter: blur(15px);
#         border-radius: 20px;
#         padding: 20px;
#         border: 1px solid rgba(255, 255, 255, 0.3);
#         box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
#     }

#     /* HEADERS */
#     h1, h2, h3 {
#         color: white !important;
#         text-shadow: 0px 2px 4px rgba(0,0,0,0.2);
#     }
    
#     p, div, label {
#         color: white !important;
#         font-weight: 500;
#     }

#     /* BUTTON FIX - DARK PINK TEXT */
#     .stButton > button {
#         background-color: white !important;
#         color: #D63384 !important; /* DARK PINK TEXT - HIGH CONTRAST */
#         font-weight: 900 !important;
#         border-radius: 30px;
#         border: none;
#         padding: 12px 25px;
#         transition: all 0.3s ease;
#     }
#     .stButton > button:hover {
#         transform: scale(1.05);
#         background-color: #f8f9fa !important;
#         box-shadow: 0 5px 15px rgba(0,0,0,0.2);
#     }

#     /* HIDE DEFAULT ELEMENTS */
#     #MainMenu, footer, header {visibility: hidden;}
#     </style>
#     """, unsafe_allow_html=True)

# # --- AUTHENTICATION ---
# if "authenticated" not in st.session_state:
#     st.session_state.authenticated = False

# if not st.session_state.authenticated:
#     st.markdown("<br><br>", unsafe_allow_html=True)
#     st.title("🔒 Login")
#     col1, col2, col3 = st.columns([1,2,1])
#     with col2:
#         password = st.text_input("Password", type="password", placeholder="🐧 magic word", label_visibility="collapsed")
#         if st.button("Unlock", use_container_width=True):
#             if password == "penguin123": 
#                 st.session_state.authenticated = True
#                 st.rerun()
#             elif password:
#                 st.error("Try again beautiful 🤨")
#     st.stop() 

# # --- MAIN APP ---
# st.title("Hey Penguin ❤️")

# tab1, tab2, tab3 = st.tabs(["   🏠 Home   ", "   🍽️ Food AI   ", "   💌 Vent   "])

# # --- TAB 1: DASHBOARD ---
# with tab1:
#     st.markdown("### 💑 Us")
    
#     start_date = date(2024, 9, 7) 
#     today = date.today()
#     delta = today - start_date
    
#     c1, c2 = st.columns(2)
#     c1.markdown(f"<h2 style='text-align: center;'>{delta.days}</h2><p style='text-align: center;'>Days Together</p>", unsafe_allow_html=True)
#     c2.markdown(f"<h2 style='text-align: center;'>{delta.days * 24}</h2><p style='text-align: center;'>Hours of Love</p>", unsafe_allow_html=True)

#     st.markdown("---")
    
#     # AI GENERATED LOVE NOTE
#     st.markdown("### 📝 Note of the Day")
#     if "daily_note" not in st.session_state:
#         with st.spinner("Writing you a poem..."):
#             st.session_state.daily_note = get_ai_love_note()
            
#     st.info(f"✨ {st.session_state.daily_note}")
    
#     if st.button("Generate New Note 🎲"):
#         del st.session_state.daily_note
#         st.rerun()

#     st.markdown("---")
#     st.markdown("### 🎵 Jukebox")
#     songs = {
#         "Mere Bina (Crook)": "https://www.youtube.com/watch?v=f9PKHVesfDc",
#         "I Wanna Be Yours (AM)": "https://www.youtube.com/watch?v=nyuo9-OjNNg",
#         "Die For You (Weeknd)": "https://www.youtube.com/watch?v=2AH5l-vrY9Q",
#         "Take Me to the River": "https://www.youtube.com/watch?v=6ar2VHW1i2w" 
#     }
#     selected_song = st.selectbox("", list(songs.keys()), label_visibility="collapsed")
#     st.video(songs[selected_song])

# # --- TAB 2: AI FOOD CHEF ---
# with tab2:
#     st.markdown("### 👨‍🍳 Chef Shalv AI")
#     st.write("Don't know what to eat? Tell me the vibe.")
    
#     vibe = st.select_slider("What's the mood?", options=["Comfort Food 🧸", "Spicy/Adventure 🌶️", "Healthy-ish 🥗", "Fancy Date 🍷", "Sweet Tooth 🍩"])
    
#     if st.button("Consult the Chef 🍳", use_container_width=True):
#         with st.spinner("Analyzing your cravings..."):
#             suggestion = get_food_suggestion(vibe)
#             st.success(suggestion)

# # --- TAB 3: VENT & NOTIFY ---
# with tab3:
#     st.markdown("### 🛡️ Safe Space")
#     st.write("I'm listening.")
    
#     reason = st.selectbox("What's wrong?", 
#                           ["I had a bad day at work", "I miss you", "I'm just anxious", "Someone was mean", "I need attention"])
    
#     details = st.text_area("Want to type it out?", placeholder="Vent here...")
    
#     if st.button("Send to Shalv 📨", use_container_width=True):
#         # 1. Show UI Feedback
#         st.warning(f"I'm sorry you feel this way regarding '{reason}'.")
#         st.write("Listening to this usually helps:")
#         st.video("https://www.youtube.com/watch?v=f9PKHVesfDc")
        
#         # 2. Send Notification
#         alert_msg = f"🚨 Penguin Alert! Reason: {reason}. Note: {details}"
#         send_notification(alert_msg)
#         st.toast("Notification sent to Shalv's phone!", icon="✅")



















import streamlit as st
import random
import requests # For notifications
from datetime import date
from openai import AzureOpenAI

# --- CONFIGURATION ---
st.set_page_config(page_title="For My Penguin", page_icon="🐧", layout="centered")

# --- AI SETUP ---
try:
    client = AzureOpenAI(
        api_key=st.secrets["AZURE_OPENAI_API_KEY"],
        api_version=st.secrets["AZURE_OPENAI_VERSION"],
        azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"]
    )
    deployment_name = st.secrets["AZURE_DEPLOYMENT_NAME"]
except:
    # If secrets aren't set, we won't crash, just disable AI features gracefully
    client = None

# --- HELPER FUNCTIONS ---
def send_notification(message):
    try:
        requests.post("https://ntfy.sh/shalv_penguin_alert", 
                      data=message.encode(encoding='utf-8'))
    except:
        pass

def get_ai_love_note():
    if not client: return "I love you more than code! (Add API Key for new poems)"
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a romantic boyfriend. Write a 1-sentence witty, cute, and deeply romantic note for your girlfriend 'Penguin'. Use emojis."},
                {"role": "user", "content": "Write a note for today."}
            ]
        )
        return response.choices[0].message.content
    except:
        return "You are my favorite bug in the system ❤️"

def get_food_suggestion(vibe):
    if not client: return "Let's order Pizza! (AI is offline)"
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a Michelin star chef. Suggest 1 specific dish based on the vibe. Keep it short and add a 'Chef Kiss' comment."},
                {"role": "user", "content": f"The vibe is {vibe}"}
            ]
        )
        return response.choices[0].message.content
    except:
        return "Let's just get Maggi. It never fails."

# --- CUSTOM CSS (VISUALS) ---
st.markdown("""
    <style>
    /* ANIMATED GRADIENT BACKGROUND */
    .stApp {
        background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fad0c4, #fbc2eb);
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
        background: rgba(255, 255, 255, 0.4); 
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 2px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
    }

    /* TEXT COLORS */
    h1, h2, h3, p, div, label, span {
        color: #4a4a4a !important; /* Dark Grey for readability */
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    h1 {
        color: #ff4b4b !important; /* Streamlit Red/Pink for Titles */
        text-shadow: 2px 2px 0px #fff;
    }

    /* BUTTON FIX - PURE BLACK TEXT */
    .stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important; /* PURE BLACK TEXT */
        border: 2px solid #000000 !important; /* BLACK BORDER */
        border-radius: 15px;
        padding: 10px 25px;
        font-weight: 900 !important;
        font-size: 16px !important;
        box-shadow: 4px 4px 0px #000000 !important; /* Retro Shadow */
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px #000000 !important;
    }
    
    /* REMOVE HEADER/FOOTER */
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
        st.markdown("### Enter the magic word:")
        password = st.text_input("Password", type="password", placeholder="🐧...", label_visibility="collapsed")
        if st.button("Unlock My Gift ❤️", use_container_width=True):
            if password == "penguin123": 
                st.session_state.authenticated = True
                st.rerun()
            elif password:
                st.error("Wrong password! Are you an imposter? 🤨")
    st.stop() 

# --- MAIN APP ---
st.title("Hey Penguin ❤️")

# Cute GIF at the top
c1, c2, c3 = st.columns([1,2,1])
with c2:
    # Cute bouncing penguin GIF
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Bxd3c5cW55eGZ4ZGd2Y3V4Y2h6eWd5ZmZ5eWd5ZmZ5eWd5ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/1HQHB98Fn0ah2/giphy.gif")

tab1, tab2, tab3 = st.tabs(["🏠 Us", "🍽️ Chef AI", "💌 Vent"])

# --- TAB 1: DASHBOARD ---
with tab1:
    st.markdown("<h3 style='text-align: center;'>Our Love Timeline ⏳</h3>", unsafe_allow_html=True)
    
    start_date = date(2024, 9, 7) 
    today = date.today()
    delta = today - start_date
    
    # Metrics with Emoji Headers
    c1, c2 = st.columns(2)
    c1.info(f"**{delta.days}** Days Together")
    c2.info(f"**{delta.days * 24}** Hours (Approx)")

    st.markdown("---")
    
    # AI GENERATED LOVE NOTE
    st.markdown("### 💌 Daily Note (AI)")
    if "daily_note" not in st.session_state:
        with st.spinner("Writing poetry..."):
            st.session_state.daily_note = get_ai_love_note()
            
    st.success(f"✨ {st.session_state.daily_note}")
    
    if st.button("New Note 🎲", use_container_width=True):
        del st.session_state.daily_note
        st.rerun()

    st.markdown("---")
    st.markdown("### 🎵 Our Jukebox")
    songs = {
        "Mere Bina (Crook)": "https://www.youtube.com/watch?v=f9PKHVesfDc",
        "I Wanna Be Yours (AM)": "https://www.youtube.com/watch?v=nyuo9-OjNNg",
        "Die For You (Weeknd)": "https://www.youtube.com/watch?v=2AH5l-vrY9Q",
        "Take Me to the River": "https://www.youtube.com/watch?v=6ar2VHW1i2w" 
    }
    selected_song = st.selectbox("Pick a vibe:", list(songs.keys()))
    st.video(songs[selected_song])

# --- TAB 2: AI FOOD CHEF ---
with tab2:
    st.markdown("### 👨‍🍳 Chef Shalv AI")
    st.write("Tell me the vibe, and I'll decide the menu.")
    
    vibe = st.select_slider("Mood:", options=["Comfort 🧸", "Spicy 🌶️", "Healthy 🥗", "Fancy 🍷", "Sweet 🍩"])
    
    if st.button("Consult the Chef 🍳", use_container_width=True):
        with st.spinner("Chef is tasting the sauce..."):
            suggestion = get_food_suggestion(vibe)
            st.success(suggestion)
            # Chef Kiss GIF
            st.image("https://media.giphy.com/media/l0MYyDa8S9ghzNebm/giphy.gif", width=200)

# --- TAB 3: VENT & NOTIFY ---
with tab3:
    st.markdown("### 🛡️ Safe Space")
    st.write("I'm listening. Tell me what's wrong.")
    
    reason = st.selectbox("Reason:", 
                          ["I had a bad day at work", "I miss you", "I'm just anxious", "Someone was mean", "I need attention"])
    
    details = st.text_area("Details (Optional):", placeholder="Type it out here...")
    
    if st.button("Send to Shalv 📨", use_container_width=True):
        # 1. Show UI Feedback
        st.warning(f"Message received. I love you, Penguin. ❤️")
        st.video("https://www.youtube.com/watch?v=f9PKHVesfDc")
        
        # 2. Send Notification
        alert_msg = f"🚨 Penguin Alert! Reason: {reason}. Note: {details}"
        send_notification(alert_msg)
        st.toast("He has been notified!", icon="✅")
