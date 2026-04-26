from pathlib import Path

import pandas as pd
import yaml
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "data.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

with open(PROJECT_ROOT / "params.yaml", "r", encoding="utf-8") as file:
    params = yaml.safe_load(file)

test_size = params["split"]["test_size"]
random_state = params["random_state"]

df = pd.read_csv(RAW_DATA_PATH)
df = df.drop_duplicates().dropna().reset_index(drop=True)

target_column = "variety"

X = df.drop(columns=[target_column])
y = df[target_column]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=test_size,
    random_state=random_state,
    stratify=y
)

train_df = X_train.copy()
train_df[target_column] = y_train.values

test_df = X_test.copy()
test_df[target_column] = y_test.values

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

train_df.to_csv(PROCESSED_DIR / "train.csv", index=False)
test_df.to_csv(PROCESSED_DIR / "test.csv", index=False)

print(f"Train rows: {len(train_df)}")
print(f"Test rows: {len(test_df)}")
print(f"Random state: {random_state}")
