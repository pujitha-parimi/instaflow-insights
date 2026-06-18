import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# -----------------------------
# Helper function to convert k/m/b values
# -----------------------------
def convert_to_number(value):
    if isinstance(value, str):
        value = value.lower().replace(",", "").strip()
        try:
            if value.endswith("k"):
                return float(value[:-1]) * 1_000
            elif value.endswith("m"):
                return float(value[:-1]) * 1_000_000
            elif value.endswith("b"):
                return float(value[:-1]) * 1_000_000_000
            else:
                return float(value)
        except:
            return np.nan
    return value

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("dataset/instagram_influencers.csv")
df.columns = df.columns.str.strip()

print("Dataset loaded for ML")

# -----------------------------
# Clean numeric columns
# -----------------------------
numeric_columns = [
    "Followers",
    "Avg. Likes",
    "New Post Avg. Likes",
    "Total Likes"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = df[col].apply(convert_to_number)

# Clean engagement rate
if "60-Day Eng Rate" in df.columns:
    df["60-Day Eng Rate"] = (
        df["60-Day Eng Rate"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )
    df["60-Day Eng Rate"] = pd.to_numeric(df["60-Day Eng Rate"], errors="coerce")

# Drop missing values
df = df.dropna(subset=["Followers", "Avg. Likes", "60-Day Eng Rate"])

# -----------------------------
# 🔥 Create Custom Influence Score
# -----------------------------
df["Custom Influence Score"] = (
    0.4 * df["60-Day Eng Rate"] +
    0.3 * np.log1p(df["Followers"]) +
    0.3 * np.log1p(df["Avg. Likes"])
)

# -----------------------------
# Features & Target
# -----------------------------
features = ["Followers", "Avg. Likes", "60-Day Eng Rate"]
X = df[features]
y = df["Custom Influence Score"]

# -----------------------------
# Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Train Model
# -----------------------------
model = LinearRegression()
model.fit(X_train, y_train)

print("Model training completed")

# -----------------------------
# Predictions
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# Evaluation
# -----------------------------
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nMODEL PERFORMANCE")
print("Mean Absolute Error:", round(mae, 4))
print("R2 Score:", round(r2, 4))
