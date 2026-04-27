# ==============================
# 🎯 SMART FEATURES - NO AI API NEEDED
# Pure Python + Pandas powered!
# ==============================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Load dataset ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("netflix.csv")
    if "date_added" in df.columns:
        df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
        df["year_added"] = df["date_added"].dt.year
        df["month_added"] = df["date_added"].dt.month
    if "duration" in df.columns:
        df["minutes"] = df["duration"].str.extract(r"(\d+)").astype(float)
    return df

df = load_data()

# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.header("🎯 Smart Features")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Auto Insights",
    "🎬 Recommendations",
    "📈 Trends",
    "🔍 Deep Search"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — AUTO INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("📊 Auto-Generated Insights")
    st.caption("Dataset se automatically nikale gaye interesting facts!")

    total  = len(df)
    movies = len(df[df["type"] == "Movie"])  if "type" in df.columns else 0
    shows  = len(df[df["type"] == "TV Show"]) if "type" in df.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🎬 Total Titles", f"{total:,}")
    c2.metric("🎥 Movies",       f"{movies:,}")
    c3.metric("📺 TV Shows",     f"{shows:,}")
    c4.metric("📊 Movie %",      f"{round(movies/total*100) if total else 0}%")

    st.markdown("---")
    st.markdown("### 🔍 Smart Facts")

    insights = []
    if "listed_in" in df.columns:
        top_genre = df["listed_in"].dropna().str.split(", ").explode().value_counts().idxmax()
        top_count = df["listed_in"].dropna().str.split(", ").explode().value_counts().max()
        insights.append(f"🏆 **Sabse popular genre:** {top_genre} ({top_count} titles)")
    if "country" in df.columns:
        tc = df["country"].dropna().value_counts()
        insights.append(f"🌍 **Sabse zyada content:** {tc.idxmax()} ({tc.max()} titles)")
    if "release_year" in df.columns:
        insights.append(f"📅 **Sabse zyada releases:** {int(df['release_year'].value_counts().idxmax())} mein")
    if "rating" in df.columns:
        insights.append(f"🔞 **Sabse common rating:** {df['rating'].dropna().value_counts().idxmax()}")
    if "minutes" in df.columns:
        avg = df[df["type"]=="Movie"]["minutes"].mean()
        if not pd.isna(avg):
            insights.append(f"⏱️ **Average movie length:** {int(avg)} minutes")
    if "release_year" in df.columns:
        insights.append(f"🆕 **Newest:** {int(df['release_year'].max())} | 🕰️ **Oldest:** {int(df['release_year'].min())}")
    if "year_added" in df.columns:
        insights.append(f"📥 **Sabse zyada content add hua:** {int(df['year_added'].dropna().value_counts().idxmax())} mein")

    for i in insights:
        st.info(i)

    st.markdown("### 🎭 Top 10 Genres")
    if "listed_in" in df.columns:
        gc = df["listed_in"].dropna().str.split(", ").explode().value_counts().head(10)
        fig = px.bar(x=gc.values, y=gc.index, orientation="h",
                     color=gc.values, color_continuous_scale="Reds",
                     labels={"x": "Count", "y": "Genre"})
        fig.update_layout(showlegend=False, coloraxis_showscale=False,
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("🎬 Smart Recommendations")
    st.caption("Apni pasand batao — dataset se best matches nikalenge!")

    col1, col2 = st.columns(2)
    with col1:
        if "listed_in" in df.columns:
            all_genres_list = sorted(df["listed_in"].dropna().str.split(", ").explode().unique().tolist())
            fav_genre = st.selectbox("🎭 Genre", all_genres_list)
        else:
            fav_genre = None
        content_type = st.radio("📺 Type", ["Movie", "TV Show", "Dono"])

    with col2:
        if "rating" in df.columns:
            ratings = ["Koi bhi"] + sorted(df["rating"].dropna().unique().tolist())
            selected_rating = st.selectbox("🔞 Rating", ratings)
        else:
            selected_rating = "Koi bhi"
        if "release_year" in df.columns:
            min_yr = int(df["release_year"].min())
            max_yr = int(df["release_year"].max())
            year_range = st.slider("📅 Year Range", min_yr, max_yr, (2015, max_yr))
        else:
            year_range = None

    num_results = st.slider("🔢 Kitne results?", 5, 20, 10)

    if st.button("🎯 Recommend Karo!", key="rec_btn"):
        filtered = df.copy()
        if fav_genre and "listed_in" in df.columns:
            filtered = filtered[filtered["listed_in"].str.contains(fav_genre, na=False)]
        if content_type != "Dono" and "type" in df.columns:
            filtered = filtered[filtered["type"] == content_type]
        if selected_rating != "Koi bhi" and "rating" in df.columns:
            filtered = filtered[filtered["rating"] == selected_rating]
        if year_range and "release_year" in df.columns:
            filtered = filtered[(filtered["release_year"] >= year_range[0]) & (filtered["release_year"] <= year_range[1])]

        if len(filtered) == 0:
            st.warning("⚠️ Koi match nahi mila! Filters thode loose karo.")
        else:
            sample = filtered.sample(min(num_results, len(filtered)))
            st.success(f"✅ {len(filtered)} matches mile! Top {len(sample)} dikh rahe hain:")
            show_cols = [c for c in ["title","type","listed_in","release_year","rating","duration","country"] if c in sample.columns]
            st.dataframe(sample[show_cols].reset_index(drop=True), use_container_width=True, hide_index=True)

        if st.button("🎲 Ek Random Pick!"):
            pick = filtered.sample(1).iloc[0]
            st.balloons()
            st.markdown(f"### 🎉 Aaj dekho: **{pick.get('title','N/A')}**")
            if "description" in pick:
                st.caption(pick["description"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("📈 Netflix Content Trends")

    trend_option = st.selectbox("Kaunsa trend?", [
        "Content Added Per Year",
        "Movies vs TV Shows Over Years",
        "Top 10 Countries",
        "Rating Distribution",
        "Top Directors",
    ])

    if trend_option == "Content Added Per Year" and "year_added" in df.columns:
        data = df["year_added"].dropna().value_counts().sort_index()
        fig = px.line(x=data.index, y=data.values, markers=True,
                      labels={"x":"Year","y":"Titles Added"}, title="Content Added Per Year")
        fig.update_traces(line_color="#E50914", line_width=3)
        st.plotly_chart(fig, use_container_width=True)

    elif trend_option == "Movies vs TV Shows Over Years" and "release_year" in df.columns:
        data = df.groupby(["release_year","type"]).size().reset_index(name="count")
        fig = px.line(data, x="release_year", y="count", color="type", markers=True,
                      title="Movies vs TV Shows Over Years",
                      color_discrete_map={"Movie":"#E50914","TV Show":"#564d4d"})
        st.plotly_chart(fig, use_container_width=True)

    elif trend_option == "Top 10 Countries" and "country" in df.columns:
        data = df["country"].dropna().value_counts().head(10)
        fig = px.bar(x=data.index, y=data.values, labels={"x":"Country","y":"Titles"},
                     title="Top 10 Countries", color=data.values, color_continuous_scale="Reds")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    elif trend_option == "Rating Distribution" and "rating" in df.columns:
        data = df["rating"].dropna().value_counts()
        fig = px.pie(values=data.values, names=data.index, title="Rating Distribution",
                     color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig, use_container_width=True)

    elif trend_option == "Top Directors" and "director" in df.columns:
        data = df["director"].dropna().value_counts().head(10)
        fig = px.bar(x=data.values, y=data.index, orientation="h",
                     labels={"x":"Titles","y":"Director"}, title="Top 10 Directors",
                     color=data.values, color_continuous_scale="Reds")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Yeh column dataset mein nahi hai.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — DEEP SEARCH
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("🔍 Deep Search")
    st.caption("Title, director, actor — kuch bhi search karo!")

    search_query = st.text_input("🔎 Kuch bhi type karo...", placeholder="e.g. Shah Rukh, Comedy, 2020...")
    search_in = st.multiselect(
        "Kahan search karein?",
        options=[c for c in ["title","director","cast","listed_in","description","country"] if c in df.columns],
        default=[c for c in ["title","director","cast"] if c in df.columns]
    )

    if search_query and search_in:
        mask = pd.Series([False] * len(df))
        for col in search_in:
            mask |= df[col].astype(str).str.contains(search_query, case=False, na=False)
        results = df[mask]
        st.success(f"✅ **{len(results)} results** mile '{search_query}' ke liye!")
        show_cols = [c for c in ["title","type","director","cast","release_year","rating","listed_in"] if c in results.columns]
        st.dataframe(results[show_cols].reset_index(drop=True), use_container_width=True, hide_index=True)

        if len(results) > 0 and "listed_in" in results.columns:
            st.markdown("#### 🎭 In results mein genres:")
            gd = results["listed_in"].dropna().str.split(", ").explode().value_counts().head(8)
            fig = px.bar(x=gd.index, y=gd.values, color=gd.values,
                         color_continuous_scale="Reds", labels={"x":"Genre","y":"Count"})
            fig.update_layout(coloraxis_showscale=False,
                              plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
    elif search_query:
        st.warning("Kam se kam ek column select karo.")
