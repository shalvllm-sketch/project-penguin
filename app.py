
import streamlit as st
import random
import time
import requests
import os
import pandas as pd
import pydeck as pdk
from datetime import date, datetime
from openai import AzureOpenAI
import base64
import uuid
import streamlit.components.v1 as components

# --- CONFIGURATION ---
st.set_page_config(page_title="Pookie Dashboard 💖", page_icon="✨", layout="centered")

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

# --- HELPER FUNCTIONS (UPDATED FOR ROMANCE THEME) ---

def plan_trip(destination, start_date, end_date, budget, vibe):
    if not client: return "I'll take you to the moon! (AI Offline)"
    
    days = (end_date - start_date).days + 1
    
    prompt = (
        f"Plan a romantic couple's trip to {destination} for {days} days "
        f"({start_date} to {end_date}). \n"
        f"Total Budget: ₹{budget} (Strict constraint). \n"
        f"Vibe: {vibe}. \n"
        f"Output Guide: \n"
        f"1. Break down costs (Travel, Stay, Food, Activities) to prove it fits the budget.\n"
        f"2. Day-by-day itinerary (Morning, Afternoon, Romantic Evening).\n"
        f"3. Suggest 1 specific romantic hotel/Airbnb within budget.\n"
        f"4. Keep it realistic for an Indian couple traveling from Delhi/Gurgaon."
    )
    
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are an expert travel agent for couples. You plan realistic, budget-friendly, romantic trips."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except:
        return "Let's just go to Goa and figure it out there! 🏖️"

def predict_future(month):
    if not client: return "Outlook good ❤️"
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a funny, romantic fortune teller predicting the future of a couple (Shalv and Capybara). Be witty, slightly roasting Shalv, but ultimately sweet."},
                {"role": "user", "content": f"Predict a specific milestone for us in {month} 2026."}
            ]
        )
        return response.choices[0].message.content
    except:
        return "You will be happy and loved."

def send_notification(message):
    try:
        requests.post("https://ntfy.sh/shalv_penguin_alert", 
                      data=message.encode(encoding='utf-8'))
    except:
        pass

def get_ai_love_note():
    if not client: return "I love you to the moon and back! ❤️ (AI Offline)"
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a romantic boyfriend named Shalv. Write a 1-sentence intense love note for your girlfriend 'Capybara'. Be poetic but modern. Use emojis."},
                {"role": "user", "content": "Write a note for today."}
            ]
        )
        return response.choices[0].message.content
    except:
        return "You are my favorite notification 🌟"

def get_food_suggestion(vibe):
    if not client: return "Hot Chocolate at Starbucks! (AI Offline)"

    # --- CAPYBARA'S TASTE PROFILE ---
    her_tastes = (
        "USER PROFILE (CAPYBARA): \n"
        "- LOVES: Cheesecake, Nutella Waffles, Hot Chocolate, Cheese, Crispy textures.\n"
        "- HATES: Red Velvet.\n"
        "- CONTEXT: A romantic date or comfort food. Suggest places in Gurgaon (Sector 48/Cyber Hub)."
    )

    try:
        prompt_text = (
            f"Suggest 1 specific food treat ({vibe}) near Gurgaon. "
            f"Cost under ₹800. \n"
            f"{her_tastes}\n"
            f"Format: 'Dish Name' at 'Restaurant Name'. Add a romantic reason."
        )
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a Gurgaon food expert helping a boyfriend treat his girl."},
                {"role": "user", "content": prompt_text}
            ]
        )
        return response.choices[0].message.content
    except:
        return "Get the Dark Hot Chocolate from Paul's or Colocal. It's a hug in a mug!"

def upload_voice_to_github(audio_bytes, extension):
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}.{extension}"
    path = f"voice/{filename}"

    url = f"https://api.github.com/repos/{st.secrets['GITHUB_REPO']}/contents/{path}"

    payload = {
        "message": "🎧 New voice note from Capybara (Love Edition)",
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
    if not client: return "Watch 'About Time' or 'Jab We Met' (AI Offline)"
    
    try:
        prompt_text = (
            f"Suggest 1 specific Movie on {platform} (India Library). "
            f"Mood: {mood}. Language: {language}. "
            f"It MUST be perfect for a couple watching on a date night. "
            f"Give a 1-sentence cheeky reason why we should cuddle and watch it."
        )
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a movie buff suggesting movies for a couple."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.9 
        )
        return response.choices[0].message.content
    except:
        return "Just watch 'Yeh Jawaani Hai Deewani'. It's a classic!"

