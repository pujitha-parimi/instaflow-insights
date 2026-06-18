import os
import pandas as pd
import plotly.express as px

DATASET_PATH = "dataset/instagram_influencers.csv"

DATASET_NAME = os.path.splitext(os.path.basename(DATASET_PATH))[0]

OUTPUT_DIR = os.path.join("static", "interactive", DATASET_NAME)
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATASET_PATH)
df.columns = df.columns.str.strip()

def convert_to_number(value):
    value = str(value).lower().replace(",", "").strip()
    if value.endswith("k"):
        return float(value[:-1]) * 1_000
    elif value.endswith("m"):
        return float(value[:-1]) * 1_000_000
    else:
        try:
            return float(value)
        except:
            return None

df["Followers"] = df["Followers"].apply(convert_to_number)
df["Avg. Likes"] = df["Avg. Likes"].apply(convert_to_number)

df["Followers_M"] = df["Followers"] / 1_000_000
df["Avg_Likes_K"] = df["Avg. Likes"] / 1_000
df["Influence Score"] = pd.to_numeric(df["Influence Score"], errors="coerce")
df["Posts"] = pd.to_numeric(df["Posts"], errors="coerce")

df["60-Day Eng Rate"] = (
    df["60-Day Eng Rate"]
    .astype(str)
    .str.replace("%", "")
)
df["60-Day Eng Rate"] = pd.to_numeric(
    df["60-Day Eng Rate"], errors="coerce"
)

# -----------------------------
# INTERACTIVE SCATTER (Hover Enabled)
# -----------------------------

fig = px.scatter(
    df,
    x="Followers_M",
    y="Avg_Likes_K",
    hover_name="Channel Info",
    hover_data={
        "Followers_M": ":.2f",
        "Avg_Likes_K": ":.0f"
    },
    labels={
        "Followers_M": "Followers (Millions)",
        "Avg_Likes_K": "Average Likes (Thousands)"
    },
    title="Followers vs Average Likes (Interactive)"
)

fig.write_html(
    os.path.join(OUTPUT_DIR, "followers_vs_avg_likes_interactive.html")
)

fig2 = px.scatter(
    df,
    x="Followers_M",
    y="Influence Score",
    hover_name="Channel Info",
    labels={
        "Followers_M": "Followers (Millions)",
        "Influence Score": "Influence Score"
    },
    title="Followers vs Influence Score (Interactive)"
)

fig2.write_html(
    os.path.join(OUTPUT_DIR, "followers_vs_influence_interactive.html")
)

print("followers_vs_influence_interactive.html saved")

fig3 = px.scatter(
    df,
    x="Posts",
    y="60-Day Eng Rate",
    hover_name="Channel Info",
    labels={
        "Posts": "Number of Posts",
        "60-Day Eng Rate": "Engagement Rate (%)"
    },
    title="Posts vs Engagement Rate (Interactive)"
)

fig3.write_html(
    os.path.join(OUTPUT_DIR, "posts_vs_engagement_interactive.html")
)

print("posts_vs_engagement_interactive.html saved")

print("Interactive chart saved successfully")
