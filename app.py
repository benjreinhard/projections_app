import streamlit as st
import pandas as pd
st.set_page_config(layout="wide", page_title="College Baseball Projections")

@st.cache_data
def load_hitters():
    df = pd.read_csv("New folder (2)/2026_d1_hitter_final.csv")
    return df

@st.cache_data
def load_pitchers():
    df = pd.read_csv("New folder (2)/2026_d1_pitcher_final.csv")
    return df

hitters = load_hitters()
pitchers = load_pitchers()

st.title("College Baseball Projection Leaderboards")
tab_hit, tab_pitch = st.tabs(["Hitters", "Pitchers"])

with tab_hit:
    st.subheader("Hitter Projections")
    conf_options = sorted(hitters["Conference"].dropna().unique())
    pos_options = sorted(hitters["Position"].dropna().unique())
    
    conf = st.multiselect("Conference", conf_options, default=conf_options, key="hit_conf")
    pos = st.multiselect("Position", pos_options, default=pos_options, key="hit_pos")
    name = st.text_input("Search Player", key="hit_name")
    
    filtered = hitters.copy()
    if conf:
        filtered = filtered[filtered["Conference"].isin(conf)]
    if pos:
        filtered = filtered[filtered["Position"].isin(pos)]
    if name:
        filtered = filtered[
            filtered["Name"].str.contains(name, case=False, na=False)
        ]
    
    st.dataframe(
        filtered.sort_values("WOBA", ascending=False),
        use_container_width=True
    )

with tab_pitch:
    st.subheader("Pitcher Projections")
    conf_options = sorted(pitchers["Conference"].dropna().unique())
    pos_options = sorted(pitchers["Position"].dropna().unique())
    
    conf = st.multiselect("Conference", conf_options, default=conf_options, key="pitch_conf")
    pos = st.multiselect("Position", pos_options, default=pos_options, key="pitch_pos")
    name = st.text_input("Search Pitcher", key="pitch_name")
    
    filtered = pitchers.copy()
    if conf:
        filtered = filtered[filtered["Conference"].isin(conf)]
    if pos:
        filtered = filtered[filtered["Position"].isin(pos)]
    if name:
        filtered = filtered[
            filtered["Name"].str.contains(name, case=False, na=False)
        ]
    
    st.dataframe(
        filtered.sort_values("FIP+", ascending=False),
        use_container_width=True
    )
