import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "smartmart_data.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

os.makedirs(MODEL_DIR, exist_ok=True)


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(DATA_FILE)

print("=" * 50)
print("SMARTMART ML MODEL TRAINING")
print("=" * 50)

print(f"\nDataset shape: {df.shape}")


# ==========================================
# MODEL 1: ELECTRICITY PREDICTION
# ==========================================

electricity_features = [
    "customers",
    "employees",
    "operating_hours",
    "sales_area_m2",
    "revenue",
    "water_m3",
    "fuel_liters"
]

X_electricity = df[electricity_features]

y_electricity = df["electricity_kwh"]


X_train, X_test, y_train, y_test = train_test_split(
    X_electricity,
    y_electricity,
    test_size=0.20,
    random_state=42
)


electricity_model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

electricity_model.fit(
    X_train,
    y_train
)


electricity_prediction = electricity_model.predict(X_test)

electricity_mae = mean_absolute_error(
    y_test,
    electricity_prediction
)

electricity_r2 = r2_score(
    y_test,
    electricity_prediction
)


print("\nELECTRICITY MODEL")
print("-" * 30)

print(f"MAE: {electricity_mae:,.2f} kWh")
print(f"R² Score: {electricity_r2:.3f}")


joblib.dump(
    electricity_model,
    os.path.join(
        MODEL_DIR,
        "electricity_model.pkl"
    )
)


# ==========================================
# MODEL 2: WATER PREDICTION
# ==========================================

water_features = [
    "customers",
    "employees",
    "operating_hours",
    "sales_area_m2",
    "revenue",
    "electricity_kwh"
]

X_water = df[water_features]

y_water = df["water_m3"]


X_train, X_test, y_train, y_test = train_test_split(
    X_water,
    y_water,
    test_size=0.20,
    random_state=42
)


water_model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

water_model.fit(
    X_train,
    y_train
)


water_prediction = water_model.predict(X_test)

water_mae = mean_absolute_error(
    y_test,
    water_prediction
)

water_r2 = r2_score(
    y_test,
    water_prediction
)


print("\nWATER MODEL")
print("-" * 30)

print(f"MAE: {water_mae:,.2f} m³")
print(f"R² Score: {water_r2:.3f}")


joblib.dump(
    water_model,
    os.path.join(
        MODEL_DIR,
        "water_model.pkl"
    )
)


# ==========================================
# FINISHED
# ==========================================

print("\n" + "=" * 50)
print("MODEL TRAINING COMPLETED")
print("=" * 50)

print("\nModels saved in:")

print(
    os.path.join(
        MODEL_DIR,
        "electricity_model.pkl"
    )
)

print(
    os.path.join(
        MODEL_DIR,
        "water_model.pkl"
    )
)