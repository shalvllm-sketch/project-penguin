# import streamlit as st
# import random
# import time
# import requests
# import os
# import pandas as pd
# import pydeck as pdk
# from datetime import date
# from openai import AzureOpenAI
# import base64
# import uuid
# from datetime import datetime
# from youtube_search import YoutubeSearch

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
#     if not client: return "Just go to Bhai Ji Shawarma! (AI Offline)"

#     # --- 1. CAPYBARA'S TASTE PROFILE ---
#     # We explicitly tell the AI what she loves and hates to guide the suggestion.
#     her_tastes = (
#         "USER PROFILE (CAPYBARA): \n"
#         "- LOVES (Sweet): Cheesecake, Nutella Cheesecake Waffle, Biscoff Waffle (The Belgian Waffle Co).\n"
#         "- HATES (Sweet): Red Velvet (NEVER suggest this).\n"
#         "- LOVES (Savory): 7 Cheese/Mac & Cheese Pizza (La Pino'z), Crispy Paneer Shawarma (Bhai Ji), "
#         "Manchurian & Fried Rice (Hong's Kitchen), Mac & Cheese (Social).\n"
#         "- PREFERENCE: She likes 'Cheesy', 'Crispy', and 'Spicy' textures."
#     )

#     # --- 2. DYNAMIC PROMPT LOGIC ---
#     if "Sweet" in vibe:
#         category = "DESSERT (Cheesecake, Waffles, Chocolate)"
#         constraint = "Strictly NO savory items. STRICTLY NO RED VELVET. Suggest something indulgent."
#     else:
#         category = "SAVORY VEGETARIAN street food/snack"
#         constraint = "Ensure it is cheesy, crispy, or spicy. NO sweets."

#     try:
#         prompt_text = (
#             f"Suggest 1 specific {category} near Sector 48 Gurgaon (Sohna Road). "
#             f"Cost must be UNDER ₹400. \n"
#             f"{her_tastes}\n" # <--- Injecting her profile here
#             f"Constraint: {constraint} \n"
#             f"Format: 'Dish Name' at 'Restaurant Name' (~Price). "
#             f"Add a witty reason why it fits the '{vibe}' vibe."
#         )
        
#         response = client.chat.completions.create(
#             model=deployment_name,
#             messages=[
#                 {"role": "system", "content": "You are a Gurgaon food expert who knows my girlfriend's specific taste buds."},
#                 {"role": "user", "content": prompt_text}
#             ]
#         )
#         return response.choices[0].message.content
#     except:
#         return "Just get the Nutella Waffle from Belgian Waffle Co. It never fails."

# def upload_voice_to_github(audio_bytes, extension):
#     filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}.{extension}"
#     path = f"voice/{filename}"

#     url = f"https://api.github.com/repos/{st.secrets['GITHUB_REPO']}/contents/{path}"

#     payload = {
#         "message": "🎧 New voice note from Capybara",
#         "content": base64.b64encode(audio_bytes).decode("utf-8"),
#         "branch": st.secrets["GITHUB_BRANCH"]
#     }

#     headers = {
#         "Authorization": f"token {st.secrets['GITHUB_TOKEN']}",
#         "Accept": "application/vnd.github+json"
#     }

#     response = requests.put(url, json=payload, headers=headers)

#     if response.status_code not in (200, 201):
#         raise Exception(f"GitHub upload failed: {response.text}")

#     raw_url = (
#         f"https://raw.githubusercontent.com/"
#         f"{st.secrets['GITHUB_REPO']}/"
#         f"{st.secrets['GITHUB_BRANCH']}/"
#         f"{path}"
#     )

#     return raw_url

# def get_movie_suggestion(mood, platform, language):
#     if not client: return "Watch 'Fifty Shades' or '365 Days' (AI Offline)"
    
#     # 1. MOOD LOGIC
#     if "Sexy" in mood or "Spicy" in mood:
#         mood_context = "Erotic, Steamy, High-Chemistry Romance, or Sensual Thriller"
#     else:
#         mood_context = mood

