import streamlit as st
import random
import time
import requests
import os
import pandas as pd
import pydeck as pdk
from datetime import date
from openai import AzureOpenAI
import base64
import uuid
from datetime import datetime



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
    if not client: return "Just go to Bhai Ji Shawarma! (AI Offline)"

    # --- 1. CAPYBARA'S TASTE PROFILE ---
    # We explicitly tell the AI what she loves and hates to guide the suggestion.
    her_tastes = (
        "USER PROFILE (CAPYBARA): \n"
        "- LOVES (Sweet): Cheesecake, Nutella Cheesecake Waffle, Biscoff Waffle (The Belgian Waffle Co).\n"
        "- HATES (Sweet): Red Velvet (NEVER suggest this).\n"
        "- LOVES (Savory): 7 Cheese/Mac & Cheese Pizza (La Pino'z), Crispy Paneer Shawarma (Bhai Ji), "
        "Manchurian & Fried Rice (Hong's Kitchen), Mac & Cheese (Social).\n"
        "- PREFERENCE: She likes 'Cheesy', 'Crispy', and 'Spicy' textures."
    )

    # --- 2. DYNAMIC PROMPT LOGIC ---
    if "Sweet" in vibe:
        category = "DESSERT (Cheesecake, Waffles, Chocolate)"
        constraint = "Strictly NO savory items. STRICTLY NO RED VELVET. Suggest something indulgent."
    else:
        category = "SAVORY VEGETARIAN street food/snack"
        constraint = "Ensure it is cheesy, crispy, or spicy. NO sweets."

    try:
        prompt_text = (
            f"Suggest 1 specific {category} near Sector 48 Gurgaon (Sohna Road). "
            f"Cost must be UNDER ₹400. \n"
            f"{her_tastes}\n" # <--- Injecting her profile here
            f"Constraint: {constraint} \n"
            f"Format: 'Dish Name' at 'Restaurant Name' (~Price). "
            f"Add a witty reason why it fits the '{vibe}' vibe."
        )
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a Gurgaon food expert who knows my girlfriend's specific taste buds."},
                {"role": "user", "content": prompt_text}
            ]
        )
        return response.choices[0].message.content
    except:
        return "Just get the Nutella Waffle from Belgian Waffle Co. It never fails."

