# import streamlit as st
# import random
# import requests # For notifications
# from datetime import date
# from openai import AzureOpenAI

# # --- CONFIGURATION ---
# st.set_page_config(page_title="For My Penguin", page_icon="🐧", layout="centered")

# # --- AI SETUP ---
# try:
#     client = AzureOpenAI(
#         api_key=st.secrets["AZURE_OPENAI_API_KEY"],
#         api_version=st.secrets["AZURE_OPENAI_VERSION"],
#         azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"]
#     )
#     deployment_name = st.secrets["AZURE_DEPLOYMENT_NAME"]
# except:
#     # If secrets aren't set, we won't crash, just disable AI features gracefully
#     client = None

# # --- HELPER FUNCTIONS ---
# def send_notification(message):
#     try:
#         requests.post("https://ntfy.sh/shalv_penguin_alert", 
#                       data=message.encode(encoding='utf-8'))
#     except:
#         pass

# def get_ai_love_note():
#     if not client: return "I love you more than code! (Add API Key for new poems)"
#     try:
#         response = client.chat.completions.create(
#             model=deployment_name,
#             messages=[
#                 {"role": "system", "content": "You are a romantic boyfriend. Write a 1-sentence witty, cute, and deeply romantic note for your girlfriend 'Penguin'. Use emojis."},
#                 {"role": "user", "content": "Write a note for today."}
#             ]
#         )
#         return response.choices[0].message.content
#     except:
#         return "You are my favorite bug in the system ❤️"

# def get_food_suggestion(vibe):
#     if not client: return "Let's order Pizza! (AI is offline)"
#     try:
#         response = client.chat.completions.create(
#             model=deployment_name,
#             messages=[
#                 {"role": "system", "content": "You are a Michelin star chef. Suggest 1 specific dish based on the vibe. Keep it short and add a 'Chef Kiss' comment."},
#                 {"role": "user", "content": f"The vibe is {vibe}"}
#             ]
#         )
#         return response.choices[0].message.content
#     except:
#         return "Let's just get Maggi. It never fails."

# # --- CUSTOM CSS (VISUALS) ---
# st.markdown("""
#     <style>
#     /* ANIMATED GRADIENT BACKGROUND */
#     .stApp {
#         background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fad0c4, #fbc2eb);
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
#         background: rgba(255, 255, 255, 0.4); 
#         backdrop-filter: blur(10px);
#         border-radius: 20px;
#         padding: 20px;
#         border: 2px solid rgba(255, 255, 255, 0.6);
#         box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
#     }

#     /* TEXT COLORS */
#     h1, h2, h3, p, div, label, span {
#         color: #4a4a4a !important; /* Dark Grey for readability */
#         font-family: 'Helvetica Neue', sans-serif;
#     }
    
#     h1 {
#         color: #ff4b4b !important; /* Streamlit Red/Pink for Titles */
#         text-shadow: 2px 2px 0px #fff;
#     }

#     /* BUTTON FIX - PURE BLACK TEXT */
#     .stButton > button {
#         background-color: #ffffff !important;
#         color: #000000 !important; /* PURE BLACK TEXT */
#         border: 2px solid #000000 !important; /* BLACK BORDER */
#         border-radius: 15px;
#         padding: 10px 25px;
#         font-weight: 900 !important;
#         font-size: 16px !important;
#         box-shadow: 4px 4px 0px #000000 !important; /* Retro Shadow */
#         transition: all 0.2s ease;
#     }
#     .stButton > button:hover {
#         transform: translate(-2px, -2px);
#         box-shadow: 6px 6px 0px #000000 !important;
#     }
    
#     /* REMOVE HEADER/FOOTER */
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
#         st.markdown("### Enter the magic word:")
#         password = st.text_input("Password", type="password", placeholder="🐧...", label_visibility="collapsed")
#         if st.button("Unlock My Gift ❤️", use_container_width=True):
#             if password == "penguin123": 
#                 st.session_state.authenticated = True
#                 st.rerun()
#             elif password:
#                 st.error("Wrong password! Are you an imposter? 🤨")
#     st.stop() 

# # --- MAIN APP ---
# st.title("Hey Penguin ❤️")

# # Cute GIF at the top
# c1, c2, c3 = st.columns([1,2,1])
# with c2:
#     # Cute bouncing penguin GIF
#     st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Bxd3c5cW55eGZ4ZGd2Y3V4Y2h6eWd5ZmZ5eWd5ZmZ5eWd5ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/1HQHB98Fn0ah2/giphy.gif")

# tab1, tab2, tab3 = st.tabs(["🏠 Us", "🍽️ Chef AI", "💌 Vent"])

# # --- TAB 1: DASHBOARD ---
# with tab1:
#     st.markdown("<h3 style='text-align: center;'>Our Love Timeline ⏳</h3>", unsafe_allow_html=True)
    
#     start_date = date(2024, 9, 7) 
#     today = date.today()
#     delta = today - start_date
    
#     # Metrics with Emoji Headers
#     c1, c2 = st.columns(2)
#     c1.info(f"**{delta.days}** Days Together")
#     c2.info(f"**{delta.days * 24}** Hours (Approx)")

#     st.markdown("---")
    
#     # AI GENERATED LOVE NOTE
#     st.markdown("### 💌 Daily Note (AI)")
#     if "daily_note" not in st.session_state:
#         with st.spinner("Writing poetry..."):
#             st.session_state.daily_note = get_ai_love_note()
            
#     st.success(f"✨ {st.session_state.daily_note}")
    
#     if st.button("New Note 🎲", use_container_width=True):
#         del st.session_state.daily_note
#         st.rerun()