#     # 2. LANGUAGE LOGIC
#     if language == "Any":
#         lang_prompt = "Any language (English, Hindi, or Korean preferred)."
#     else:
#         lang_prompt = f"Strictly in {language} language (or excellent dub)."

#     # 3. RANDOM STRATEGY (The Fix for Repetition) 🎲
#     # We pick a random "filter" so the AI doesn't pick the same top movie every time.
#     strategies = [
#         "an underrated hidden gem",
#         "a critically acclaimed masterpiece",
#         "a massive blockbuster hit",
#         "a cult classic",
#         "something released in the last 3 years",
#         "a fan favorite with high IMDB rating"
#     ]
#     selected_strategy = random.choice(strategies)

#     try:
#         prompt_text = (
#             f"Suggest 1 specific Movie or Web Series available on {platform} (India Region Library). "
#             f"The mood is: {mood_context}. "
#             f"Language Constraint: {lang_prompt}. "
#             f"Selection Strategy: Pick {selected_strategy}. " # <--- Forces variety
#             f"We are a couple (Shalv and Capybara). "
#             f"Give a 1-sentence plot summary and a 1-sentence cheeky/witty reason why we should watch it."
#         )
        
#         response = client.chat.completions.create(
#             model=deployment_name,
#             messages=[
#                 {"role": "system", "content": "You are a movie buff knowing the Indian OTT catalog. You suggest diverse movies, not just the most popular ones."},
#                 {"role": "user", "content": prompt_text}
#             ],
#             temperature=0.9  # <--- Increased randomness (0.0 is repetitive, 1.0 is chaotic)
#         )
#         return response.choices[0].message.content
#     except:
#         return "Just watch 'Bridgerton' on Netflix. It hits the spot!"

# def youtube_search(query, limit=5):
#     """
#     Robust YouTube search using multiple Invidious instances (Failover)
#     """
#     # List of public Invidious instances to try
#     instances = [
#         "https://inv.tux.pizza",
#         "https://vid.puffyan.us", 
#         "https://yewtu.be",
#         "https://invidious.drgns.space"
#     ]
    
#     params = {"q": query, "type": "video"}
    
#     for instance in instances:
#         url = f"{instance}/api/v1/search"
#         try:
#             # 6-second timeout to prevent hanging
#             r = requests.get(url, params=params, timeout=6)
            
#             if r.status_code == 200:
#                 data = r.json()
#                 # Verify we actually got a list of videos
#                 if isinstance(data, list) and len(data) > 0:
#                     return data[:limit]
#         except Exception as e:
#             print(f"Error connecting to {instance}: {e}")
#             continue # Try the next server
            
#     return []

# # --- CUSTOM CSS ---
# st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

#     /* DYNAMIC BACKGROUND */
#     .stApp {
#         background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #ffd1ff, #a1c4fd);
#         background-size: 400% 400%;
#         animation: gradient 15s ease infinite;
#     }
#     .stApp::before {
#         content: "";
#         position: absolute;
#         top: 0;
#         left: 0;
#         width: 100%;
#         height: 100%;
#         background-image: url("https://www.transparenttextures.com/patterns/hearts.png");
#         opacity: 0.6;
#         pointer-events: none;
#     }
#     @keyframes gradient {
#         0% { background-position: 0% 50%; }
#         50% { background-position: 100% 50%; }
#         100% { background-position: 0% 50%; }
#     }

#     /* TITLE STYLE */
#     .title-text {
#         font-family: 'Pacifico', cursive;
#         font-size: 60px;
#         color: white;
#         text-align: center;
#         text-shadow: 3px 3px 0px #ff0066, 6px 6px 0px rgba(0,0,0,0.2);
#         margin-bottom: 10px;
#         animation: bounce 2s infinite;
#     }
#     @keyframes bounce {
#         0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
#         40% {transform: translateY(-20px);}
#         60% {transform: translateY(-10px);}
#     }

