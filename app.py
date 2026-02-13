
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="College Baseball Projections")

@st.cache_data
def load_hitters():
    """Load projections for hitters."""
    rows = []
    for p in players:
        pa = np.random.randint(80, 500)
        bb = np.random.randint(10, 50)
        k = np.random.randint(30, 120)
        rows.append(
            {
                "player_name": p,
                "position": "OF",
                "year": np.random.choice(["Fr", "So", "Jr", "Sr"]),
                "conference": np.random.choice(confs),
                "PA": pa,
                "wOBA": np.random.uniform(0.300, 0.420),
                "BA": np.random.uniform(0.220, 0.320),
                "OBP": np.random.uniform(0.300, 0.420),
                "SLG": np.random.uniform(0.350, 0.600),
                "1B": np.random.randint(10, 60),
                "2B": np.random.randint(5, 25),
                "3B": np.random.randint(0, 5),
                "HR": np.random.randint(0, 20),
                "HBP": np.random.randint(0, 10),
                "BB": bb,
                "K": k,
            }
        )
    return pd.DataFrame(rows)


@st.cache_data
def load_pitchers():
    """Load point projections for pitchers (stub/demo data in current app)."""
    rows = []
    for p in players:
        bf = np.random.randint(80, 500)
        k = np.random.randint(20, int(0.35 * bf))
        bb = np.random.randint(5, int(0.12 * bf))
        hr = np.random.randint(1, 15)
        rows.append(
            {
                "player_name": p,
                "position": "RHP",
                "year": np.random.choice(["Fr", "So", "Jr", "Sr"]),
                "conference": np.random.choice(confs),
                "IP": np.random.randint(10, 120),
                "BF": bf,
                "FIP": np.random.uniform(2.8, 5.2),
                "ERA": np.random.uniform(2.5, 5.5),
                "K": k,
                "BB": bb,
                "HR": hr,
            }
        )
    return pd.DataFrame(rows)


@st.cache_data
def filter_and_compute_hitters(df, conf_list, search_name):
    """Filter and compute hitter rate stats from point projections."""
    filtered = df[
        (df["conference"].isin(conf_list))
        & (df["player_name"].str.contains(search_name, case=False))
    ].copy()

    filtered["BB%"] = filtered["BB"] / filtered["PA"]
    filtered["K%"] = filtered["K"] / filtered["PA"]

    display = filtered[
        [
            "player_name",
            "position",
            "year",
            "conference",
            "PA",
            "wOBA",
            "BA",
            "OBP",
            "SLG",
            "1B",
            "2B",
            "3B",
            "HR",
            "HBP",
            "BB%",
            "K%",
        ]
    ]

    return display.sort_values("wOBA", ascending=False)


@st.cache_data
def filter_and_compute_pitchers(df, conf_list, search_name):
    """Filter and compute pitcher rate stats from point projections."""
    filtered = df[
        (df["conference"].isin(conf_list))
        & (df["player_name"].str.contains(search_name, case=False))
    ].copy()

    filtered["K%"] = filtered["K"] / filtered["BF"]
    filtered["BB%"] = filtered["BB"] / filtered["BF"]
    filtered["K-BB%"] = filtered["K%"] - filtered["BB%"]
    filtered["HR%"] = filtered["HR"] / filtered["BF"]

    display = filtered[
        [
            "player_name",
            "position",
            "year",
            "conference",
            "IP",
            "BF",
            "FIP",
            "ERA",
            "K%",
            "BB%",
            "K-BB%",
            "HR%",
        ]
    ]

    return display.sort_values("FIP")


hitters = load_hitters()
pitchers = load_pitchers()

st.title("College Baseball Projection Leaderboards")

tab_hit, tab_pitch = st.tabs(["Hitters", "Pitchers"])

with tab_hit:
    st.subheader("Hitter Point Projections")

    conf = st.multiselect("Conference", confs, default=confs, key="hit_conf")
    name = st.text_input("Search Player", key="hit_search")

    display = filter_and_compute_hitters(hitters, tuple(conf), name if name else "")
    st.dataframe(display, width="stretch")

with tab_pitch:
    st.subheader("Pitcher Point Projections")

    conf = st.multiselect("Conference", confs, default=confs, key="pit_conf")
    name = st.text_input("Search Pitcher", key="pit_search")

    display = filter_and_compute_pitchers(pitchers, tuple(conf), name if name else "")
    st.dataframe(display, width="stretch")