#     st.markdown("---")
#     st.markdown("### 🎵 Our Jukebox")
#     songs = {
#         "Mere Bina (Crook)": "https://www.youtube.com/watch?v=f9PKHVesfDc",
#         "I Wanna Be Yours (AM)": "https://www.youtube.com/watch?v=nyuo9-OjNNg",
#         "Die For You (Weeknd)": "https://www.youtube.com/watch?v=2AH5l-vrY9Q",
#         "Take Me to the River": "https://www.youtube.com/watch?v=6ar2VHW1i2w" 
#     }
#     selected_song = st.selectbox("Pick a vibe:", list(songs.keys()))
#     st.video(songs[selected_song])

# # --- TAB 2: AI FOOD CHEF ---
# with tab2:
#     st.markdown("### 👨‍🍳 Chef Shalv AI")
#     st.write("Tell me the vibe, and I'll decide the menu.")
    
#     vibe = st.select_slider("Mood:", options=["Comfort 🧸", "Spicy 🌶️", "Healthy 🥗", "Fancy 🍷", "Sweet 🍩"])
    
#     if st.button("Consult the Chef 🍳", use_container_width=True):
#         with st.spinner("Chef is tasting the sauce..."):
#             suggestion = get_food_suggestion(vibe)
#             st.success(suggestion)
#             # Chef Kiss GIF
#             st.image("https://media.giphy.com/media/l0MYyDa8S9ghzNebm/giphy.gif", width=200)

# # --- TAB 3: VENT & NOTIFY ---
# with tab3:
#     st.markdown("### 🛡️ Safe Space")
#     st.write("I'm listening. Tell me what's wrong.")
    
#     reason = st.selectbox("Reason:", 
#                           ["I had a bad day at work", "I miss you", "I'm just anxious", "Someone was mean", "I need attention"])
    
#     details = st.text_area("Details (Optional):", placeholder="Type it out here...")
    
#     if st.button("Send to Shalv 📨", use_container_width=True):
#         # 1. Show UI Feedback
#         st.warning(f"Message received. I love you, Penguin. ❤️")
#         st.video("https://www.youtube.com/watch?v=f9PKHVesfDc")
        
#         # 2. Send Notification
#         alert_msg = f"🚨 Penguin Alert! Reason: {reason}. Note: {details}"
#         send_notification(alert_msg)
#         st.toast("He has been notified!", icon="✅")












import streamlit as st
import random
import requests
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
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a local Gurgaon food guide. Suggest 1 specific VEGETARIAN dish from a REAL restaurant in Gurgaon. The cost must be UNDER ₹500. Format: 'Dish Name' at 'Restaurant Name' (~Price). Add a short witty reason."},
                {"role": "user", "content": f"Suggest a {vibe} meal."}
            ]
        )
        return response.choices[0].message.content
    except:
        return "Just get Chole Bhature from Civil Lines. It never fails."

def play_story_game(topic):
    if not client: return "Once upon a time... the AI broke. The end."
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a funny storyteller. Write a very short (3 sentences max) funny story about 'Shalv' and 'Capybara' involving the user's topic. Make Shalv look slightly silly and Capybara look smart."},
                {"role": "user", "content": f"Topic: {topic}"}
            ]
        )
        return response.choices[0].message.content
    except:
        return "Error generating story. Try again!"

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* ANIMATED GRADIENT BACKGROUND - Capybara Earth Tones */
    .stApp {
        background: linear-gradient(-45deg, #e0c3fc, #8ec5fc, #90f7ec, #fbc2eb);
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
        background: rgba(255, 255, 255, 0.5); 
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 2px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* TEXT COLORS */
    h1, h2, h3, p, div, label, span {
        color: #2c3e50 !important; /* Dark Blue-Grey for contrast */
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    h1 {
        color: #6c5ce7 !important; /* Purple/Blue Title */
        text-shadow: 2px 2px 0px #fff;
    }

    /* BUTTON FIX - PURE BLACK TEXT & BORDER */
    .stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 800 !important;
        box-shadow: 3px 3px 0px #000000 !important; 
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translate(-2px, -2px);
        box-shadow: 5px 5px 0px #000000 !important;
    }
    
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
            if password.lower() == "capybara123": # <--- UPDATED PASSWORD
                st.session_state.authenticated = True
                st.rerun()
            elif password:
                st.error("Access Denied! Are you really my Capybara? 🤨")
    st.stop() 

# --- MAIN APP ---
st.title("Hey Capybara 🥔")

# Capybara GIF
c1, c2, c3 = st.columns([1,2,1])
with c2:
    st.image("https://media.giphy.com/media/Q8OPrlvICzjajupr2T/giphy.gif")

tab1, tab2, tab3, tab4 = st.tabs(["🏠 Us", "🍽️ Food", "🎮 Play", "💌 Vent"])

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
    st.markdown("### 🥗 Ggn Food Guide")
    st.write("Vegetarian. Under ₹500. Let's go.")
    
    vibe = st.select_slider("Craving?", options=["Comfort 🧸", "Spicy 🌶️", "Healthy 🥗", "Fancy 🍷", "Sweet 🍩"])
    
    if st.button("Find me food 🥘", use_container_width=True):
        with st.spinner("Searching Gurgaon menus..."):
            suggestion = get_food_suggestion(vibe)
            st.success(suggestion)

# --- TAB 3: THE GAME ---
with tab3:
    st.markdown("### 📖 Capybara Tales")
    st.write("Bored? Give me 1 random word, and I'll write a funny story about Us.")
    
    topic = st.text_input("Enter a random object (e.g. Banana, Alien, Sock):")
    
    if st.button("Weave Story 🧶", use_container_width=True):
        if topic:
            with st.spinner("Inventing a story..."):
                story = play_story_game(topic)
                st.info(story)
        else:
            st.warning("Give me a word first!")

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