#     /* BUTTONS */
#     .stButton > button {
#         background-color: #ffffff !important; 
#         color: #000000 !important; 
#         border: 2px solid #000000 !important;
#         border-radius: 12px;
#         padding: 10px 20px;
#         font-weight: 900 !important;
#         text-transform: uppercase;
#         box-shadow: 4px 4px 0px #000000 !important;
#         transition: all 0.2s ease;
#     }
#     .stButton > button:hover {
#         transform: translate(-2px, -2px);
#         box-shadow: 6px 6px 0px #000000 !important;
#         background-color: #ffe6e6 !important;
#     }

#     /* TABS */
#     .stTabs [data-baseweb="tab-panel"] {
#         background: rgba(255, 255, 255, 0.85);
#         backdrop-filter: blur(10px);
#         border-radius: 20px;
#         padding: 25px;
#         border: 2px solid #000;
#         box-shadow: 5px 5px 0px rgba(0,0,0,0.2);
#     }

#     h1, h2, h3 { color: #D63384 !important; text-shadow: 2px 2px 0px #ffffff; font-family: 'Arial Black', sans-serif; }
#     p, div, label, span, li { color: #000000 !important; font-weight: 600; }

#     /* ========================= */
#     /* 🔥 MOBILE INPUT & DROPDOWN FIX (GREY FIX) */
#     /* ========================= */

#     :root {
#         color-scheme: light !important;
#     }

#     /* Force Input Boxes to be White with Black Text */
#     input, textarea, select {
#         background-color: #ffffff !important;
#         color: #000000 !important;
#         -webkit-text-fill-color: #000000 !important;
#         caret-color: #000000 !important;
#         border: 2px solid #000000 !important;
#     }

#     /* FORCE THE DROPDOWN MENU TO BE WHITE */
#     div[data-baseweb="select"] > div {
#         background-color: #ffffff !important;
#         color: #000000 !important;
#         border-color: #000000 !important;
#     }
    
#     /* The Pop-up Menu container */
#     div[data-baseweb="popover"], div[data-baseweb="menu"] {
#         background-color: #ffffff !important;
#         border: 2px solid black !important;
#     }
    
#     /* The individual options in the list */
#     div[data-baseweb="option"] {
#         background-color: #ffffff !important;
#         color: #000000 !important; 
#     }
    
#     /* Hover effect for options (Pink highlight) */
#     div[data-baseweb="option"]:hover {
#         background-color: #FFC0CB !important;
#         color: #000000 !important;
#     }
    
#     /* Selected option */
#     div[aria-selected="true"] {
#         background-color: #FFC0CB !important;
#         color: #000000 !important;
#     }

#     /* Placeholder Text Color */
#     ::placeholder {
#         color: #555555 !important;
#         opacity: 1 !important;
#     }

#     #MainMenu, footer, header {visibility: hidden;}
#     </style>
#     """, unsafe_allow_html=True)

# # --- AUTHENTICATION ---
# if "authenticated" not in st.session_state:
#     st.session_state.authenticated = False

# if not st.session_state.authenticated:
#     st.markdown("<br><br>", unsafe_allow_html=True)
#     st.markdown('<p class="title-text">Locked 🔒</p>', unsafe_allow_html=True)
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
# if "voice_draft" not in st.session_state:
#     st.session_state.voice_draft = None


# st.markdown('<p class="title-text">My Capybara ❤️</p>', unsafe_allow_html=True)

# # UPDATE THIS LINE
# tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🏠 Us", "🍽️ Food", "🎰 Play", "💌 Vent", "📍 Map", "🎬 Watch"])

# # --- TAB 1: DASHBOARD ---
# # --- TAB 1: DASHBOARD ---
# with tab1:
#     # GIF: Your Custom US Page GIF
#     c1, c2, c3 = st.columns([1, 2, 1])
#     with c2:
#         st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcTVnOGxnNzIwZG51ZXFocGRtMjljY2g3c2xmc21pc2JhZjNtYWIyOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/yu7xIHQ2UysA7GwoXx/giphy.gif")