def upload_voice_to_github(audio_bytes, extension):
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}.{extension}"
    path = f"voice/{filename}"

    url = f"https://api.github.com/repos/{st.secrets['GITHUB_REPO']}/contents/{path}"

    payload = {
        "message": "🎧 New voice note from Capybara",
        "content": base64.b64encode(audio_bytes).decode("utf-8"),
        "branch": st.secrets["GITHUB_BRANCH"]
    }

    headers = {
        "Authorization": f"token {st.secrets['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.put(url, json=payload, headers=headers)

    if response.status_code not in (200, 201):
        raise Exception(f"GitHub upload failed: {response.text}")

    raw_url = (
        f"https://raw.githubusercontent.com/"
        f"{st.secrets['GITHUB_REPO']}/"
        f"{st.secrets['GITHUB_BRANCH']}/"
        f"{path}"
    )

    return raw_url

def get_movie_suggestion(mood, platform, language):
    if not client: return "Watch 'Fifty Shades' or '365 Days' (AI Offline)"
    
    # Handle specific "Spicy" mood context
    if "Sexy" in mood or "Spicy" in mood:
        mood_context = "Erotic, Steamy, High-Chemistry Romance, or Sensual Thriller"
    else:
        mood_context = mood

    # Handle Language Context
    if language == "Any":
        lang_prompt = "Any language (English, Hindi, or Korean preferred)."
    else:
        lang_prompt = f"Strictly in {language} language (or excellent dub)."

    try:
        prompt_text = (
            f"Suggest 1 specific Movie or Web Series available on {platform} (India Region Library). "
            f"The mood/genre is: {mood_context}. "
            f"Language Constraint: {lang_prompt}. "
            f"We are a couple (Shalv and Capybara). "
            f"Give a 1-sentence plot summary and a 1-sentence cheeky/witty reason why we should watch it."
        )
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a movie buff knowing the Indian OTT catalog. You suggest great movies for couples."},
                {"role": "user", "content": prompt_text}
            ]
        )
        return response.choices[0].message.content
    except:
        return "Just watch 'Bridgerton' on Netflix. It hits the spot!"
        



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

    /* ========================= */
    /* 🔥 MOBILE INPUT & DROPDOWN FIX (GREY FIX) */
    /* ========================= */

    :root {
        color-scheme: light !important;
    }

    /* Force Input Boxes to be White with Black Text */
    input, textarea, select {
        background-color: #ffffff !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        caret-color: #000000 !important;
        border: 2px solid #000000 !important;
    }

    /* FORCE THE DROPDOWN MENU TO BE WHITE */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-color: #000000 !important;
    }
    
    /* The Pop-up Menu container */
    div[data-baseweb="popover"], div[data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 2px solid black !important;
    }
    
    /* The individual options in the list */
    div[data-baseweb="option"] {
        background-color: #ffffff !important;
        color: #000000 !important; 
    }
    
    /* Hover effect for options (Pink highlight) */
    div[data-baseweb="option"]:hover {
        background-color: #FFC0CB !important;
        color: #000000 !important;
    }
    
    /* Selected option */
    div[aria-selected="true"] {
        background-color: #FFC0CB !important;
        color: #000000 !important;
    }

    /* Placeholder Text Color */
    ::placeholder {
        color: #555555 !important;
        opacity: 1 !important;
    }

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
            if password.lower() == "capybara": 
                st.session_state.authenticated = True
                st.rerun()
            elif password:
                st.error("Access Denied! 🤨")
    st.stop() 

# --- MAIN APP ---
if "voice_draft" not in st.session_state:
    st.session_state.voice_draft = None


st.markdown('<p class="title-text">My Capybara ❤️</p>', unsafe_allow_html=True)

# UPDATE THIS LINE
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🏠 Us", "🍽️ Food", "🎰 Play", "💌 Vent", "📍 Map", "🎬 Watch"])

# --- TAB 1: DASHBOARD ---
with tab1:
    # GIF: Your Custom US Page GIF
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcTVnOGxnNzIwZG51ZXFocGRtMjljY2g3c2xmc21pc2JhZjNtYWIyOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/yu7xIHQ2UysA7GwoXx/giphy.gif")

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
        "Take Me to the River": "https://www.youtube.com/watch?v=uEKVZQCEBUc" 
    }
    selected_song = st.selectbox("Vibe Check:", list(songs.keys()))
    st.video(songs[selected_song])

# --- TAB 2: STREET FOOD GUIDE ---
with tab2:
    # GIF: Your Custom FOOD Page GIF
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdG5iOXFsdTFyYjMxaXZrMTA0Y2t6amdpN3d2aHdldWUzbTl2MTF1cyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/QKSXTlCRK0r1N2NnkV/giphy.gif")
        
    st.markdown("### 🥟 Street Foodie")
    st.write("Tasty and Near Sector 48 (Under ₹300).")
    vibe = st.select_slider("Mood?", options=["Momos 🥟", "Spicy 🌶️", "Cheesy 🧀", "Desi 🥘", "Sweet 🍩"])
    if st.button("Find Snack 🌯", use_container_width=True):
        with st.spinner("Scanning street stalls..."):
            suggestion = get_food_suggestion(vibe)
            st.success(suggestion)

