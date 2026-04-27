# ============================================================
# 🎬 NETFLIX DASHBOARD - COMPLETE PRO VERSION
# No API needed | Pure Python + Pandas + Plotly
# CSV columns: Title, Type, Genre, Release_Year, Rating, Duration, Country
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600&display=swap');

/* Dark Netflix theme */
html, body, [class*="css"] {
    background-color: #141414;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}
.stApp { background-color: #141414; }

/* Hero banner */
.hero {
    background: linear-gradient(135deg, #E50914 0%, #831010 50%, #141414 100%);
    padding: 2.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    text-align: center;
}
.hero h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    letter-spacing: 4px;
    color: #fff;
    margin: 0;
    text-shadow: 0 4px 20px rgba(0,0,0,0.5);
}
.hero p { color: #ccc; font-size: 1rem; margin-top: 0.5rem; }

/* Metric cards */
.metric-card {
    background: #1f1f1f;
    border: 1px solid #333;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    margin-bottom: 1rem;
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-3px); border-color: #E50914; }
.metric-number { font-family: 'Bebas Neue', sans-serif; font-size: 2.5rem; color: #E50914; }
.metric-label { color: #999; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }

/* Section headers */
.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    color: #E50914;
    letter-spacing: 2px;
    border-left: 4px solid #E50914;
    padding-left: 12px;
    margin: 1.5rem 0 1rem 0;
}

/* Info boxes */
.insight-box {
    background: #1a1a1a;
    border-left: 3px solid #E50914;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.95rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0d0d0d !important;
    border-right: 1px solid #222;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stRadio label { color: #ccc !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background-color: #1a1a1a; border-radius: 8px; }
.stTabs [data-baseweb="tab"] { color: #aaa; }
.stTabs [aria-selected="true"] { color: #E50914 !important; border-bottom: 2px solid #E50914; }

/* Buttons */
.stButton > button {
    background: #E50914;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.5rem 1.5rem;
    transition: all 0.2s;
}
.stButton > button:hover { background: #ff1a1a; transform: scale(1.02); }

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Load & Clean Data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("netflix.csv")
    # Normalize columns
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    # Rename variations
    rename_map = {
        "genre": "listed_in",
        "genres": "listed_in",
        "year": "release_year",
        "name": "title",
    }
    df.rename(columns=rename_map, inplace=True)
    # Duration to numeric
    if "duration" in df.columns:
        df["minutes"] = pd.to_numeric(
            df["duration"].astype(str).str.extract(r"(\d+)")[0], errors="coerce"
        )
    # Rating to numeric if possible
    if "rating" in df.columns:
        df["rating_num"] = pd.to_numeric(df["rating"], errors="coerce")
    return df

df = load_data()

# ── Hero Banner ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🎬 NETFLIX DASHBOARD</h1>
    <p>Explore • Discover • Analyze</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Filters")
    st.markdown("---")

    # Type filter
    if "type" in df.columns:
        all_types = ["All"] + sorted(df["type"].dropna().unique().tolist())
        sel_type = st.selectbox("📺 Content Type", all_types)
    else:
        sel_type = "All"

    # Genre filter
    if "listed_in" in df.columns:
        all_genres = sorted(df["listed_in"].dropna().str.split(", ").explode().unique().tolist())
        sel_genre = st.selectbox("🎭 Genre", ["All"] + all_genres)
    else:
        sel_genre = "All"

    # Country filter
    if "country" in df.columns:
        all_countries = sorted(df["country"].dropna().unique().tolist())
        sel_country = st.selectbox("🌍 Country", ["All"] + all_countries)
    else:
        sel_country = "All"

    # Year filter
    if "release_year" in df.columns:
        min_yr = int(df["release_year"].dropna().min())
        max_yr = int(df["release_year"].dropna().max())
        year_range = st.slider("📅 Release Year", min_yr, max_yr, (min_yr, max_yr))
    else:
        year_range = None

    # Rating filter
    if "rating_num" in df.columns and df["rating_num"].notna().any():
        min_r = float(df["rating_num"].dropna().min())
        max_r = float(df["rating_num"].dropna().max())
        rating_range = st.slider("⭐ Min Rating", min_r, max_r, min_r)
    else:
        rating_range = None

    st.markdown("---")
    st.markdown("### 📊 Dataset Info")
    st.info(f"Total titles: **{len(df)}**\nColumns: **{', '.join(df.columns.tolist())}**")

# ── Apply Filters ─────────────────────────────────────────────────────────────
filtered = df.copy()
if sel_type != "All" and "type" in df.columns:
    filtered = filtered[filtered["type"] == sel_type]
if sel_genre != "All" and "listed_in" in df.columns:
    filtered = filtered[filtered["listed_in"].str.contains(sel_genre, na=False)]
if sel_country != "All" and "country" in df.columns:
    filtered = filtered[filtered["country"] == sel_country]
if year_range and "release_year" in df.columns:
    filtered = filtered[
        (filtered["release_year"] >= year_range[0]) &
        (filtered["release_year"] <= year_range[1])
    ]
if rating_range and "rating_num" in df.columns:
    filtered = filtered[filtered["rating_num"] >= rating_range]

# ── KPI Metrics ───────────────────────────────────────────────────────────────
total   = len(filtered)
movies  = len(filtered[filtered["type"] == "Movie"])  if "type" in filtered.columns else 0
shows   = len(filtered[filtered["type"] == "TV Show"]) if "type" in filtered.columns else 0
avg_dur = int(filtered["minutes"].mean()) if "minutes" in filtered.columns and filtered["minutes"].notna().any() else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-number">{total}</div><div class="metric-label">Total Titles</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-number">{movies}</div><div class="metric-label">Movies</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-number">{shows}</div><div class="metric-label">TV Shows</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-number">{avg_dur if avg_dur else "N/A"}</div><div class="metric-label">Avg Duration (min)</div></div>', unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "📈 Trends",
    "🎬 Recommendations",
    "🔍 Search",
    "📋 Browse All"
])

# Plotly dark theme helper
PLOT_BG = "rgba(0,0,0,0)"
PAPER_BG = "rgba(0,0,0,0)"
FONT_COLOR = "#ffffff"
RED = "#E50914"

def dark_layout(fig, title=""):
    fig.update_layout(
        title=dict(text=title, font=dict(color=FONT_COLOR, size=16)),
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR),
        xaxis=dict(gridcolor="#333", zerolinecolor="#333"),
        yaxis=dict(gridcolor="#333", zerolinecolor="#333"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=FONT_COLOR)),
    )
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">AUTO INSIGHTS</div>', unsafe_allow_html=True)

    # Smart Facts
    insights = []
    if "listed_in" in filtered.columns and len(filtered) > 0:
        top_g = filtered["listed_in"].dropna().str.split(", ").explode().value_counts()
        if len(top_g) > 0:
            insights.append(f"🏆 Sabse popular genre: <b>{top_g.idxmax()}</b> ({top_g.max()} titles)")
    if "country" in filtered.columns and len(filtered) > 0:
        tc = filtered["country"].dropna().value_counts()
        if len(tc) > 0:
            insights.append(f"🌍 Sabse zyada content: <b>{tc.idxmax()}</b> ({tc.max()} titles)")
    if "release_year" in filtered.columns and len(filtered) > 0:
        yr = filtered["release_year"].dropna().value_counts()
        if len(yr) > 0:
            insights.append(f"📅 Peak release year: <b>{int(yr.idxmax())}</b> ({yr.max()} titles)")
    if "rating_num" in filtered.columns and filtered["rating_num"].notna().any():
        avg_r = round(filtered["rating_num"].mean(), 1)
        insights.append(f"⭐ Average rating: <b>{avg_r}</b>")
    if "release_year" in filtered.columns and len(filtered) > 0:
        insights.append(f"🆕 Newest: <b>{int(filtered['release_year'].max())}</b> | 🕰️ Oldest: <b>{int(filtered['release_year'].min())}</b>")

    if insights:
        for i in insights:
            st.markdown(f'<div class="insight-box">{i}</div>', unsafe_allow_html=True)
    else:
        st.warning("Filters se koi data nahi mila. Filters adjust karo.")

    st.markdown("")
    c1, c2 = st.columns(2)

    # Genre bar chart
    with c1:
        st.markdown('<div class="section-title">TOP GENRES</div>', unsafe_allow_html=True)
        if "listed_in" in filtered.columns and len(filtered) > 0:
            gc = filtered["listed_in"].dropna().str.split(", ").explode().value_counts().head(8)
            if len(gc) > 0:
                fig = px.bar(x=gc.values, y=gc.index, orientation="h",
                             color=gc.values, color_continuous_scale=["#831010", "#E50914"],
                             labels={"x": "Count", "y": ""})
                fig.update_layout(coloraxis_showscale=False)
                dark_layout(fig)
                st.plotly_chart(fig, use_container_width=True)

    # Type pie
    with c2:
        st.markdown('<div class="section-title">CONTENT TYPE</div>', unsafe_allow_html=True)
        if "type" in filtered.columns and len(filtered) > 0:
            tc = filtered["type"].value_counts()
            fig2 = px.pie(values=tc.values, names=tc.index,
                          color_discrete_sequence=[RED, "#564d4d", "#888"])
            fig2.update_traces(textfont_color="white")
            dark_layout(fig2)
            st.plotly_chart(fig2, use_container_width=True)

    # Country bar
    if "country" in filtered.columns and len(filtered) > 0:
        st.markdown('<div class="section-title">TOP COUNTRIES</div>', unsafe_allow_html=True)
        cc = filtered["country"].dropna().value_counts().head(10)
        if len(cc) > 0:
            fig3 = px.bar(x=cc.index, y=cc.values, labels={"x": "Country", "y": "Titles"},
                          color=cc.values, color_continuous_scale=["#831010", RED])
            fig3.update_layout(coloraxis_showscale=False)
            dark_layout(fig3)
            st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">CONTENT TRENDS</div>', unsafe_allow_html=True)

    trend_opts = []
    if "release_year" in filtered.columns: trend_opts.append("📅 Releases by Year")
    if "type" in filtered.columns and "release_year" in filtered.columns: trend_opts.append("🎭 Movies vs TV Shows")
    if "listed_in" in filtered.columns: trend_opts.append("🎪 Genre Breakdown")
    if "country" in filtered.columns: trend_opts.append("🌐 Country Distribution")
    if "minutes" in filtered.columns: trend_opts.append("⏱️ Duration Distribution")

    if trend_opts:
        sel_trend = st.selectbox("Trend choose karo:", trend_opts)

        if "Releases by Year" in sel_trend and "release_year" in filtered.columns:
            data = filtered["release_year"].dropna().value_counts().sort_index()
            fig = px.area(x=data.index, y=data.values,
                          labels={"x": "Year", "y": "Titles"},
                          color_discrete_sequence=[RED])
            fig.update_traces(fill="tozeroy", fillcolor="rgba(229,9,20,0.15)", line_color=RED)
            dark_layout(fig, "Releases Per Year")
            st.plotly_chart(fig, use_container_width=True)

        elif "Movies vs TV Shows" in sel_trend:
            data = filtered.groupby(["release_year", "type"]).size().reset_index(name="count")
            fig = px.line(data, x="release_year", y="count", color="type", markers=True,
                          color_discrete_map={"Movie": RED, "TV Show": "#888"})
            dark_layout(fig, "Movies vs TV Shows Over Years")
            st.plotly_chart(fig, use_container_width=True)

        elif "Genre Breakdown" in sel_trend:
            data = filtered["listed_in"].dropna().str.split(", ").explode().value_counts().head(12)
            fig = px.bar(x=data.index, y=data.values,
                         color=data.values, color_continuous_scale=["#831010", RED],
                         labels={"x": "Genre", "y": "Count"})
            fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-35)
            dark_layout(fig, "Genre Distribution")
            st.plotly_chart(fig, use_container_width=True)

        elif "Country Distribution" in sel_trend:
            data = filtered["country"].dropna().value_counts().head(15)
            fig = px.bar(x=data.values, y=data.index, orientation="h",
                         color=data.values, color_continuous_scale=["#831010", RED],
                         labels={"x": "Count", "y": "Country"})
            fig.update_layout(coloraxis_showscale=False)
            dark_layout(fig, "Content by Country")
            st.plotly_chart(fig, use_container_width=True)

        elif "Duration Distribution" in sel_trend:
            dur_data = filtered["minutes"].dropna()
            if len(dur_data) > 0:
                fig = px.histogram(dur_data, nbins=20, color_discrete_sequence=[RED],
                                   labels={"value": "Minutes", "count": "Titles"})
                dark_layout(fig, "Duration Distribution")
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Filtered data mein trend columns nahi hain.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">SMART RECOMMENDATIONS</div>', unsafe_allow_html=True)
    st.caption("Apni pasand batao — best matches nikalenge! 🎯")

    rc1, rc2 = st.columns(2)

    with rc1:
        if "listed_in" in df.columns:
            genre_list = sorted(df["listed_in"].dropna().str.split(", ").explode().unique().tolist())
            rec_genre = st.selectbox("🎭 Favourite Genre", genre_list, key="rec_genre")
        else:
            rec_genre = None

        if "type" in df.columns:
            type_opts = ["Dono chalega"] + sorted(df["type"].dropna().unique().tolist())
            rec_type = st.radio("📺 Type", type_opts, key="rec_type")
        else:
            rec_type = "Dono chalega"

    with rc2:
        if "release_year" in df.columns:
            rmin = int(df["release_year"].dropna().min())
            rmax = int(df["release_year"].dropna().max())
            rec_year = st.slider("📅 Year Range", rmin, rmax, (2010, rmax), key="rec_year")
        else:
            rec_year = None

        if "rating_num" in df.columns and df["rating_num"].notna().any():
            rr_min = float(df["rating_num"].dropna().min())
            rr_max = float(df["rating_num"].dropna().max())
            rec_rating = st.slider("⭐ Min Rating", rr_min, rr_max, rr_min, key="rec_rating")
        else:
            rec_rating = None

    num_rec = st.slider("🔢 Kitne results chahiye?", 1, min(20, len(df)), min(8, len(df)), key="num_rec")

    if st.button("🎯 Recommend Karo!", key="rec_btn"):
        rec_df = df.copy()
        if rec_genre and "listed_in" in rec_df.columns:
            rec_df = rec_df[rec_df["listed_in"].str.contains(rec_genre, na=False)]
        if rec_type != "Dono chalega" and "type" in rec_df.columns:
            rec_df = rec_df[rec_df["type"] == rec_type]
        if rec_year and "release_year" in rec_df.columns:
            rec_df = rec_df[(rec_df["release_year"] >= rec_year[0]) & (rec_df["release_year"] <= rec_year[1])]
        if rec_rating and "rating_num" in rec_df.columns:
            rec_df = rec_df[rec_df["rating_num"] >= rec_rating]

        if len(rec_df) == 0:
            st.warning("⚠️ Koi match nahi mila! Filters thode loose karo.")
        else:
            sample = rec_df.sample(min(num_rec, len(rec_df)))
            st.success(f"🎉 {len(rec_df)} matches mile! Yeh dekho:")
            show_cols = [c for c in ["title","type","listed_in","release_year","rating","duration","country"] if c in sample.columns]
            st.dataframe(sample[show_cols].reset_index(drop=True), use_container_width=True, hide_index=True)

            st.markdown("---")
            if st.button("🎲 Ek Random Pick Karo!"):
                pick = rec_df.sample(1).iloc[0]
                st.balloons()
                title = pick.get("title", "N/A")
                st.markdown(f"## 🎬 Aaj yeh dekho: **{title}**")
                details = []
                for col in ["type","listed_in","release_year","rating","duration","country"]:
                    if col in pick and pd.notna(pick[col]):
                        details.append(f"**{col.title()}:** {pick[col]}")
                st.markdown(" | ".join(details))

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — SEARCH
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">DEEP SEARCH</div>', unsafe_allow_html=True)
    st.caption("Kuch bhi type karo — title, genre, country, director...")

    search_q = st.text_input("🔎", placeholder="e.g. India, Comedy, Thriller, 2020...", label_visibility="collapsed")

    searchable = [c for c in ["title","type","listed_in","country","director","cast"] if c in df.columns]
    search_in  = st.multiselect("Kahan search karein?", searchable, default=searchable[:3])

    if search_q and search_in:
        mask = pd.Series([False] * len(df))
        for col in search_in:
            mask |= df[col].astype(str).str.contains(search_q, case=False, na=False)
        res = df[mask]

        if len(res) == 0:
            st.error(f"❌ '{search_q}' ke liye koi result nahi mila.")
        else:
            st.success(f"✅ **{len(res)} results** mile!")
            show_cols = [c for c in ["title","type","listed_in","release_year","rating","duration","country"] if c in res.columns]
            st.dataframe(res[show_cols].reset_index(drop=True), use_container_width=True, hide_index=True)

            if "listed_in" in res.columns and len(res) > 1:
                st.markdown("#### 🎭 Results mein genre breakdown:")
                gd = res["listed_in"].dropna().str.split(", ").explode().value_counts().head(8)
                fig = px.bar(x=gd.index, y=gd.values, color=gd.values,
                             color_continuous_scale=["#831010", RED],
                             labels={"x": "Genre", "y": "Count"})
                fig.update_layout(coloraxis_showscale=False)
                dark_layout(fig)
                st.plotly_chart(fig, use_container_width=True)
    elif search_q:
        st.warning("Kam se kam ek column select karo.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — BROWSE ALL
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">BROWSE ALL TITLES</div>', unsafe_allow_html=True)
    st.caption(f"Filtered results: **{len(filtered)}** titles")

    # Sort option
    sortable = [c for c in ["title","release_year","rating_num","type"] if c in filtered.columns]
    if sortable:
        sort_col = st.selectbox("Sort by:", sortable)
        sort_asc = st.radio("Order:", ["Ascending ↑", "Descending ↓"], horizontal=True)
        sorted_df = filtered.sort_values(sort_col, ascending=(sort_asc == "Ascending ↑"))
    else:
        sorted_df = filtered

    show_cols = [c for c in ["title","type","listed_in","release_year","rating","duration","country"] if c in sorted_df.columns]
    st.dataframe(sorted_df[show_cols].reset_index(drop=True), use_container_width=True, hide_index=True, height=500)

    # Download button
    csv_data = sorted_df[show_cols].to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Filtered Data as CSV", csv_data, "netflix_filtered.csv", "text/csv")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="text-align:center; color:#555; font-size:0.8rem;">🎬 Netflix Dashboard | Built with Streamlit & Plotly</p>',
    unsafe_allow_html=True
)
