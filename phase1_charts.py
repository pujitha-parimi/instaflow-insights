import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from matplotlib.ticker import MaxNLocator, FuncFormatter

DATASET_PATH = "dataset/instagram_influencers.csv"

# Dataset name (used for folder)
DATASET_NAME = os.path.splitext(os.path.basename(DATASET_PATH))[0]

OUTPUT_DIR = os.path.join(
    "static", "images", DATASET_NAME
)

# -----------------------------
# CREATE OUTPUT FOLDER (IF NEEDED)
# -----------------------------

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Created image folder: {OUTPUT_DIR}")
else:
    print(f"Image folder already exists: {OUTPUT_DIR}")

# -----------------------------
# LOAD DATASET
# -----------------------------

df = pd.read_csv(DATASET_PATH)
# Clean column names
df.columns = df.columns.str.strip()

print("Dataset loaded for chart generation")

def save_chart(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(path):
        print(f"Chart already exists, skipping: {filename}")
        return False
    plt.savefig(path)
    print(f"Saved: {path}")
    return True

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

numeric_cols = [
    "Followers",
    "Avg. Likes",
    "Influence Score",
    "60-Day Eng Rate",
    "Posts"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].apply(convert_to_number)
df["Followers_M"] = df["Followers"] / 1_000_000
df["Avg_Likes_K"] = df["Avg. Likes"] / 1_000

# -----------------------------
# CHART 1: Followers vs Influence Score (Bar Chart)
# -----------------------------

top10 = df.sort_values(by="Influence Score", ascending=False).head(15)

plt.figure()
plt.bar(top10["Channel Info"], top10["Influence Score"])
plt.xlabel("Influencers")
plt.ylabel("Influence Score")
plt.title("Top 15 Influencers by Influence Score")
plt.xticks(rotation=75)
plt.tight_layout()
if save_chart("top_influencers_influence.png"):
    plt.close()
else:
    plt.close()


print("Chart 1 saved: top_influencers_influence.png")



# Bottom 15 influencers
bottom15 = df.sort_values(by="Influence Score", ascending=True).head(15)

plt.figure()
plt.bar(bottom15["Channel Info"], bottom15["Influence Score"])
plt.xlabel("Influencers")
plt.ylabel("Influence Score")
plt.title("Bottom 15 Influencers by Influence Score")
plt.xticks(rotation=75)
plt.tight_layout()

if save_chart("bottom_influencers_influence.png"):
    plt.close()
else:
    plt.close()



# Sort by Influence Score
df_sorted = df.sort_values(by="Influence Score", ascending=False)

# Find the middle index
middle_index = len(df_sorted) // 2
middle15 = df_sorted.iloc[middle_index-7:middle_index+8]  # 15 entries centered around median

plt.figure()
plt.bar(middle15["Channel Info"], middle15["Influence Score"])
plt.xlabel("Influencers")
plt.ylabel("Influence Score")
plt.title("Middle 15 Influencers by Influence Score")
plt.xticks(rotation=75)
plt.tight_layout()

if save_chart("middle_influencers_influence.png"):
    plt.close()
else:
    plt.close()

# -----------------------------
# CHART 2: Country-wise Distribution (Pie Chart)
# -----------------------------

country_counts = df["Country Or Region"].value_counts().head(5)

plt.figure()
plt.pie(country_counts.values, labels=country_counts.index, autopct="%1.1f%%")
plt.title("Top 5 Countries by Influencer Distribution")
plt.tight_layout()
if save_chart("country_distribution_pie.png"):
    plt.close()
else:
    plt.close()


print("Chart 2 saved: country_distribution_pie.png")

# -----------------------------
# CHART 3: Followers vs Influence Score (Scatter)
# -----------------------------

plt.figure(figsize=(8,6))
plt.scatter(df["Followers_M"], df["Influence Score"], alpha=0.6)
plt.xlabel("Followers (in Millions)")
plt.ylabel("Influence Score")
plt.title("Followers vs Influence Score")
plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
save_chart("followers_vs_influence.png")
plt.close()


print("Chart 3 saved: followers_vs_influence.png")

# -----------------------------
# CHART 4: Avg Likes vs Followers
# -----------------------------

plt.figure(figsize=(9,6))

plt.scatter(
    df["Followers_M"],
    df["Avg_Likes_K"],
    alpha=0.6
)

plt.xlabel("Followers (Millions)")
plt.ylabel("Average Likes (Thousands)")
plt.title("Followers vs Average Likes")

# ✅ LIMIT number of ticks
plt.gca().xaxis.set_major_locator(MaxNLocator(6))
plt.gca().yaxis.set_major_locator(MaxNLocator(6))

# ✅ Format tick labels
plt.gca().xaxis.set_major_formatter(
    FuncFormatter(lambda x, _: f"{x:.1f}M")
)
plt.gca().yaxis.set_major_formatter(
    FuncFormatter(lambda y, _: f"{y:.0f}K")
)

plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()

save_chart("followers_vs_avg_likes.png")
plt.close()



print("Chart 4 saved: followers_vs_avg_likes.png")

# -----------------------------
# CHART 5: Engagement Rate Distribution
# -----------------------------

plt.figure(figsize=(8,6))
engagement_clean = df["60-Day Eng Rate"].dropna()
plt.hist(engagement_clean, bins=15, edgecolor="black")
plt.xlabel("Engagement Rate (%)")
plt.ylabel("Number of Influencers")
plt.title("Engagement Rate Distribution")
plt.tight_layout()
save_chart("engagement_rate_distribution.png")
plt.close()


print("Chart 5 saved: engagement_rate_distribution.png")

# -----------------------------
# CHART 6: Posts vs Engagement Rate
# -----------------------------

plt.figure(figsize=(8,6))
plt.scatter(df["Posts"], df["60-Day Eng Rate"], alpha=0.6)
plt.xlabel("Number of Posts")
plt.ylabel("Engagement Rate (%)")
plt.title("Posts vs Engagement Rate")
plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
save_chart("posts_vs_engagement.png")
plt.close()


print("Chart 6 saved: posts_vs_engagement.png")

# -----------------------------
# CHART 7: Top Countries by Avg Influence Score
# -----------------------------

country_influence = (
    df.groupby("Country Or Region")["Influence Score"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
)

plt.figure()
country_influence.plot(kind="bar")
plt.xlabel("Country")
plt.ylabel("Average Influence Score")
plt.title("Top Countries by Average Influence Score")
plt.tight_layout()
save_chart("top_countries_avg_influence.png")
plt.close()

print("Chart 7 saved: top_countries_avg_influence.png")

numeric_df = df.select_dtypes(include="number")

plt.figure(figsize=(8,6))
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap of Influencer Metrics")
plt.tight_layout()
save_chart("correlation_heatmap.png")
plt.close()

print("Chart 8 saved: correlation_heatmap.png")