def youtube_search(query, limit=5):
    # Updated list of servers to try
    instances = [
        "https://invidious.projectsegfau.lt",
        "https://inv.tux.pizza",
        "https://yewtu.be", 
        "https://invidious.no-logs.com"
    ]
    
    params = {"q": query, "type": "video"}
    
    for instance in instances:
        try:
            r = requests.get(f"{instance}/api/v1/search", params=params, timeout=2)
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[:limit]
        except:
            continue
            
    # 2. EMERGENCY FALLBACK (UPDATED FOR ROMANCE)
    return [
        {"title": "Ed Sheeran - Perfect", "videoId": "2Vv-BfVoq4g"},
        {"title": "Arijit Singh - Tum Hi Ho", "videoId": "IJq0yyWug1k"},
        {"title": "AP Dhillon - With You", "videoId": "N_Y3J1sJ2Jw"},
        {"title": "Taylor Swift - Lover", "videoId": "-BjZmE2gtdo"},
        {"title": "Diljit Dosanjh - Lover", "videoId": "mHj0W9c8dIQ"}
    ]

# --- CUSTOM CSS (STARS + ROMANCE THEME) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Quicksand:wght@500;700&display=swap');

    /* --- STAR ANIMATION (GOLDEN FLOWING STARS) --- */
    .star {
        color: #FFD700; /* Gold */
        font-size: 1.5em;
        font-family: Arial, sans-serif;
        text-shadow: 0 0 5px #ffeb3b;
        position: fixed;
        top: -10%;
        z-index: 9999;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
        animation-name: star-fall, star-twinkle;
        animation-duration: 12s, 3s;
        animation-timing-function: linear, ease-in-out;
        animation-iteration-count: infinite, infinite;
        animation-play-state: running, running;
        pointer-events: none;
    }
    @keyframes star-fall {
        0% {top: -10%; transform: rotate(0deg);}
        100% {top: 100%; transform: rotate(360deg);}
    }
    @keyframes star-twinkle {
        0% {opacity: 0.8; transform: scale(1);}
        50% {opacity: 0.4; transform: scale(0.8);}
        100% {opacity: 0.8; transform: scale(1);}
    }
    
    /* Randomize star positions */
    .star:nth-of-type(1) {left: 5%; animation-delay: 0s, 0s; font-size: 1em;}
    .star:nth-of-type(2) {left: 15%; animation-delay: 4s, 1s; font-size: 1.8em;}
    .star:nth-of-type(3) {left: 25%; animation-delay: 2s, 0.5s;}
    .star:nth-of-type(4) {left: 40%; animation-delay: 8s, 2s; color: #FFA500;}
    .star:nth-of-type(5) {left: 60%; animation-delay: 6s, 1.5s;}
    .star:nth-of-type(6) {left: 75%; animation-delay: 3s, 2.5s; font-size: 1.2em;}
    .star:nth-of-type(7) {left: 90%; animation-delay: 1s, 3s; color: #FFFACD;}
    
    /* --- ROMANCE THEME BACKGROUND --- */
    .stApp {
        /* Deep Maroon to Romantic Gold Gradient */
        background: linear-gradient(135deg, #2b0c0d 0%, #6d1b1e 40%, #c47679 100%);
        background-attachment: fixed;
    }
    
    /* FONTS & HEADERS */
    h1, h2, h3 { 
        color: #FFD700 !important; /* Gold */
        text-shadow: 2px 2px 0px #3d0000; 
        font-family: 'Dancing Script', cursive;
    }
    
    /* MAIN TITLE STYLE */
    .title-text {
        font-family: 'Dancing Script', cursive;
        font-size: 70px;
        color: #FFD700; 
        text-align: center;
        text-shadow: 3px 3px 0px #3d0000, 0px 0px 10px #ff0000; 
        margin-bottom: 10px;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* --- TABS STYLING --- */
    div[data-baseweb="tab"] > div > div > p {
        color: #FFDDE1 !important; 
        text-shadow: 1px 1px 2px #000000; 
        font-weight: bold;
        font-family: 'Quicksand', sans-serif;
    }

    div[aria-selected="true"] > div > div > p {
        color: #FFD700 !important; /* Gold text for selected */
        text-shadow: 0px 0px 5px #FFD700;
    }
    
    /* CARDS/PANELS */
    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        border: 2px solid #FFD700;
        box-shadow: 0 0 15px rgba(255, 105, 180, 0.4);
    }
    
    /* BUTTONS */
    .stButton > button {
        background-color: #800020 !important; /* Burgundy */
        color: #FFD700 !important; /* Gold Text */
        border: 2px solid #FFD700 !important;
        border-radius: 20px;
        font-family: 'Quicksand', sans-serif;
        font-weight: bold;
        text-transform: uppercase;
        box-shadow: 0px 4px 0px #4a0010 !important;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #a31545 !important;
        transform: translateY(-2px);
        box-shadow: 0px 6px 0px #4a0010 !important;
    }
    .stButton > button:active {
        transform: translateY(2px);
        box-shadow: 0px 0px 0px #4a0010 !important;
    }

    /* GENERAL TEXT INSIDE WHITE BOXES */
    p, div, label, span, li { 
        color: #4a0010; /* Dark Burgundy Text */
        font-family: 'Quicksand', sans-serif;
        font-weight: 600; 
    }
    
    /* INPUT FIELDS */
    input, textarea, select {
        background-color: #fff0f5 !important; /* Lavender Blush */
        color: #4a0010 !important;
        border: 1px solid #800020 !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    
    <div class="star">★</div>
    <div class="star">✨</div>
    <div class="star">★</div>
    <div class="star">✨</div>
    <div class="star">★</div>
    <div class="star">✨</div>
    <div class="star">★</div>
    """, unsafe_allow_html=True)

# --- AUTHENTICATION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<p class="title-text">Welcome Capybara 💖</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.info("This area is restricted to Shalv's favorite person.")
        password = st.text_input("Enter Secret Password", type="password", placeholder="Hint: Who are you?")
        if st.button("Unlock My Heart 🔓", use_container_width=True):
            if password.lower() == "capybara": 
                st.session_state.authenticated = True
                st.rerun()
            elif password:
                st.error("Wrong password, but you're still cute. Try again.")
    st.stop() 

# --- MAIN APP ---
if "voice_draft" not in st.session_state:
    st.session_state.voice_draft = None

st.markdown('<p class="title-text">Hey Beautiful ✨</p>', unsafe_allow_html=True)

# TABS
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["🏠 Us", "🍫 Food", "🎰 Play", "💌 Vent", "📍 Map", "🎬 Movie", "🎁 VAULT", "✈️ Trip", "🔮 Future"])

# --- TAB 1: DASHBOARD ---
with tab1:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        # UPDATED ROMANTIC GIF
        st.image("https://media.giphy.com/media/l4pTfx2qLszoacZRS/giphy.gif") # Cute bear hug or similar

    st.markdown("### 💑 Our Love Timeline")
    
    # --- LIVE TIMER (HTML/JS INJECTION) ---
    timer_html = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@700&display=swap');
        .timer-container {
            background-color: rgba(255, 255, 255, 0.9);
            border: 2px solid #FFD700;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            font-family: 'Quicksand', sans-serif;
            box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
        }
        .timer-text {
            font-size: 24px;
            color: #800020;
            font-weight: bold;
            margin: 0;
        }
        .timer-label {
            font-size: 14px;
            color: #d4af37;
            margin-top: 5px;
            font-weight: bold;
            text-transform: uppercase;
        }
    </style>
    
    <div class="timer-container">
        <div id="timer" class="timer-text">Loading...</div>
        <div class="timer-label">Loving You Since (Sept 7, 2024 • 9:00 PM)</div>
    </div>

    <script>
    var startDate = new Date("September 7, 2024 21:00:00").getTime();

    var x = setInterval(function() {
        var now = new Date().getTime();
        var distance = now - startDate;

        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        document.getElementById("timer").innerHTML = 
            days + "d : " + hours + "h : " + minutes + "m : " + seconds + "s ";
    }, 1000);
    </script>
    """
    components.html(timer_html, height=130)

    st.markdown("---")
    
    st.markdown("### 📸 Us")
    photo_dir = "photos"
    if os.path.exists(photo_dir) and len(os.listdir(photo_dir)) > 0:
        images = [f for f in os.listdir(photo_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        if images:
            random_image = random.choice(images)
            st.image(f"{photo_dir}/{random_image}", caption="My Forever ❤️")
            if st.button("Next Pic 🔄", use_container_width=True):
                st.rerun()
    else:
        st.info("💡 (Upload photos to GitHub to see them here!)")

    st.markdown("---")
    st.markdown("### 💌 Daily Note")
    if "daily_note" not in st.session_state:
        st.session_state.daily_note = get_ai_love_note()  
    st.info(f"📜 {st.session_state.daily_note}")
    if st.button("New Note ✨", use_container_width=True):
        del st.session_state.daily_note
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 🎵 Our Jam")
    query = st.text_input("Play a song for us 🎻", placeholder="Song name / Artist")
    
    if query:
        with st.spinner("DJ Shalv is searching..."):
            results = youtube_search(query, limit=5)
            
            if results:
                options = {f"{v['title']}": f"https://www.youtube.com/watch?v={v['videoId']}" for v in results}
                selected = st.selectbox("Pick one 🎶", options.keys())
                st.video(options[selected])
            else:
                st.error("YouTube is sleepy. Try again later!")
    else:
        st.caption("Try: 'Perfect Ed Sheeran', 'Tum Hi Ho', 'Lover'")

# --- TAB 2: FOOD ---
with tab2:
    st.markdown("### 🍽️ Date Night Menu")
    st.write("What are we craving, my lady?")
    
    vibe = st.select_slider("Craving?", options=["Coffee Date ☕", "Desi Tadka 🍛", "Asian/Ramen 🍜", "Italian/Pizza 🍕", "Sweet Treat 🍰"])
    
    if st.button("Find Place 🍬", use_container_width=True):
        with st.spinner("Checking Zomato (via AI)..."):
            suggestion = get_food_suggestion(vibe)
            st.success(suggestion)
            st.balloons()

# --- TAB 3: NAUGHTY SLOTS (Unchanged but styled) ---
with tab3:
    st.markdown("### 🎰 Date Night Roulette")
    st.caption("Rules: You spin, we do. 🌶️")
    
    if "spin_count" not in st.session_state:
        st.session_state.spin_count = 0
    
    player_turn = st.radio(
        "Who is spinning?",
        ["Her Turn 👩", "His Turn 👨"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # (Keeping your inventory list same as before for brevity)
    naughty_inventory = [
        ("🧊", "SENSORY", "Ice Play: Run an ice cube all over my body."),
        ("🫣", "TEASE", "Blindfold: Put on a blindfold. 5 mins of mystery."),
        ("👙", "VIEW", "Private Strip Tease: Slow and steady."),
        ("👅", "ORAL", "Worship: 5 minutes of oral pleasure."),
        ("🧴", "TOUCH", "Massage: Full body oil massage."),
        ("🤫", "DIRTY", "Whisper: Whisper exactly what you want."),
        ("🐕", "ACTION", "Doggy Style: Deep and hard."),
        ("🤠", "ACTION", "Cowgirl: You're on top."),
        ("🥄", "INTIMATE", "The Finger: You know what to do."),
        ("♋", "MUTUAL", "69: Mutual pleasure."),
        ("🚿", "WET", "Shower Sex: Let's get wet."),
        ("🐇", "QUICK", "The Quickie: Right here, right now."),
        ("🪞", "VIEW", "Vanity: Do it in front of a mirror."),
        ("😈", "DOM", "Yes Sir/Ma'am: Spinner is the Slave."),
        ("👔", "KINK", "Restraint: Tie the Spinner to the bed."),
        ("👋", "IMPACT", "Spanking: 10 solid spanks."),
        ("🦶", "WORSHIP", "Body Worship: Kiss every inch."),
        ("🍆", "ORAL", "Deep Throat: Maintain eye contact."),
        ("🤐", "DENIAL", "Edging: Stop right before the end."),
        ("🃏", "WILD", "Joker Card: Spinner chooses ANY act."),
        ("🎲", "CHANCE", "Roleplay: We are strangers meeting at a bar."),
        ("📸", "RISKY", "The Tape: We film ourselves (and delete later)."),
        ("🤫", "WALK THE TALK", "Tell me a secret fantasy. Then we do it.")
    ]
    
    face_sitting_task = ("👅", "ORAL", "Face Sitting: Don't move until tapped out.")
    
    btn_text = f"SPIN FOR {player_turn.upper()} 🎰"
    
    if st.button(btn_text, use_container_width=True):
        st.session_state.spin_count += 1
        with st.spinner("Rolling..."):
            time.sleep(1.0)
        
        # RIGGED LOGIC (Every 3rd spin)
        if st.session_state.spin_count % 3 == 0:
            selected_task = face_sitting_task
        else:
            selected_task = random.choice(naughty_inventory)
            
        emoji, category, description = selected_task
        
        st.markdown(f"<h1 style='text-align: center; color: #800020 !important; font-size: 60px;'>{emoji} | {emoji} | {emoji}</h1>", unsafe_allow_html=True)
        st.balloons()
        
        with st.container(border=True):
            st.markdown(f"#### 🎯 TARGET: {player_turn.upper()}")
            st.markdown(f"**🔥 CATEGORY:** {category}")
            st.divider() 
            st.markdown(f"## {description}")

# --- TAB 4: VENT & VOICE ---
with tab4:
    st.markdown("### ☁️ Safe Space")
    
    st.write("Vent here. No judgement. Just love.")
    reason = st.selectbox("Topic", ["Miss You", "Had a Bad Day", "Happy News", "Just Grumpy"])
    details = st.text_area("Tell me everything:", placeholder="...")
    
    if st.button("Send to Shalv 📨", use_container_width=True):
        st.success("Sent. I'm reading it now.")
        send_notification(f"🚨 Capybara Vent ({reason}): {details}")

    st.markdown("---")
    
    st.markdown("### 🎙️ Voice Note")
    audio_file = st.audio_input("Record a message")

    if audio_file:
        st.session_state.voice_draft = audio_file.getvalue()
        st.success("Voice recorded. Tap Send when ready 💌")

    if st.session_state.voice_draft:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Discard", use_container_width=True):
                st.session_state.voice_draft = None
                st.rerun()
        with col2:
            if st.button("📤 Send Voice", use_container_width=True):
                with st.spinner("Sending..."):
                    try:
                        raw_url = upload_voice_to_github(st.session_state.voice_draft, "webm")
                        send_notification(f"🎧 New Voice Note from Her 💖\n\n▶️ Listen:\n{raw_url}")
                        st.session_state.voice_draft = None
                        st.success("Sent! 💕")
                    except Exception as e:
                        st.error(f"Failed: {e}")

# --- TAB 5: MAP ---
with tab5:
    st.markdown("### 📍 Our World")
    map_data = pd.DataFrame({
        'lat': [28.4026, 28.4108, 28.3930],
        'lon': [77.0673, 77.0380, 77.0680],
        'label': ['First Date', 'First Kiss', 'First Meeting'],
        'color': [[255, 215, 0, 200], [255, 0, 0, 200], [0, 128, 0, 200]] 
    })
    
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
        get_color=[255, 255, 255, 255], 
        get_angle=0,
        get_text_anchor='"middle"',
        get_alignment_baseline='"top"'
    )
    
    view_state = pdk.ViewState(latitude=28.405, longitude=77.055, zoom=13)
    st.pydeck_chart(pdk.Deck(layers=[scatter_layer, text_layer], initial_view_state=view_state))

# --- TAB 6: MOVIE ---
with tab6:
    st.markdown("### 🎬 Movie Night")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mood = st.selectbox("Vibe", ["Romantic 🥰", "Comfy/Cozy 🧸", "Comedy 😂", "Thriller 😱"])
    with col2:
        language = st.selectbox("Lang", ["English", "Hindi", "Korean"])
    with col3:
        platform = st.selectbox("Where?", ["Netflix", "Prime", "Hotstar", "Any"])
        
    if st.button("Recommend 🍿", use_container_width=True):
        with st.spinner("Consulting the cinema gods..."):
            rec = get_movie_suggestion(mood, platform, language)
            st.success(rec)

# --- TAB 7: VAULT ---
with tab7:
    st.markdown("### 💌 The 'Open When' Vault")
    st.write("Digital letters for when you need me most.")
    
    st.markdown("""
    <style>
    .envelope-btn {
        width: 100%; padding: 20px; background: #FFF0F5;
        border: 2px dashed #800020; border-radius: 10px;
        text-align: center; font-weight: bold; margin-bottom: 10px;
        cursor: pointer; transition: 0.3s;
    }
    .envelope-btn:hover { background: #FFD700; border-color: #000; }
    </style>
    """, unsafe_allow_html=True)
    
    if "opened_letter" not in st.session_state:
        st.session_state.opened_letter = None

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Open when you MISS me 🥺", key="miss"): st.session_state.opened_letter = "miss"
        if st.button("Open when you're MAD 😡", key="mad"): st.session_state.opened_letter = "mad"
        if st.button("Open when you're SAD 😢", key="sad"): st.session_state.opened_letter = "sad"
    with col2:
        if st.button("Open for CONFIDENCE 💃", key="conf"): st.session_state.opened_letter = "conf"
        if st.button("Open on NEW YEAR 🎆", key="ny"): st.session_state.opened_letter = "ny"
        if st.button("Open when HUNGRY 🍟", key="hungry"): st.session_state.opened_letter = "hungry"

    st.markdown("---")
    
    if st.session_state.opened_letter == "miss":
        st.info("💌 **Message:** I am just one call away. Look at our photos. I love you more than code. Call me right now.")
    elif st.session_state.opened_letter == "mad":
        st.warning("💌 **Message:** Okay, I messed up. I'm sorry. I'm an idiot, but I'm YOUR idiot. Let's talk? 🏳️")
        st.image("https://media.giphy.com/media/l1J9PVAZTGx0BvZtK/giphy.gif")
    elif st.session_state.opened_letter == "sad":
        st.success("💌 **Message:** You are the strongest person I know. This will pass. Order a waffle and know I'm hugging you in spirit.")
    elif st.session_state.opened_letter == "conf":
        st.error("💌 **Message:** HAVE YOU SEEN YOURSELF? You are gorgeous. You are smart. You are the main character.")
    elif st.session_state.opened_letter == "ny":
        st.balloons()
        st.markdown("## 🎆 HAPPY NEW YEAR BABY!")
        st.write("My resolution is simple: To make you laugh every single day of 2026.")
    elif st.session_state.opened_letter == "hungry":
        st.info("💌 **Message:** Go to the 'Food' tab! I'm paying (send bill).")

# --- TAB 8: TRIP ---
with tab8:
    st.markdown("### ✈️ Let's Run Away")
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("Where to?", placeholder="Vietnam, Kerala...")
        budget = st.number_input("Budget (₹)", value=50000, step=5000)
    with col2:
        start_d = st.date_input("Start", min_value=date.today())
        end_d = st.date_input("End", min_value=date.today())
        
    vibe = st.select_slider("Trip Vibe?", options=["Lazy 😴", "Romantic 🍷", "Adventure 🧗", "Foodie 🍜"])
    
    if st.button("Plan Our Escape 🌍", use_container_width=True):
        if not destination:
            st.error("Pick a place!")
        else:
            with st.spinner("Planning..."):
                itinerary = plan_trip(destination, start_d, end_d, budget, vibe)
                with st.container(border=True):
                    st.markdown(itinerary)

# --- TAB 9: FUTURE ---
with tab9:
    st.markdown("### 🔮 Oracle of Love")
    month = st.selectbox("Pick a Month in 2026", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    
    if st.button("Reveal Destiny 🧙‍♀️", use_container_width=True):
        with st.spinner("Gazing into the stars..."):
            prediction = predict_future(month)
            st.markdown(f"""
                <div style="background-color: #FFF0F5; border: 2px solid #800020; padding: 20px; border-radius: 15px; text-align: center;">
                    <h3 style="color: #800020 !important;">🔮 {month} 2026 🔮</h3>
                    <p style="font-size: 18px; color: black;">{prediction}</p>
                </div>
                """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<br><hr><center>Made with ❤️ by Shalv for his Capybara</center>", unsafe_allow_html=True)
