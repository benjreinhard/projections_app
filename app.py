
# source streamlit_env/bin/activate
# streamlit run app.py
#  streamlit run ~/Desktop/college_baseball_projections/app.py
# pip install streamlit altair pandas numpy

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(layout="wide", page_title="College Baseball Projections")
np.random.seed(42)

players = [f"Player {c}" for c in list("ABCDEFGHIJK")]
teams = ["Minnesota", "LSU", "UNC"]
confs = ["Big Ten", "SEC", "ACC"]
percentiles = [5, 25, 50, 75, 95]

# =======================
# DATA LOADING (CACHED)
# =======================

@st.cache_data
def load_hitters():
    # how to csv
    # return pd.read_csv("data/processed/d1_hitting_projections.csv")

    rows = []
    for p in players:
        row = {
            "player_name": p,
            "position": "OF",
            "year": np.random.choice(["Fr", "So", "Jr", "Sr"]),
            "conference": np.random.choice(confs),
            "team": np.random.choice(teams),
            "PA": np.random.randint(80, 500)
        }
        for q in percentiles:
            row[f"wOBA_p{q}"] = np.random.uniform(.300, .420)
            row[f"BA_p{q}"]   = np.random.uniform(.220, .320)
            row[f"OBP_p{q}"]  = np.random.uniform(.300, .420)
            row[f"SLG_p{q}"]  = np.random.uniform(.350, .600)
            row[f"1B_p{q}"]   = np.random.randint(10, 60)
            row[f"2B_p{q}"]   = np.random.randint(5, 25)
            row[f"3B_p{q}"]   = np.random.randint(0, 5)
            row[f"HR_p{q}"]   = np.random.randint(0, 20)
            row[f"HBP_p{q}"]  = np.random.randint(0, 10)
            row[f"BB_p{q}"]   = np.random.randint(10, 50)
            row[f"K_p{q}"]    = np.random.randint(30, 120)
        rows.append(row)
    return pd.DataFrame(rows)

@st.cache_data
def load_pitchers():
    # how to csv 
    # return pd.read_csv("data/processed/d1_pitching_projections.csv")

    rows = []
    for p in players:
        BF = np.random.randint(80, 500)
        row = {
            "player_name": p,
            "position": "RHP",
            "year": np.random.choice(["Fr", "So", "Jr", "Sr"]),
            "conference": np.random.choice(confs),
            "team": np.random.choice(teams),
            "IP": np.random.randint(10, 120),
            "BF": BF
        }
        for q in percentiles:
            row[f"FIP_p{q}"] = np.random.uniform(2.8, 5.2)
            row[f"ERA_p{q}"] = np.random.uniform(2.5, 5.5)
            row[f"K_p{q}"]   = np.random.randint(20, int(0.35 * BF))
            row[f"BB_p{q}"]  = np.random.randint(5, int(0.12 * BF))
            row[f"HR_p{q}"]  = np.random.randint(1, 15)
        rows.append(row)
    return pd.DataFrame(rows)

@st.cache_data
def compute_accuracy():
    metrics = ["wOBA", "BA", "OBP", "SLG", "FIP", "ERA"]
    rows = []

    for m in metrics:
        pred = np.random.normal(0, 1, 400)
        actual = pred + np.random.normal(0, 0.4, 400)
        rows.append({
            "Metric": m,
            "RMSE": np.sqrt(np.mean((pred - actual) ** 2))
        })

    rmse_df = pd.DataFrame(rows)

    calib_df = pd.DataFrame({
        "Predicted Percentile": np.linspace(5, 95, 40),
        "Actual Percentile": np.linspace(5, 95, 40)
        + np.random.normal(0, 5, 40)
    })

    return rmse_df, calib_df

@st.cache_data
def filter_and_compute_hitters(df, min_pa, conf_list, search_name, pct):
    """Cached filtering and computation for hitters"""
    df = df[
        (df["PA"] >= min_pa) &
        (df["conference"].isin(conf_list)) &
        (df["player_name"].str.contains(search_name, case=False))
    ].copy()

    df["BB%"] = df[f"BB_p{pct}"] / df["PA"]
    df["K%"]  = df[f"K_p{pct}"]  / df["PA"]

    display = df[[
        "player_name", "position", "year", "conference", "team", "PA",
        f"wOBA_p{pct}", f"BA_p{pct}", f"OBP_p{pct}", f"SLG_p{pct}",
        f"1B_p{pct}", f"2B_p{pct}", f"3B_p{pct}", f"HR_p{pct}",
        f"HBP_p{pct}", "BB%", "K%"
    ]].rename(columns={
        f"wOBA_p{pct}": "wOBA",
        f"BA_p{pct}": "BA",
        f"OBP_p{pct}": "OBP",
        f"SLG_p{pct}": "SLG",
        f"1B_p{pct}": "1B",
        f"2B_p{pct}": "2B",
        f"3B_p{pct}": "3B",
        f"HR_p{pct}": "HR",
        f"HBP_p{pct}": "HBP"
    })

    return display.sort_values("wOBA", ascending=False)