#     st.markdown("### 💑 Our Timeline")
#     start_date = date(2024, 9, 7) 
#     today = date.today()
#     delta = today - start_date
#     c1, c2 = st.columns(2)
#     c1.info(f"**{delta.days}** Days")
#     c2.info(f"**{delta.days * 24}** Hours")
#     st.markdown("---")
    
#     st.markdown("### 📸 Memories")
#     photo_dir = "photos"
#     if os.path.exists(photo_dir) and len(os.listdir(photo_dir)) > 0:
#         images = [f for f in os.listdir(photo_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
#         if images:
#             random_image = random.choice(images)
#             st.image(f"{photo_dir}/{random_image}", caption="Us ❤️")
#             if st.button("Next Pic 🔄", use_container_width=True):
#                 st.rerun()
#     else:
#         st.info("💡 (Upload photos to GitHub to see them here!)")
    
#     st.markdown("---")
#     st.markdown("### 💌 Daily Note")
#     if "daily_note" not in st.session_state:
#         st.session_state.daily_note = get_ai_love_note()  
#     st.success(f"✨ {st.session_state.daily_note}")
#     if st.button("New Note 🎲", use_container_width=True):
#         del st.session_state.daily_note
#         st.rerun()
        
#     st.markdown("---")
    
#     st.markdown("### 🎵 Jukebox")
#     query = st.text_input(
#         "Search a song for your current mood 💗",
#          placeholder="Song name / Artist / Lyrics"
#     )
    
#     if query:
#         with st.spinner("Searching YouTube..."):
#             try:
#                 # Returns a list of dictionaries
#                 results = YoutubeSearch(query, max_results=5).to_dict()
                
#                 if results:
#                     # Creating the dropdown options
#                     # note: this library uses 'id' instead of 'videoId'
#                     options = {
#                         f"{v['title']} — {v['channel']}": f"https://www.youtube.com/watch?v={v['id']}"
#                         for v in results
#                     }
                    
#                     selected = st.selectbox("Pick one 🎶", options.keys())
#                     st.video(options[selected])
#                 else:
#                     st.error("Couldn't find that song 😔 Try another?")
#             except Exception as e:
#                 st.error("Search failed momentarily. Try again!")
#     else:
#         st.caption("💡 Try: 'Tum Se Hi', 'Until I Found You', 'Die For You'")# --- TAB 2: STREET FOOD GUIDE ---
# with tab2:
#     # GIF: Your Custom FOOD Page GIF
#     c1, c2, c3 = st.columns([1,2,1])
#     with c2:
#         st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdG5iOXFsdTFyYjMxaXZrMTA0Y2t6amdpN3d2aHdldWUzbTl2MTF1cyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/QKSXTlCRK0r1N2NnkV/giphy.gif")
        
#     st.markdown("### 🥟 Street Foodie")
#     st.write("Tasty and Near Sector 48 (Under ₹300).")
#     vibe = st.select_slider("Mood?", options=["Momos 🥟", "Spicy 🌶️", "Cheesy 🧀", "Desi 🥘", "Sweet 🍩"])
#     if st.button("Find Snack 🌯", use_container_width=True):
#         with st.spinner("Scanning street stalls..."):
#             suggestion = get_food_suggestion(vibe)
#             st.success(suggestion)

# # --- TAB 3: SPICY SLOTS ---
# with tab3:
#     # GIF: Your Custom PLAY Page GIF
#     c1, c2, c3 = st.columns([1,2,1])
#     with c2:
#         st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnBoNjlieXMxNHFxZjd4YzdxZmh6bHluaWxjY3l1b3hneXJoOTU1ZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/4PbHPdnetp3Pi/giphy.gif")
        
#     st.markdown("### 🎰 Naughty Slots")
#     st.write("Spin to unlock a reward. (18+)")
    
