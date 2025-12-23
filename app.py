import streamlit as st
import random
from datetime import date

# --- CONFIGURATION ---
st.set_page_config(page_title="For My Penguin", page_icon="❤️", layout="centered")

# --- AUTHENTICATION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("Login ❤️")
    password = st.text_input("Enter the magic word:", type="password")
    if st.button("Enter"):
        if password == "penguin123": 
            st.session_state.authenticated = True
            st.rerun()
        elif password:
            st.error("Wrong password! Are you really her? 🤨")
    st.stop() 

# --- APP LOGIC ---
st.title("Hey Baby ❤️")

# Create Tabs
tab1, tab2, tab3 = st.tabs(["🏠 Us", "🍔 Food", "💌 Vent"])

# --- TAB 1: RELATIONSHIP STATS & JUKEBOX ---
with tab1:
    st.header("Our Stats")
    
    # DATE CONFIGURATION
    start_date = date(2024, 9, 9) 
    today = date.today()
    delta = today - start_date
    
    col1, col2 = st.columns(2)
    col1.metric("Days Together", f"{delta.days}")
    col2.metric("Hours (Approx)", f"{delta.days * 24}")
    
    st.divider()
    
    # --- NEW: JUKEBOX FEATURE ---
    st.subheader("Our Jukebox 🎵")
    
    # The Playlist
    songs = {
        "Mere Bina (Crook)": "https://www.youtube.com/watch?v=f9PKHVesfDc",
        "I Wanna Be Yours (Arctic Monkeys)": "https://www.youtube.com/watch?v=nyuo9-OjNNg",
        "Die For You (The Weeknd)": "https://www.youtube.com/watch?v=2AH5l-vrY9Q",
        "Take Me to the River (I Will Swim)": "https://www.youtube.com/watch?v=6ar2VHW1i2w" 
    }
    
    # Dropdown menu
    selected_song = st.selectbox("Pick a Vibe:", list(songs.keys()))
    
    # Play the song
    st.video(songs[selected_song])
    
    st.divider()
    st.subheader("Your Daily Reminder:")
    compliments = [
        "You look beautiful today.",
        "I am so lucky to have you.",
        "Don't stress, you got this.",
        "I love your smile."
    ]
    st.info(random.choice(compliments))

# --- TAB 2: DECISION HELPER ---
with tab2:
    st.header("What should we eat?")
    food_options = ["Pizza", "Sushi", "Burgers", "North Indian", "Chinese", "Maggi"]
    
    if st.button("Pick Dinner For Us"):
        choice = random.choice(food_options)
        st.success(f"The Love Bot says: **{choice}**")
        st.balloons()

# --- TAB 3: VENT BOX ---
with tab3:
    st.header("Tell me everything")
    st.write("I might be busy at work, but I'm listening here.")
    
    mood = st.selectbox("How are you feeling?", ["Happy", "Sad", "Angry", "Tired", "Miss You"])
    
    if mood == "Sad":
        st.warning("I'm sorry baby. Remember I'm just a call away.")
        st.write("Listening to this usually helps you...")
        # Auto-plays "Mere Bina" when she is sad
        st.video("https://www.youtube.com/watch?v=f9PKHVesfDc")
        
    elif mood == "Angry":
        st.error("Take a deep breath. Tell me who I need to fight.")
        
    elif mood == "Miss You":
        st.info("I miss you more! See you soon.")
        
    elif mood == "Tired":
        st.write("Go take a nap, you deserve it.")
        
    elif mood == "Happy":
        st.success("Yay! I love seeing you happy!")
        st.balloons()
