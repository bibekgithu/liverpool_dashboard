# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64

# ============================
# LIVERPOOL THEME + PAGE CONFIG
# ============================
st.set_page_config(
    page_title="Liverpool 25/26 Dashboard",
    layout="wide",
    page_icon="🔴",
    initial_sidebar_state="expanded"
)

# Custom Liverpool Styling
st.markdown("""
<style>
.stApp { background-color: #fafafa; }

.title-container {
    padding: 20px;
    background-color: #c8102e;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 20px;
}
.title-container h1 {
    color: white;
    font-size: 45px;
    font-weight: 900;
    letter-spacing: 1px;
}

h2, h3 {
    color: #c8102e;
    font-weight: 700;
}

.css-1d391kg {
    background-color: #c8102e !important;
}
.css-1d391kg * {
    color: white !important;
}

.metric-card {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    border-left: 8px solid #c8102e;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    text-align: center;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)


# ============================
# TITLE
# ============================
st.markdown("""
<div class="title-container">
    <h1>🔴 Liverpool FC 2025/26 Dashboard</h1>
</div>
""", unsafe_allow_html=True)

st.write("""
Welcome to the official **Liverpool FC 2025/26 Season Dashboard**.  
Explore full squad performance, analytics, and detailed player breakdown.
""")


# ============================
# LOAD DATA
# ============================
df = pd.read_csv("data/liverpool_25_26.csv")


# ============================
# SIDEBAR FILTERS
# ============================
st.sidebar.header("⚙️ Filters")

# Search Bar
search_query = st.sidebar.text_input("🔍 Search Player", key="search_player")

# Position filter
positions = df["Pos"].unique()
selected_pos = st.sidebar.multiselect(
    "Select Position",
    positions,
    default=positions,
    key="pos_filter"
)

# Player filter
players = df["Player"].unique()
selected_player = st.sidebar.multiselect(
    "Select Player",
    players,
    default=players,
    key="player_filter"
)

# Filter data
filtered_df = df[
    (df["Pos"].isin(selected_pos)) &
    (df["Player"].isin(selected_player))
]

# Apply search
if search_query:
    filtered_df = filtered_df[
        filtered_df["Player"].str.contains(search_query, case=False)
    ]


# ============================
# TABS
# ============================
tab1, tab2, tab3, tab4 = st.tabs(
    ["📋 Overview", "📊 Charts", "📈 Player Stats", "📥 Download"]
)


# ----------------------------------------------------------------
# TAB 1 — OVERVIEW
# ----------------------------------------------------------------
with tab1:
    st.subheader("📌 Filtered Player Data")
    st.dataframe(filtered_df, use_container_width=True)

    st.subheader("📌 Squad Summary")

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div class="metric-card">
        <h3>⚽ Total Goals</h3>
        <h1>{int(filtered_df["Goals"].sum())}</h1>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="metric-card">
        <h3>🎯 Total Assists</h3>
        <h1>{int(filtered_df["Assists"].sum())}</h1>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="metric-card">
        <h3>⭐ Total Points</h3>
        <h1>{int(filtered_df["Points"].sum())}</h1>
    </div>
    """, unsafe_allow_html=True)


# ----------------------------------------------------------------
# TAB 2 — CHARTS
# ----------------------------------------------------------------
with tab2:
    st.subheader("📊 Goals by Player")
    plt.figure(figsize=(10, 5))
    sns.barplot(data=filtered_df, x="Player", y="Goals", color="#c8102e")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    st.subheader("📊 Assists by Player")
    plt.figure(figsize=(10, 5))
    sns.barplot(data=filtered_df, x="Player", y="Assists", color="#c8102e")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    st.subheader("📊 Points by Player")
    plt.figure(figsize=(10, 5))
    sns.barplot(data=filtered_df, x="Player", y="Points", color="#c8102e")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    st.subheader("📊 Expected Goals (xG) vs Actual Goals")
    plt.figure(figsize=(10,5))
    sns.scatterplot(data=filtered_df, x="xG", y="Goals", hue="Pos", s=100, palette="Reds")
    st.pyplot(plt)

    st.subheader("📊 Expected Assists (xA) vs Actual Assists")
    plt.figure(figsize=(10,5))
    sns.scatterplot(data=filtered_df, x="xA", y="Assists", hue="Pos", s=100, palette="Reds")
    st.pyplot(plt)


# ----------------------------------------------------------------
# TAB 3 — PLAYER STATS
# ----------------------------------------------------------------
with tab3:
    st.subheader("📈 Player Points Trend")
    st.line_chart(filtered_df.set_index("Player")["Points"])


# ----------------------------------------------------------------
# TAB 4 — DOWNLOAD
# ----------------------------------------------------------------
with tab4:
    st.subheader("📥 Download Filtered Data")

    csv = filtered_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()

    st.markdown(
        f'<a href="data:file/csv;base64,{b64}" download="filtered_liverpool.csv">'
        f'⬇ Click to Download CSV</a>',
        unsafe_allow_html=True
    )


# ----------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------
st.markdown("---")
st.write("Dashboard created by **Bibek Poudel** | Liverpool FC ❤️ | YNWA")
