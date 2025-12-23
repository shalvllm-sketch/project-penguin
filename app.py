# import streamlit as st
# import random
# import time
# import requests
# from datetime import date
# from openai import AzureOpenAI

# # --- CONFIGURATION ---
# st.set_page_config(page_title="For My Capybara", page_icon="🥔", layout="centered")

# # --- AI SETUP ---
# try:
#     client = AzureOpenAI(
#         api_key=st.secrets["AZURE_OPENAI_API_KEY"],
#         api_version=st.secrets["AZURE_OPENAI_VERSION"],
#         azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"]
#     )
#     deployment_name = st.secrets["AZURE_DEPLOYMENT_NAME"]
# except:
#     client = None

# # --- HELPER FUNCTIONS ---
# def send_notification(message):
#     try:
#         requests.post("https://ntfy.sh/shalv_penguin_alert", 
#                       data=message.encode(encoding='utf-8'))
#     except:
#         pass

# def get_ai_love_note():
#     if not client: return "I love you more than code! (AI Offline)"
#     try:
#         response = client.chat.completions.create(
#             model=deployment_name,
#             messages=[
#                 {"role": "system", "content": "You are a romantic boyfriend named Shalv. Write a 1-sentence witty, cute love note for your girlfriend 'Capybara'. Use emojis."},
#                 {"role": "user", "content": "Write a note for today."}
#             ]
#         )
#         return response.choices[0].message.content
#     except:
#         return "You are my favorite notification ❤️"

# def get_food_suggestion(vibe):
#     if not client: return "Order Domino's! (AI Offline)"
#     try:
#         # UPDATED PROMPT: Sector 48 Vicinity
#         prompt_text = f"Suggest 1 specific VEGETARIAN dish from a REAL restaurant near Sector 48 Gurgaon (within 45 mins drive). Cost must be UNDER ₹300. Format: 'Dish Name' at 'Restaurant Name' (~Price). Add a short witty reason why it fits the '{vibe}' vibe."
        
#         response = client.chat.completions.create(
#             model=deployment_name,
#             messages=[
#                 {"role": "system", "content": "You are a local Gurgaon food guide. You know the best hidden gems near Sector 48, Sohna Road, and Nirvana Country."},
#                 {"role": "user", "content": prompt_text}
#             ]
#         )
#         return response.choices[0].message.content
#     except:
#         return "Just get Chole Bhature from Civil Lines. It never fails."

# # --- CUSTOM CSS ---
# st.markdown("""
#     <style>
#     /* ANIMATED GRADIENT BACKGROUND */
#     .stApp {
#         background: linear-gradient(-45deg, #FF9A8B, #FF6A88, #FF99AC, #FFB199);
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
#         background: rgba(255, 255, 255, 0.6); 
#         backdrop-filter: blur(12px);
#         border-radius: 20px;
#         padding: 20px;
#         border: 2px solid rgba(255, 255, 255, 0.9);
#         box-shadow: 0 4px 15px rgba(0,0,0,0.05);
#     }

#     /* TEXT COLORS */
#     h1, h2, h3, p, div, label, span {
#         color: #4a4a4a !important; 
#         font-family: 'Helvetica Neue', sans-serif;
#     }
#     h1 {
#         color: #D63384 !important; /* Hot Pink Title */
#         text-shadow: 2px 2px 0px #fff;
#     }

#     /* BUTTON FIX - BLACK TEXT */
#     .stButton > button {
#         background-color: #ffffff !important;
#         color: #000000 !important;
#         border: 2px solid #000000 !important;
#         border-radius: 12px;
#         padding: 10px 20px;
#         font-weight: 800 !important;
#         box-shadow: 3px 3px 0px #000000 !important; 
#         transition: all 0.2s ease;
#     }
#     .stButton > button:hover {
#         transform: translate(-2px, -2px);
#         box-shadow: 5px 5px 0px #000000 !important;
#     }
    
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
#         st.write("Password hint: What do I call you?")
#         password = st.text_input("Password", type="password", label_visibility="collapsed")
#         if st.button("Unlock ❤️", use_container_width=True):
#             if password.lower() == "capybara": 
#                 st.session_state.authenticated = True
#                 st.rerun()
#             elif password:
#                 st.error("Access Denied! 🤨")
#     st.stop() 

# # --- MAIN APP ---
# st.title("Hey Capybara 🥔")

# # Capybara GIF
# c1, c2, c3 = st.columns([1,2,1])
# with c2:
#     st.image("https://media.giphy.com/media/Q8OPrlvICzjajupr2T/giphy.gif")

# tab1, tab2, tab3, tab4 = st.tabs(["🏠 Us", "🍽️ Food", "🎰 Play", "💌 Vent"])

# # --- TAB 1: DASHBOARD ---
# with tab1:
#     st.markdown("### 💑 Our Timeline")
#     start_date = date(2024, 9, 7) 
#     today = date.today()
#     delta = today - start_date
    
#     c1, c2 = st.columns(2)
#     c1.info(f"**{delta.days}** Days")
#     c2.info(f"**{delta.days * 24}** Hours")

#     st.markdown("---")
    
#     st.markdown("### 💌 Daily Note")
#     if "daily_note" not in st.session_state:
#         with st.spinner("Writing..."):
#             st.session_state.daily_note = get_ai_love_note()
            
