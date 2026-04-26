from pathlib import Path

import joblib
import mlflow
import pandas as pd
import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TRAIN_PATH = PROJECT_ROOT / "data" / "processed" / "train.csv"
TEST_PATH = PROJECT_ROOT / "data" / "processed" / "test.csv"
MODEL_PATH = PROJECT_ROOT / "model.pkl"

with open(PROJECT_ROOT / "params.yaml", "r", encoding="utf-8") as file:
    params = yaml.safe_load(file)

random_state = params["random_state"]
max_iter = params["model"]["max_iter"]

target_column = "variety"

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

X_train = train_df.drop(columns=[target_column])
y_train = train_df[target_column]

X_test = test_df.drop(columns=[target_column])
y_test = test_df[target_column]

model = LogisticRegression(
    max_iter=max_iter,
    random_state=random_state
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

joblib.dump(model, MODEL_PATH)

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("hw5_reproducibility")

with mlflow.start_run(run_name="train_logistic_regression"):
    mlflow.log_param("model", "LogisticRegression")
    mlflow.log_param("random_state", random_state)
    mlflow.log_param("max_iter", max_iter)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_artifact(str(MODEL_PATH))

print(f"accuracy = {accuracy:.4f}")
