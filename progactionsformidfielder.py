import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import percentileofscore

# -----------------------
# Load CSV
# -----------------------
mid_prog_df = pd.read_csv("euro24_midfielders_full.csv")
mid_prog_df.columns = mid_prog_df.columns.str.strip()

# -----------------------
# App Title
# -----------------------
st.title("Euro 2024 Midfielders: Progressive Actions Dashboard")
st.markdown("Interactive visualization of progressive passes, carries, and final third entries.")

# -----------------------
# Player selector
# -----------------------
players = mid_prog_df["player"].tolist()
selected_player = st.selectbox("Select a player", players)
player_data = mid_prog_df[mid_prog_df["player"] == selected_player]

# -----------------------
# Scatter plot: Passes vs Carries
# -----------------------
st.subheader("Progressive Passes vs Carries per 90")

fig, ax = plt.subplots(figsize=(8,6))

# Default midfielders in gray (excluding selected player and Eriksen)
mask_default = (mid_prog_df["player"] != selected_player) & (mid_prog_df["player"] != "Christian Dannemann Eriksen")
ax.scatter(
    mid_prog_df.loc[mask_default, "prog_passes_90"],
    mid_prog_df.loc[mask_default, "prog_carries_90"],
    alpha=0.5, color='gray', label="Midfielders"
)

# Eriksen color logic: red if selected, blue otherwise
mask_eriksen = mid_prog_df["player"] == "Christian Dannemann Eriksen"
eriksen_color = 'red' if selected_player == "Christian Dannemann Eriksen" else 'blue'
ax.scatter(
    mid_prog_df.loc[mask_eriksen, "prog_passes_90"],
    mid_prog_df.loc[mask_eriksen, "prog_carries_90"],
    color=eriksen_color, s=120, label="Eriksen"
)

# Other selected player (not Eriksen) in red
if selected_player != "Christian Dannemann Eriksen":
    ax.scatter(
        player_data["prog_passes_90"],
        player_data["prog_carries_90"],
        color='red', s=120, label=selected_player
    )

ax.set_xlabel("Progressive Passes per 90")
ax.set_ylabel("Progressive Carries per 90")
ax.set_title("Progressive Passes vs Carries per 90")
ax.grid(alpha=0.3)
ax.legend()
st.pyplot(fig)

# -----------------------
# Scatter plot: Passes vs Final Third Entries
# -----------------------
st.subheader("Progressive Passes vs Final Third Entries per 90")

fig2, ax2 = plt.subplots(figsize=(8,6))

ax2.scatter(
    mid_prog_df.loc[mask_default, "prog_passes_90"],
    mid_prog_df.loc[mask_default, "prog_passes_final_third_90"],
    alpha=0.5, color='gray', label="Midfielders"
)

ax2.scatter(
    mid_prog_df.loc[mask_eriksen, "prog_passes_90"],
    mid_prog_df.loc[mask_eriksen, "prog_passes_final_third_90"],
    color=eriksen_color, s=120, label="Eriksen"
)

if selected_player != "Christian Dannemann Eriksen":
    ax2.scatter(
        player_data["prog_passes_90"],
        player_data["prog_passes_final_third_90"],
        color='red', s=120, label=selected_player
    )

ax2.set_xlabel("Progressive Passes per 90")
ax2.set_ylabel("Progressive Passes Final Third / 90")
ax2.set_title("Progressive Passes vs Final Third Entries")
ax2.grid(alpha=0.3)
ax2.legend()
st.pyplot(fig2)

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
        color = 'lightcoral' if selected_player == "Christian Dannemann Eriksen" else 'lightblue'
        return [f'background-color: {color}' for _ in row]
    elif row["player"] == selected_player:
        return ['background-color: lightcoral' for _ in row]
    else:
        return ['' for _ in row]

st.dataframe(rank_table.style.apply(highlight_players, axis=1))