#     spicy_gifts = [
#         "😈 Coupon: I go down on you (No questions asked)",
#         "🧴 Reward: Full Body Oil Massage (30 mins)",
#         "🚿 Reward: Shower Together Voucher",
#         "👙 Reward: You pick my underwear/outfit today",
#         "💋 Reward: 100 Kisses anywhere you want",
#         "👀 Reward: I strip for you (Don't laugh)",
#         "🧞‍♂️ Coupon: One Bedroom 'Wish' (I do anything)",
#         "🍑 Reward: A good hard spanking",
#         "💤 Reward: We sleep naked tonight"
#     ]
    
#     if st.button("SPIN IT! 🎲", use_container_width=True):
#         items = ["😈", "🍑", "🥔", "🫦", "❤️", "🍆"]
#         with st.spinner("Spinning..."):
#             time.sleep(1)
        
#         force_win = False
#         if random.random() < 0.40:
#             force_win = True
            
#         if force_win:
#             a = "😈"
#             b = "😈"
#             c = "❤️" 
#         else:
#             a = random.choice(items)
#             b = random.choice(items)
#             c = random.choice(items)
        
#         st.markdown(f"<h1 style='text-align: center; color: black !important;'>{a} | {b} | {c}</h1>", unsafe_allow_html=True)
        
#         if a == b == c:
#             st.balloons()
#             prize = "🧞‍♂️ JACKPOT: I do ANYTHING you say today."
#             st.success(f"{prize}")
#         elif force_win:
#              st.info("Lucky Spin! 🥈")
#              st.success("🤫 Reward: Roleplay Night (You choose the script)")
#              st.caption("Valid for 24 hours!")
#         elif a == b or b == c or a == c:
#             st.info("Mini Win! 🥈")
#             prize = random.choice(spicy_gifts)
#             st.write(f"You won: **{prize}**")
#         else:
#             st.error("No Match! 😢 But I still love you.")
#             st.write("Spin again baby.")

# # --- TAB 4: VENT ---
# with tab4:
#     # GIF: Keep existing (Cute Capybara with orange)
#     c1, c2, c3 = st.columns([1,2,1])
#     with c2:
#         st.image("https://media.giphy.com/media/Q8OPrlvICzjajupr2T/giphy.gif")
        
#     st.markdown("### 🛡️ Safe Space")
#     reason = st.selectbox("What's up?", ["Work Stress", "Miss You", "Anxious", "Just Venting"])
#     details = st.text_area("Tell me more:", placeholder="...")
#     if st.button("Send to Shalv 📨", use_container_width=True):
#         st.warning(f"Message sent. I love you.")
#         st.video("https://www.youtube.com/watch?v=f9PKHVesfDc")
#         send_notification(f"🚨 Capybara Alert! {reason}: {details}")


# st.markdown("---")
# st.markdown("### 🎙️ Send a Voice Note")

# audio_file = st.audio_input("Hold to record")

# # Store recording as draft
# if audio_file:
#     st.session_state.voice_draft = audio_file.getvalue()
#     st.success("Voice recorded. Tap Send when ready 💌")

# # Only show Send button if a draft exists
# if st.session_state.voice_draft:
#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("❌ Discard", use_container_width=True):
#             st.session_state.voice_draft = None
#             st.info("Recording discarded")

#     with col2:
#         if st.button("📤 Send Voice", use_container_width=True):
#             with st.spinner("Sending your voice..."):
#                 raw_url = upload_voice_to_github(
#                     st.session_state.voice_draft,
#                     "webm"  # or wav if you prefer
#                 )

#                 send_notification(
#                     f"🎧 New voice note from Capybara 💖\n\n▶️ Listen:\n{raw_url}"
#                 )

#             st.session_state.voice_draft = None
#             st.success("Voice note sent 💕")


# # --- TAB 5: MAP OF US ---
# with tab5:
#     # GIF: Your Custom MAP Page GIF
#     c1, c2, c3 = st.columns([1,2,1])
#     with c2:
#         st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXJlN2xjc3VyZ3Y4dHNzb29udjkzbXdvYmhkNjUyaGg5NXAydDlrZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/vTfFCC3rSfKco/giphy.gif")

#     st.markdown("### 📍 Where it all started")
    
