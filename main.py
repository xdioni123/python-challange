import streamlit as st
import pandas as pd

st.set_page_config(page_title="Champions League 2025 Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("champions-league-2025-UTC.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Home Goals"] = df["Result"].str.extract(r'(\d+)\s*-\s*\d+').astype(float)
    df["Away Goals"] = df["Result"].str.extract(r'\d+\s*-\s*(\d+)').astype(float)
    return df

st.title("UEFA Champions League 2025 Dashboard")

try:
    df = load_data()
except FileNotFoundError:
    st.error("CSV file not found! Make sure it's in the same folder as app.py")
    st.stop()

st.sidebar.header("Filters")
rounds = sorted(df["Round Number"].dropna().unique().tolist())
round_filter = st.sidebar.selectbox("Select Round", ["All"] + [str(r) for r in rounds])

teams = sorted(set(df["Home Team"].dropna().unique().tolist() + df["Away Team"].dropna().unique().tolist()))
team_filter = st.sidebar.selectbox("Select Team", ["All"] + teams)

if round_filter != "All":
    df = df[df["Round Number"] == int(round_filter)]

if team_filter != "All":
    df = df[(df["Home Team"] == team_filter) | (df["Away Team"] == team_filter)]

st.subheader("Match Results")
st.dataframe(df[["Match Number", "Round Number", "Date", "Home Team", "Away Team", "Result", "Location"]].reset_index(drop=True))

st.subheader("Match Summary")

if team_filter != "All":
    home_matches = df[df["Home Team"] == team_filter]
    away_matches = df[df["Away Team"] == team_filter]
    total_goals_for = home_matches["Home Goals"].sum() + away_matches["Away Goals"].sum()
    total_goals_against = home_matches["Away Goals"].sum() + away_matches["Home Goals"].sum()
    total_matches = len(home_matches) + len(away_matches)
    st.metric("Matches Played", total_matches)
    st.metric("Goals Scored", int(total_goals_for))
    st.metric("Goals Conceded", int(total_goals_against))

if "Home Goals" in df.columns and "Away Goals" in df.columns:
    st.subheader("Goals per Round")
    goals_df = df.groupby("Round Number")[["Home Goals", "Away Goals"]].sum()
    st.bar_chart(goals_df)

st.subheader("Match Schedule")
st.dataframe(df.sort_values("Date")[["Date", "Home Team", "Away Team", "Result", "Location"]].reset_index(drop=True))
