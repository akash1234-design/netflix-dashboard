 ==============================
# 🤖 AI FEATURES (SAFE MODE - NO API)
# ==============================

import streamlit as st
import pandas as pd

# Load dataset (make sure file name correct hai)
df = pd.read_csv("netflix.csv")
filtered_df = df

# UI separator
st.markdown("---")

# Header
st.header("🤖 AI Features")

# Tabs
tab1, tab2, tab3 = st.tabs(["AI Insights", "Recommendations", "AI Chat"])


# ==============================
# 🔍 AI INSIGHTS
# ==============================
with tab1:
    st.warning("⚠️ AI Insights temporarily disabled due to API limit.")
    st.info("You can explore insights manually using charts above.")


# ==============================
# 🎯 RECOMMENDATIONS
# ==============================
with tab2:
    
    st.info("Use filters in dashboard to find content manually.")


# ==============================
# 💬 AI CHATBOT
# ==============================
with tab3:
    st.warning("⚠️ AI Chatbot is temporarily disabled.")
    st.info("This feature will be enabled once API quota is available.")