#     st.success(f"✨ {st.session_state.daily_note}")
#     if st.button("New Note 🎲", use_container_width=True):
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
#     selected_song = st.selectbox("Vibe Check:", list(songs.keys()))
#     st.video(songs[selected_song])

# # --- TAB 2: GURGAON CHEF ---
# with tab2:
#     st.markdown("### 🥗 Sector 48 Foodie")
#     st.write("Vegetarian. Under ₹500. Near You.")
    
#     vibe = st.select_slider("Craving?", options=["Comfort 🧸", "Spicy 🌶️", "Healthy 🥗", "Fancy 🍷", "Sweet 🍩"])
    
#     if st.button("Find me food 🥘", use_container_width=True):
#         with st.spinner("Searching Sector 48..."):
#             suggestion = get_food_suggestion(vibe)
#             st.success(suggestion)

# # --- TAB 3: THE SLOT MACHINE GAME (18+) ---
# with tab3:
#     st.markdown("### 🎰 Naughty Slots")
#     st.write("Spin to win a prize. Disclaimer: 18+ 😉")
    
#     if st.button("SPIN IT! 🎲", use_container_width=True):
#         # The items in the slot machine
#         items = ["😈", "🍑", "🥔", "🫦", "❤️"]
        
#         # Spin animation (fake delay)
#         with st.spinner("Spinning..."):
#             time.sleep(1)
        
#         # Random selection
#         a = random.choice(items)
#         b = random.choice(items)
#         c = random.choice(items)
        
#         # Display the result big
#         st.markdown(f"<h1 style='text-align: center; color: black !important;'>{a} | {b} | {c}</h1>", unsafe_allow_html=True)
        
#         # Winning Logic
#         if a == b == c:
#             st.balloons()
#             st.success("JACKPOT! 🫦🫦🫦 Reward: Bedroom 'Yes' Day (I do whatever you say) 😈")
#             st.markdown("*Screenshot this coupon immediately!*")
            
#         elif a == b or b == c or a == c:
#             st.info("So close! Reward: Sensual Body Massage (Oil included) 🧴")
            
#         elif "❤️" in [a, b, c]:
#             st.success("You found a heart! Reward: 10 mins of Neck Kisses 💋")
            
#         else:
#             st.warning("No match! But you can strip... I mean, spin again. 😉")

# # --- TAB 4: VENT ---
# with tab4:
#     st.markdown("### 🛡️ Safe Space")
#     reason = st.selectbox("What's up?", ["Work Stress", "Miss You", "Anxious", "Just Venting"])
#     details = st.text_area("Tell me more:", placeholder="...")
    
#     if st.button("Send to Shalv 📨", use_container_width=True):
#         st.warning(f"I hear you. Sending a virtual hug.")
#         st.video("https://www.youtube.com/watch?v=f9PKHVesfDc")
#         send_notification(f"🚨 Capybara Alert! {reason}: {details}")
#         st.toast("Shalv notified!", icon="✅")











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
        # UPDATED PROMPT: Sector 48 Vicinity
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

# --- CUSTOM CSS (RESTORED DYNAMIC COLORS) ---
st.markdown("""
    <style>
    /* RESTORED: The Brilliant Dynamic Gradient */
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
        background: rgba(255, 255, 255, 0.25); 
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }

    /* TEXT COLORS - High Contrast */
    h1, h2, h3 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        font-family: 'Helvetica Neue', sans-serif;
    }
    p, div, label, span {
        color: white !important;
        font-weight: 500;
    }

    /* BUTTON FIX - BLACK TEXT */
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
    
    # --- NEW: PHOTO GALLERY FEATURE ---
    st.markdown("### 📸 Memory Lane")
    
    # Logic to pick random photo
    photo_dir = "photos"
    if os.path.exists(photo_dir) and len(os.listdir(photo_dir)) > 0:
        # Get all image files
        images = [f for f in os.listdir(photo_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        if images:
            random_image = random.choice(images)
            st.image(f"{photo_dir}/{random_image}", caption="Look at us! ❤️")
            if st.button("Another Memory 🔄", use_container_width=True):
                st.rerun()
        else:
            st.warning("No images found in 'photos' folder!")
    else:
        st.info("💡 Upload photos to a 'photos' folder in GitHub to see them here!")

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
    st.write("Spin to win a prize. Disclaimer: 18+ 😉")
    
    if st.button("SPIN IT! 🎲", use_container_width=True):
        items = ["😈", "🍑", "🥔", "🫦", "❤️"]
        
        with st.spinner("Spinning..."):
            time.sleep(1)
        
        a = random.choice(items)
        b = random.choice(items)
        c = random.choice(items)
        
        st.markdown(f"<h1 style='text-align: center; color: white !important;'>{a} | {b} | {c}</h1>", unsafe_allow_html=True)
        
        if a == b == c:
            st.balloons()
            st.success("JACKPOT! 🫦🫦🫦 Reward: Bedroom 'Yes' Day (I do whatever you say) 😈")
            st.markdown("*Screenshot this coupon immediately!*")
        elif a == b or b == c or a == c:
            st.info("So close! Reward: Sensual Body Massage (Oil included) 🧴")
        elif "❤️" in [a, b, c]:
            st.success("You found a heart! Reward: 10 mins of Neck Kisses 💋")
        else:
            st.warning("No match! But you can strip... I mean, spin again. 😉")

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







