# ==============================
# 🤖 AI FEATURES (GEMINI)
# ==============================

import google.generativeai as genai
import os

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load model
model = genai.GenerativeModel("gemini-pro")

st.markdown("---")
st.subheader("🤖 AI Features (Gemini)")

# Tabs
tab1, tab2, tab3 = st.tabs(["AI Insights", "Recommendations", "AI Chat"])


# ==============================
# 🔍 AI INSIGHTS
# ==============================
with tab1:
    if st.button("Generate AI Insights"):
        try:
            sample_data = filtered_df.head(20).to_string()

            prompt = f"""
            You are a data analyst.

            Analyze this Netflix dataset:

            {sample_data}

            Give 5 key insights in simple words.
            """

            response = model.generate_content(prompt)
            st.success(response.text)

        except Exception as e:
            st.error(f"Error: {e}")


# ==============================
# 🎯 RECOMMENDATIONS
# ==============================
with tab2:
    genre_input = st.text_input("Enter Genre (Comedy, Drama, Horror)")

    if st.button("Get Recommendations"):
        try:
            prompt = f"Suggest 5 Netflix {genre_input} movies with short description."

            response = model.generate_content(prompt)
            st.success(response.text)

        except Exception as e:
            st.error(f"Error: {e}")


# ==============================
# 💬 AI CHATBOT
# ==============================
with tab3:
    user_q = st.chat_input("Ask anything about Netflix data...")

    if user_q:
        try:
            data_sample = df.head(20).to_string()

            prompt = f"""
            You are a Netflix data assistant.

            Dataset sample:
            {data_sample}

            Question: {user_q}
            """

            response = model.generate_content(prompt)
            st.chat_message("assistant").write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")
