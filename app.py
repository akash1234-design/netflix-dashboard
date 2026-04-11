import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt  
st.set_page_config(page_title="Netflix Dashboard", layout="wide")
plt.style.use("dark_background")
st.markdown("""
<style>
/* Full App Background */
.stApp {
    background-color: #0e1117;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111111;
}

/* Titles */
h1, h2, h3 {
    color: #E50914;
    font-weight: bold;
}

/* KPI Cards */
.card {
    background-color: #1c1c1c;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 0px 10px rgba(229,9,20,0.5);
}

/* Metrics Box */
[data-testid="stMetric"] {
    background-color: #1c1c1c;
    padding: 15px;
    border-radius: 10px;
}

/* Download Button */
.stDownloadButton button {
    background-color: #E50914;
    color: white;
    border-radius: 8px;
    border: none;
}

/* Table */
[data-testid="stDataFrame"] {
    background-color: #1c1c1c;
}

</style>
""", unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>🎬 NETFLIX ANALYTICS DASHBOARD</h1>", unsafe_allow_html=True)

# Load Data
df = pd.read_csv("netflix.csv")


# 🔥 ADD THIS LINE
df.columns = df.columns.str.strip().str.lower()
# 🔍 Search
search = st.text_input("Search Title")

if search:
    df = df[df["title"].str.contains(search, case=False, na=False)]

# 🎛️ Sidebar Filters
st.sidebar.header("🔍 Filter Netflix Data")

genre = st.sidebar.selectbox("Genre", ["All"] + list(df["genre"].unique()))
country = st.sidebar.selectbox("Country", ["All"] + list(df["country"].unique()))
type_filter = st.sidebar.selectbox("Type", ["All"] + list(df["type"].unique()))

filtered_df = df.copy()

if genre != "All":
    filtered_df = filtered_df[filtered_df["genre"] == genre]

if country != "All":
    filtered_df = filtered_df[filtered_df["country"] == country]

if type_filter != "All":
    filtered_df = filtered_df[filtered_df["type"] == type_filter]

# 📊 KPIs
st.subheader("📈 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class='card'>
        <h3>Total Titles</h3>
        <h2>{len(filtered_df)}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class='card'>
        <h3>Movies</h3>
        <h2>{len(filtered_df[filtered_df['type']=='Movie'])}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='card'>
        <h3>TV Shows</h3>
        <h2>{len(filtered_df[filtered_df['type']=='TV Show'])}</h2>
    </div>
    """, unsafe_allow_html=True)

# 📥 Download Button
st.download_button(
    label="Download Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_netflix_data.csv",
    mime="text/csv"
)

# 📋 Table
st.dataframe(filtered_df,use_container_width=True)
# 📊 Charts
st.subheader("Genre Distribution")
st.bar_chart(filtered_df["genre"].value_counts())

st.subheader("Ratings Trend")
st.line_chart(filtered_df["rating"])

# 🥧 Pie Chart (using value_counts)
st.subheader("Content Type Distribution")
st.write(filtered_df["type"].value_counts())
# ==============================
# 🤖 AI FEATURES (PASTE AT END)
# ==============================

import openai
openai.api_key = "YOUR_API_KEY"   # <-- apni API key daalo


st.markdown("---")
st.subheader("🤖 AI Features")

# Tabs for clean UI
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

            from openai import OpenAI
            import os

            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            output = response.choices[0].message.content
            st.success(output)

        except Exception as e:
            st.error(f"Error: {e}")


# ==============================
# 🎯 RECOMMENDATIONS
# ==============================
with tab2:
    genre = st.text_input("Enter Genre (Comedy, Drama, Horror)")

    if st.button("Get Recommendations"):
        try:
            prompt = f"Suggest 5 Netflix {genre} movies with short description."

            from openai import OpenAI
            import os

            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            output = response.choices[0].message.content
            st.success(output)

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

            from openai import OpenAI
            import os

            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            output = response.choices[0].message.content
            st.chat_message("assistant").write(output)

        except Exception as e:
            st.error(f"Error: {e}")
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    output = response.choices[0].message.content
    st.write(output)

except Exception as e:
    st.error(f"Error: {e}")