# --- TAB 3: SPICY SLOTS ---
with tab3:
    # GIF: Your Custom PLAY Page GIF
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnBoNjlieXMxNHFxZjd4YzdxZmh6bHluaWxjY3l1b3hneXJoOTU1ZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/4PbHPdnetp3Pi/giphy.gif")
        
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
    # GIF: Keep existing (Cute Capybara with orange)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.image("https://media.giphy.com/media/Q8OPrlvICzjajupr2T/giphy.gif")
        
    st.markdown("### 🛡️ Safe Space")
    reason = st.selectbox("What's up?", ["Work Stress", "Miss You", "Anxious", "Just Venting"])
    details = st.text_area("Tell me more:", placeholder="...")
    if st.button("Send to Shalv 📨", use_container_width=True):
        st.warning(f"Message sent. I love you.")
        st.video("https://www.youtube.com/watch?v=f9PKHVesfDc")
        send_notification(f"🚨 Capybara Alert! {reason}: {details}")




st.markdown("---")
st.markdown("### 🎙️ Send a Voice Note")

audio_file = st.audio_input("Hold to record")

# Store recording as draft
if audio_file:
    st.session_state.voice_draft = audio_file.getvalue()
    st.success("Voice recorded. Tap Send when ready 💌")

# Only show Send button if a draft exists
if st.session_state.voice_draft:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("❌ Discard", use_container_width=True):
            st.session_state.voice_draft = None
            st.info("Recording discarded")

    with col2:
        if st.button("📤 Send Voice", use_container_width=True):
            with st.spinner("Sending your voice..."):
                raw_url = upload_voice_to_github(
                    st.session_state.voice_draft,
                    "webm"  # or wav if you prefer
                )

                send_notification(
                    f"🎧 New voice note from Capybara 💖\n\n▶️ Listen:\n{raw_url}"
                )

            st.session_state.voice_draft = None
            st.success("Voice note sent 💕")


# --- TAB 5: MAP OF US ---
with tab5:
    # GIF: Your Custom MAP Page GIF
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXJlN2xjc3VyZ3Y4dHNzb29udjkzbXdvYmhkNjUyaGg5NXAydDlrZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/vTfFCC3rSfKco/giphy.gif")

    st.markdown("### 📍 Where it all started")
    
    # 1. Define Data
    map_data = pd.DataFrame({
        'lat': [28.4026, 28.4108, 28.3930],
        'lon': [77.0673, 77.0380, 77.0680],
        'label': ['First Date', 'First Kiss', 'First Meeting'],
        'color': [
            [255, 0, 128, 200],  # Pink (Date)
            [255, 0, 0, 200],    # Red (Kiss)
            [0, 200, 0, 200]     # Green (Meeting)
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




# --- TAB 6: MOVIE SUGGESTER ---
# --- TAB 6: MOVIE SUGGESTER ---
with tab6:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        # Cute GIF of people watching TV
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjVvOWdwZjF2ZXRzaTRsMTB0em8yaXJxcnRwbzVzMmozbzE1enZ2MSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/GYikUbu3p5UdyBhe4r/giphy.gif")

    st.markdown("### 🍿 Movie Night Picker")
    st.write("Can't decide what to watch? Let my chintu sa bot pick.")

    # 3 Columns now: Mood | Language | Platform
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mood = st.selectbox("Current Mood", [
            "Romantic 🥰", 
            "Spicy/Sexy 🌶️", 
            "Comedy 😂", 
            "Thriller/Mystery 🕵️‍♀️", 
            "Horror 👻", 
            "Feel Good ✨", 
            "Cry my eyes out 😭"
        ])
    
    with col2:
        language = st.selectbox("Language", [
            "Any", "English", "Hindi", "Korean", "Spanish"
        ])

    with col3:
        platform = st.selectbox("Platform", [
            "Netflix", "Amazon Prime", "Hotstar", "Any"
        ])

    if st.button("Recommend Something 🎞️", use_container_width=True):
        with st.spinner("Checking Indian libraries..."): 
            # Pass all 3 variables now
            suggestion = get_movie_suggestion(mood, platform, language)
            st.success(suggestion)
            
            # Special effects for romantic/spicy moods
            if "Romantic" in mood or "Sexy" in mood:
                st.balloons()
