import pandas as pd

# Load dataset
df = pd.read_csv("dataset/instagram_influencers.csv")
print("\nDATASET LOADED SUCCESSFULLY\n")

# Show available columns
print("Available Columns in Dataset:")
print(df.columns.tolist())

# Clean column names
df.columns = df.columns.str.strip()

# Function to convert 'm' and 'k' strings to numbers
def convert_to_number(x):
    x = str(x).lower().strip()
    if 'm' in x:
        return float(x.replace('m','')) * 1_000_000
    elif 'k' in x:
        return float(x.replace('k','')) * 1_000
    else:
        try:
            return float(x)
        except:
            return 0

# Convert relevant columns to numeric
df['Followers'] = df['Followers'].apply(convert_to_number)
if 'Avg. Likes' in df.columns:
    df['Avg. Likes'] = df['Avg. Likes'].apply(convert_to_number)

# Basic info
print("\nTotal number of influencers:", len(df))

# Top influencers by Influence Score
if "Influence Score" in df.columns:
    top_influencers = df.sort_values(
        by="Influence Score", ascending=False
    ).head(5)
    print("\nTop 5 Influencers:")
    print(top_influencers[["Rank", "Channel Info", "Influence Score"]])
else:
    print("\nInfluence Score column not found!")

# Average statistics
print("\nAVERAGE STATISTICS")
if "Followers" in df.columns:
    print("Average Followers:", int(df["Followers"].mean()))

if "Avg. Likes" in df.columns:
    print("Average Likes:", int(df["Avg. Likes"].mean()))

if "Influence Score" in df.columns:
    print("Average Influence Score:", round(df["Influence Score"].mean(), 2))

# Country-wise analysis
if "Country Or Region" in df.columns:
    print("\nTop 5 Countries by Influencer Count:")
    print(df["Country Or Region"].value_counts().head(5))