@st.cache_data
def filter_and_compute_pitchers(df, min_ip, conf_list, search_name, pct):
    """Cached filtering and computation for pitchers"""
    df = df[
        (df["IP"] >= min_ip) &
        (df["conference"].isin(conf_list)) &
        (df["player_name"].str.contains(search_name, case=False))
    ].copy()

    df["K%"]    = df[f"K_p{pct}"]  / df["BF"]
    df["BB%"]   = df[f"BB_p{pct}"] / df["BF"]
    df["K-BB%"] = df["K%"] - df["BB%"]
    df["HR%"]   = df[f"HR_p{pct}"] / df["BF"]

    display = df[[
        "player_name", "position", "year", "conference", "team",
        "IP", "BF",
        f"FIP_p{pct}", f"ERA_p{pct}",
        "K%", "BB%", "K-BB%", "HR%"
    ]].rename(columns={
        f"FIP_p{pct}": "FIP",
        f"ERA_p{pct}": "ERA"
    })

    return display.sort_values("FIP")

@st.cache_data
def compute_team_stats(hitters_df):
    """Cached team aggregation"""
    team_hit = hitters_df.groupby("team").agg({
        "PA": "sum",
        "wOBA_p50": "mean",
        "BA_p50": "mean",
        "OBP_p50": "mean",
        "SLG_p50": "mean",
        "HR_p50": "sum"
    }).reset_index()

    team_hit.columns = ["Team", "PA", "wOBA", "BA", "OBP", "SLG", "HR"]
    return team_hit.sort_values("wOBA", ascending=False)

hitters = load_hitters()
pitchers = load_pitchers()

# =======================
# UI
# =======================

st.title("College Baseball Projection Leaderboards")

pct = st.selectbox("Percentile", percentiles, index=2, key="pct_select")

tab_hit, tab_pitch, tab_team, tab_acc = st.tabs(
    ["Hitters", "Pitchers", "Teams", "Accuracy"]
)

# ---------------- HITTERS ----------------
with tab_hit:
    st.subheader("Hitter Projections")

    min_pa = st.slider("Minimum PA", 0, 500, 100, key="hit_min_pa")
    conf = st.multiselect("Conference", confs, default=confs, key="hit_conf")
    name = st.text_input("Search Player", key="hit_search")

    # Use cached filtering function
    display = filter_and_compute_hitters(
        hitters, 
        min_pa, 
        tuple(conf),  # Convert to tuple for caching
        name if name else "", 
        pct
    )

    st.dataframe(display, width="stretch")

# ---------------- PITCHERS ----------------
with tab_pitch:
    st.subheader("Pitcher Projections")

    min_ip = st.slider("Minimum IP", 0, 120, 20, key="pit_min_ip")
    conf = st.multiselect("Conference", confs, default=confs, key="pit_conf")
    name = st.text_input("Search Pitcher", key="pit_search")

    # Use cached filtering function
    display = filter_and_compute_pitchers(
        pitchers,
        min_ip,
        tuple(conf),  # Convert to tuple for caching
        name if name else "",
        pct
    )

    st.dataframe(display, width="stretch")

# ---------------- TEAMS ----------------
with tab_team:
    st.subheader("Team Projections (Median)")

    team_hit = compute_team_stats(hitters)
    st.dataframe(team_hit, width="stretch")

# ---------------- ACCURACY ----------------
with tab_acc:
    st.subheader("Projection Accuracy")

    rmse_df, calib = compute_accuracy()
    st.dataframe(rmse_df, width="stretch")

    chart = (
        alt.Chart(calib)
        .mark_circle(size=60)
        .encode(
            x="Predicted Percentile",
            y="Actual Percentile"
        )
        + alt.Chart(pd.DataFrame({"x": [5, 95], "y": [5, 95]}))
        .mark_line()
        .encode(x="x", y="y")
    )

    st.altair_chart(chart, width="stretch")