#     # 1. Define Data
#     map_data = pd.DataFrame({
#         'lat': [28.4026, 28.4108, 28.3930],
#         'lon': [77.0673, 77.0380, 77.0680],
#         'label': ['First Date', 'First Kiss', 'First Meeting'],
#         'color': [
#             [255, 0, 128, 200],  # Pink (Date)
#             [255, 0, 0, 200],    # Red (Kiss)
#             [0, 200, 0, 200]     # Green (Meeting)
#         ]
#     })
    
#     # 2. Define Layers
#     scatter_layer = pdk.Layer(
#         "ScatterplotLayer",
#         map_data,
#         get_position='[lon, lat]',
#         get_color='color',
#         get_radius=200,
#         pickable=True,
#     )
    
#     text_layer = pdk.Layer(
#         "TextLayer",
#         map_data,
#         get_position='[lon, lat]',
#         get_text='label',
#         get_size=15, 
#         get_color=[0, 0, 0, 255], 
#         get_angle=0,
#         get_text_anchor='"middle"',
#         get_alignment_baseline='"top"'
#     )
    
#     # 3. View State
#     view_state = pdk.ViewState(
#         latitude=28.405,
#         longitude=77.055,
#         zoom=13,
#         pitch=0
#     )
    
#     # 4. Render
#     st.pydeck_chart(pdk.Deck(
#         layers=[scatter_layer, text_layer],
#         initial_view_state=view_state,
#         tooltip={"text": "{label}"}
#     ))
    
#     st.markdown("---")
#     # THE LEGEND
#     st.markdown("### 🗺️ Legend")
#     st.markdown("""
#     <div style='background-color: rgba(255,255,255,0.7); padding: 15px; border-radius: 10px; border: 2px solid black;'>
#         <p style='color: green; margin:0; font-size: 16px;'>🟢 <b>First Meeting:</b> Salescode.ai (M3M Urbana); Where I first was fascinated by your Green Top</p>
#         <br>
#         <p style='color: #D63384; margin:0; font-size: 16px;'>🌸 <b>First Date:</b> Trippy Tequila M3M IFC; Where I realized I like you</p>
#         <br>
#         <p style='color: red; margin:0; font-size: 16px;'>🔴 <b>First Kiss:</b> Parking of Vega Schools; Where I realized I love you</p>
#     </div>
#     """, unsafe_allow_html=True)


# # --- TAB 6: MOVIE SUGGESTER ---
# with tab6:
#     c1, c2, c3 = st.columns([1,2,1])
#     with c2:
#         # Cute GIF of people watching TV
#         st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjVvOWdwZjF2ZXRzaTRsMTB0em8yaXJxcnRwbzVzMmozbzE1enZ2MSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/GYikUbu3p5UdyBhe4r/giphy.gif")

#     st.markdown("### 🍿 Movie Night Picker")
#     st.write("Can't decide what to watch? Let my chintu sa bot pick.")

#     # 3 Columns now: Mood | Language | Platform
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         mood = st.selectbox("Current Mood", [
#             "Romantic 🥰", 
#             "Spicy/Sexy 🌶️", 
#             "Comedy 😂", 
#             "Thriller/Mystery 🕵️‍♀️", 
#             "Horror 👻", 
#             "Feel Good ✨", 
#             "Cry my eyes out 😭"
#         ])
    
#     with col2:
#         language = st.selectbox("Language", [
#             "Any", "English", "Hindi", "Korean", "Spanish"
#         ])

#     with col3:
#         platform = st.selectbox("Platform", [
#             "Netflix", "Amazon Prime", "Hotstar", "Any"
#         ])

#     if st.button("Recommend Something 🎞️", use_container_width=True):
#         with st.spinner("Checking Indian libraries..."): 
#             # Pass all 3 variables now
#             suggestion = get_movie_suggestion(mood, platform, language)
#             st.success(suggestion)
            
#             # Special effects for romantic/spicy moods
#             if "Romantic" in mood or "Sexy" in mood:
#                 st.balloons()
























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
