# ==============================
# 🤖 AI FEATURES - POWERED BY CLAUDE API
# ==============================
import streamlit as st
import pandas as pd
import requests
import json

# ── Load dataset ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("netflix.csv")
    return df

df = load_data()
filtered_df = df  # Replace with your actual filtered_df if you have sidebar filters

# ── Claude API helper ─────────────────────────────────────────────────────────
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL   = "claude-sonnet-4-20250514"

def ask_claude(system_prompt: str, user_message: str, max_tokens: int = 1024) -> str:
    """Send a message to Claude and return the text response."""
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return "❌ API key nahi mili. Streamlit secrets mein `ANTHROPIC_API_KEY` add karein."

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": CLAUDE_MODEL,
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_message}],
    }
    try:
        resp = requests.post(CLAUDE_API_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]
    except requests.exceptions.HTTPError as e:
        return f"❌ API Error {resp.status_code}: {resp.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ── Dataset summary for context ────────────────────────────────────────────────
def get_dataset_summary(data: pd.DataFrame) -> str:
    """Create a short summary of the dataset to give Claude context."""
    total       = len(data)
    movies      = len(data[data["type"] == "Movie"]) if "type" in data.columns else "N/A"
    shows       = len(data[data["type"] == "TV Show"]) if "type" in data.columns else "N/A"
    top_genres  = (
        data["listed_in"].str.split(", ").explode().value_counts().head(5).index.tolist()
        if "listed_in" in data.columns else []
    )
    top_countries = (
        data["country"].value_counts().head(5).index.tolist()
        if "country" in data.columns else []
    )
    years = (
        f"{int(data['release_year'].min())}–{int(data['release_year'].max())}"
        if "release_year" in data.columns else "N/A"
    )
    return (
        f"Netflix dataset: {total} titles ({movies} Movies, {shows} TV Shows). "
        f"Release years: {years}. "
        f"Top genres: {', '.join(top_genres)}. "
        f"Top countries: {', '.join(top_countries)}."
    )


# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.header("🤖 AI Features")

tab1, tab2, tab3 = st.tabs(["📊 AI Insights", "🎯 Recommendations", "💬 AI Chat"])

dataset_summary = get_dataset_summary(filtered_df)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — AI INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("📊 AI-Powered Data Insights")
    st.caption("Claude aapke Netflix dataset ko analyze karke insights dega.")

    insight_topics = [
        "Content trends aur release patterns",
        "Genre popularity aur diversity",
        "Country-wise content distribution",
        "Rating distribution analysis",
        "Content duration patterns",
    ]

    selected_topic = st.selectbox("🔍 Kis topic pe insight chahiye?", insight_topics)

    if st.button("✨ Insight Generate Karo", key="insight_btn"):
        with st.spinner("Claude analyze kar raha hai..."):
            system = (
                "Tum ek Netflix data analyst ho. User ke dataset ke baare mein "
                "Hindi-English mix (Hinglish) mein clear aur interesting insights do. "
                "Bullet points use karo. Max 250 words."
            )
            user_msg = (
                f"Dataset info: {dataset_summary}\n\n"
                f"Topic: {selected_topic}\n\n"
                "Is topic pe 5 interesting insights do."
            )
            result = ask_claude(system, user_msg)
        st.success("✅ Insight Ready!")
        st.markdown(result)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("🎯 Personalized Recommendations")
    st.caption("Apni pasand batao — Claude best Netflix content suggest karega.")

    col1, col2 = st.columns(2)

    with col1:
        fav_genre = st.selectbox(
            "🎭 Favourite Genre",
            ["Comedy", "Drama", "Thriller", "Horror", "Romance",
             "Action", "Documentary", "Sci-Fi", "Animation", "Crime"],
        )
        content_type = st.radio("📺 Type", ["Movie", "TV Show", "Dono chalega"])

    with col2:
        mood = st.selectbox(
            "😊 Aaj ka Mood",
            ["Chill & Relax", "Adrenaline Rush", "Emotional Feel", 
             "Kuch Sikhna Hai", "Hasna Chahta Hoon", "Mystery Solve Karo"],
        )
        duration_pref = st.radio("⏱️ Time Available", ["Short (< 90 min)", "Long (> 90 min)", "Koi bhi"])

    if st.button("🎬 Recommendations Do!", key="rec_btn"):
        with st.spinner("Claude best picks dhoondh raha hai..."):

            # Build a small sample from the dataset for Claude to pick from
            sample_cols = ["title", "type", "listed_in", "release_year", "rating", "duration"]
            available_cols = [c for c in sample_cols if c in filtered_df.columns]
            sample = filtered_df[available_cols].dropna().sample(min(80, len(filtered_df)), random_state=42)
            sample_str = sample.to_string(index=False)

            system = (
                "Tum ek Netflix recommendation expert ho. "
                "User ki preferences ke basis pe dataset se REAL titles suggest karo. "
                "Hinglish mein jawab do. Har recommendation ke liye title, type, aur 1-line reason batao."
            )
            user_msg = (
                f"User preferences:\n"
                f"- Genre: {fav_genre}\n"
                f"- Type: {content_type}\n"
                f"- Mood: {mood}\n"
                f"- Duration: {duration_pref}\n\n"
                f"Available Netflix titles (sample):\n{sample_str}\n\n"
                "Top 5 recommendations do in titles se. Format: **Title** (Type) — Reason"
            )
            result = ask_claude(system, user_msg, max_tokens=800)

        st.success("🎉 Recommendations Ready!")
        st.markdown(result)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — AI CHATBOT
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("💬 Netflix AI Chatbot")
    st.caption("Netflix dataset ke baare mein kuch bhi poochho!")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Netflix ke baare mein kuch bhi poochho...")

    if user_input:
        # Show user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Build conversation history for Claude
        messages_for_api = []
        for msg in st.session_state.chat_history:
            messages_for_api.append({"role": msg["role"], "content": msg["content"]})

        # Get Claude response
        with st.chat_message("assistant"):
            with st.spinner("Soch raha hoon..."):
                api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
                if not api_key:
                    response_text = "❌ API key nahi mili. Streamlit secrets mein `ANTHROPIC_API_KEY` add karein."
                else:
                    headers = {
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    }
                    system_prompt = (
                        f"Tum ek helpful Netflix data assistant ho. "
                        f"Is dataset ke baare mein jaante ho: {dataset_summary}. "
                        "Hinglish mein friendly jawab do. "
                        "Agar koi cheez dataset mein nahi hai toh honestly bolo."
                    )
                    payload = {
                        "model": CLAUDE_MODEL,
                        "max_tokens": 512,
                        "system": system_prompt,
                        "messages": messages_for_api,
                    }
                    try:
                        resp = requests.post(CLAUDE_API_URL, headers=headers, json=payload, timeout=30)
                        resp.raise_for_status()
                        response_text = resp.json()["content"][0]["text"]
                    except Exception as e:
                        response_text = f"❌ Error: {str(e)}"

            st.markdown(response_text)

        st.session_state.chat_history.append({"role": "assistant", "content": response_text})

    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Chat Clear Karo"):
            st.session_state.chat_history = []
            st.rerun()
