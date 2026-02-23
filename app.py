import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="College Baseball Projections")

DIV_FILES = {
    "D1": {
        "hitters": "New folder (2)/2026_d1_hitter_final.csv",
        "pitchers": "New folder (2)/2026_d1_pitcher_final.csv",
    },
    "D2": {
        "hitters": "New folder (2)/2026_d2_hitter_final.csv",
        "pitchers": "New folder (2)/2026_d2_pitcher_final.csv",
    },
    "D3": {
        "hitters": "New folder (2)/2026_d3_hitter_final.csv",
        "pitchers": "New folder (2)/2026_d3_pitcher_final.csv",
    },
}

division = st.selectbox("Division", list(DIV_FILES.keys()), index=0)

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

hitters = load_csv(DIV_FILES[division]["hitters"])
pitchers = load_csv(DIV_FILES[division]["pitchers"])

st.title("College Baseball Projection Leaderboards")
tab_hit, tab_pitch = st.tabs(["Hitters", "Pitchers"])

with tab_hit:
    st.subheader("Hitter Projections")
    conf_options = sorted(hitters["Conference"].dropna().unique())
    pos_options = sorted(hitters["Position"].dropna().unique())

    conf = st.multiselect(
        "Conference",
        conf_options,
        default=conf_options,
        key=f"hit_conf_{division}",
    )
    pos = st.multiselect(
        "Position",
        pos_options,
        default=pos_options,
        key=f"hit_pos_{division}",
    )
    name = st.text_input("Search Player", key=f"hit_name_{division}")

    filtered = hitters.copy()
    if conf:
        filtered = filtered[filtered["Conference"].isin(conf)]
    if pos:
        filtered = filtered[filtered["Position"].isin(pos)]
    if name:
        filtered = filtered[filtered["Name"].str.contains(name, case=False, na=False)]

    st.dataframe(
        filtered.sort_values("WOBA", ascending=False),
        use_container_width=True,
    )

with tab_pitch:
    st.subheader("Pitcher Projections")
    conf_options = sorted(pitchers["Conference"].dropna().unique())
    pos_options = sorted(pitchers["Position"].dropna().unique())

    conf = st.multiselect(
        "Conference",
        conf_options,
        default=conf_options,
        key=f"pitch_conf_{division}",
    )
    pos = st.multiselect(
        "Position",
        pos_options,
        default=pos_options,
        key=f"pitch_pos_{division}",
    )
    name = st.text_input("Search Pitcher", key=f"pitch_name_{division}")

    filtered = pitchers.copy()
    if conf:
        filtered = filtered[filtered["Conference"].isin(conf)]
    if pos:
        filtered = filtered[filtered["Position"].isin(pos)]
    if name:
        filtered = filtered[filtered["Name"].str.contains(name, case=False, na=False)]

    st.dataframe(
        filtered.sort_values("FIP+", ascending=False),
        use_container_width=True,
    )
