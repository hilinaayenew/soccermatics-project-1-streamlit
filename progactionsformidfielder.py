import streamlit as st
import pandas as pd
from scipy.stats import percentileofscore
import plotly.express as px

# -----------------------
# Load CSV
# -----------------------
mid_prog_df = pd.read_csv("euro24_midfielders_full.csv")
mid_prog_df.columns = mid_prog_df.columns.str.strip()

# -----------------------
st.title("Euro 2024 Midfielders: Progressive Actions Dashboard")
st.markdown("visualization of progressive passes, carries, and final third entries.")
st.markdown("This data applies to players with above 200 total minutes played.")

# -----------------------
# Player selector
# -----------------------
players = mid_prog_df["player"].tolist()
selected_player = st.selectbox("Select a player", players)
player_data = mid_prog_df[mid_prog_df["player"] == selected_player]

# -----------------------
# Add hover text for Plotly
# -----------------------
mid_prog_df['hover_text'] = (
    "Player: " + mid_prog_df['player'] +
    "<br>Total games: " + mid_prog_df['total_games'].astype(str) +
    "<br>Mid games: " + mid_prog_df['mid_games'].astype(str) +
    "<br>Prog Passes /90: " + mid_prog_df['prog_passes_90'].round(2).astype(str) +
    "<br>Prog Carries /90: " + mid_prog_df['prog_carries_90'].round(2).astype(str) +
    "<br>Final Third /90: " + mid_prog_df['prog_passes_final_third_90'].round(2).astype(str)
)

# -----------------------
# Scatter plot: Passes vs Carries
# -----------------------
st.subheader("Progressive Passes vs Carries per 90")

fig = px.scatter(
    mid_prog_df,
    x='prog_passes_90',
    y='prog_carries_90',
    color=mid_prog_df['player'].apply(
        lambda x: 'green' if x == selected_player  else 'red' if x == "Christian Dannemann Eriksen" else 'gray'
    ),
    hover_name='player',
    hover_data={
        'total_games': True,
        'mid_games': True,
        'prog_passes_90': True,
        'prog_carries_90': True,
        'prog_passes_final_third_90': True
    },
    opacity=0.7,
    size_max=20
)
fig.update_layout(title='Progressive Passes vs Carries per 90', xaxis_title='Prog Passes /90', yaxis_title='Prog Carries /90')
st.plotly_chart(fig, use_container_width=True)

# -----------------------
# Scatter plot: Passes vs Final Third Entries
# -----------------------
st.subheader("Progressive Passes vs Final Third Entries per 90")

fig2 = px.scatter(
    mid_prog_df,
    x='prog_passes_90',
    y='prog_passes_final_third_90',
    color=mid_prog_df['player'].apply(
        lambda x: 'green' if x == selected_player else 'red' if x == "Christian Dannemann Eriksen" else 'gray'
    ),
    hover_name='player',
    hover_data={
        'total_games': True,
        'mid_games': True,
        'prog_passes_90': True,
        'prog_carries_90': True,
        'prog_passes_final_third_90': True
    },
    opacity=0.7,
    size_max=20
)
fig2.update_layout(title='Progressive Passes vs Final Third Entries', xaxis_title='Prog Passes /90', yaxis_title='Final Third /90')
st.plotly_chart(fig2, use_container_width=True)

# -----------------------
# Percentile ranks
# -----------------------
st.subheader(f"{selected_player} Percentile Ranks")

pp90 = float(player_data["prog_passes_90"].iloc[0])
pc90 = float(player_data["prog_carries_90"].iloc[0])
fte = float(player_data["prog_passes_final_third_90"].iloc[0])

pp_percentile = percentileofscore(mid_prog_df["prog_passes_90"], pp90)
pc_percentile = percentileofscore(mid_prog_df["prog_carries_90"], pc90)
fte_percentile = percentileofscore(mid_prog_df["prog_passes_final_third_90"], fte)

st.write(f"Progressive Passes / 90: {pp_percentile:.1f}th percentile")
st.write(f"Progressive Carries / 90: {pc_percentile:.1f}th percentile")
st.write(f"Final Third Entries / 90: {fte_percentile:.1f}th percentile")

# -----------------------
# Ranking table with customizable metric
# -----------------------
st.subheader("Midfielders Rank Table")

rank_metrics = [
    "prog_passes_90", 
    "prog_carries_90", 
    "prog_passes_final_third_90", 
    "prog_passes", 
    "prog_carries", 
    "prog_passes_final_third", 
    "total_games", 
    "mid_games"
]
selected_metric = st.selectbox("Select metric to rank by", rank_metrics)

rank_table = mid_prog_df.sort_values(selected_metric, ascending=False).reset_index(drop=True)
rank_table["rank"] = rank_table.index + 1
rank_table = rank_table[[
    "rank", "player", "total_games", "mid_games",
    "prog_passes", "prog_carries", "prog_passes_final_third",
    "prog_passes_90", "prog_carries_90", "prog_passes_final_third_90"
]]

# Highlight Eriksen (blue if not selected, red if selected) and selected player
def highlight_players(row):
    if row["player"] == "Christian Dannemann Eriksen":
        color = 'green' if selected_player == "Christian Dannemann Eriksen" else 'red'
        return [f'background-color: {color}' for _ in row]
    elif row["player"] == selected_player:
        return ['background-color: green' for _ in row]
    else:
        return ['' for _ in row]

st.dataframe(rank_table.style.apply(highlight_players, axis=1))
