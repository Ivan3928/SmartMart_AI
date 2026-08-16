import os
import numpy as np
import pandas as pd


# ==========================================
# SMARTMART SIMULATED BUSINESS DATASET
# ==========================================

np.random.seed(42)

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(DATA_DIR, exist_ok=True)


# ------------------------------------------
# 1. Create dates
# ------------------------------------------

dates = pd.date_range(
    start="2024-01-01",
    periods=36,
    freq="MS"
)

n = len(dates)


# ------------------------------------------
# 2. Business information
# ------------------------------------------

land_area = 5000
building_area = 3500
sales_area = 2500

employees = np.random.randint(45, 61, n)
operating_hours = np.random.uniform(12, 15, n)


# ------------------------------------------
# 3. Customers
# ------------------------------------------

month_number = np.arange(n)

seasonal_factor = (
    1
    + 0.12 * np.sin(2 * np.pi * month_number / 12)
)

customers = (
    18000
    + month_number * 150
    + seasonal_factor * 2500
    + np.random.normal(0, 800, n)
)

customers = customers.astype(int)
customers = np.maximum(customers, 10000)


# ------------------------------------------
# 4. Revenue
# ------------------------------------------

average_purchase = np.random.normal(650, 40, n)

revenue = customers * average_purchase

revenue = np.round(revenue, 2)


# ------------------------------------------
# 5. Electricity consumption
# ------------------------------------------

electricity_kwh = (
    75000
    + customers * 1.25
    + employees * 350
    + operating_hours * 1800
    + np.random.normal(0, 5000, n)
)

electricity_kwh = np.maximum(electricity_kwh, 50000)

electricity_kwh = np.round(electricity_kwh, 2)


# ------------------------------------------
# 6. Water consumption
# ------------------------------------------

water_m3 = (
    700
    + customers * 0.035
    + employees * 8
    + np.random.normal(0, 70, n)
)

water_m3 = np.maximum(water_m3, 400)

water_m3 = np.round(water_m3, 2)


# ------------------------------------------
# 7. Fuel consumption
# ------------------------------------------

fuel_liters = (
    2500
    + customers * 0.08
    + np.random.normal(0, 250, n)
)

fuel_liters = np.maximum(fuel_liters, 1500)

fuel_liters = np.round(fuel_liters, 2)


# ------------------------------------------
# 8. Raw / operational materials
# ------------------------------------------

packaging_kg = (
    customers * 0.035
    + np.random.normal(0, 150, n)
)

packaging_kg = np.maximum(packaging_kg, 300)

packaging_kg = np.round(packaging_kg, 2)


cleaning_material_kg = (
    employees * 2.5
    + np.random.normal(0, 20, n)
)

cleaning_material_kg = np.maximum(cleaning_material_kg, 50)

cleaning_material_kg = np.round(cleaning_material_kg, 2)


# ------------------------------------------
# 9. Waste
# ------------------------------------------

waste_kg = (
    customers * 0.045
    + packaging_kg * 0.15
    + np.random.normal(0, 100, n)
)

waste_kg = np.maximum(waste_kg, 200)

waste_kg = np.round(waste_kg, 2)


# ------------------------------------------
# 10. Resource prices
# ------------------------------------------

electricity_price = np.random.uniform(8.0, 10.0, n)
water_price = np.random.uniform(35, 45, n)
fuel_price = np.random.uniform(90, 105, n)
packaging_price = np.random.uniform(70, 90, n)
cleaning_price = np.random.uniform(120, 150, n)


# ------------------------------------------
# 11. Resource costs
# ------------------------------------------

electricity_cost = electricity_kwh * electricity_price

water_cost = water_m3 * water_price

fuel_cost = fuel_liters * fuel_price

packaging_cost = packaging_kg * packaging_price

cleaning_cost = cleaning_material_kg * cleaning_price

total_resource_cost = (
    electricity_cost
    + water_cost
    + fuel_cost
    + packaging_cost
    + cleaning_cost
)


# ------------------------------------------
# 12. Cost of goods sold
# ------------------------------------------

cogs = revenue * np.random.uniform(0.62, 0.68, n)


# ------------------------------------------
# 13. Operating expenses
# ------------------------------------------

salary_expense = employees * 28000

rent_and_maintenance = np.random.uniform(
    500000,
    600000,
    n
)

other_operating_expense = np.random.uniform(
    150000,
    250000,
    n
)

operating_expenses = (
    salary_expense
    + rent_and_maintenance
    + other_operating_expense
    + total_resource_cost
)


# ------------------------------------------
# 14. Profit
# ------------------------------------------

gross_profit = revenue - cogs

operating_profit = gross_profit - operating_expenses

tax = np.maximum(operating_profit * 0.20, 0)

net_profit = operating_profit - tax


# ------------------------------------------
# 15. Balance Sheet
# ------------------------------------------

land_value = 15000000

building_value = 25000000

equipment_value = 5000000

inventory = cogs * 0.15

cash = np.maximum(
    revenue * 0.20,
    1000000
)

accounts_receivable = revenue * 0.05

total_assets = (
    land_value
    + building_value
    + equipment_value
    + inventory
    + cash
    + accounts_receivable
)


# Liabilities

bank_loan = 12000000

accounts_payable = cogs * 0.08

total_liabilities = bank_loan + accounts_payable


# Equity balances the accounting equation

total_equity = total_assets - total_liabilities


# ------------------------------------------
# 16. KPIs
# ------------------------------------------

electricity_per_customer = (
    electricity_kwh / customers
)

water_per_customer = (
    water_m3 / customers
)

revenue_per_square_meter = (
    revenue / sales_area
)

electricity_per_square_meter = (
    electricity_kwh / building_area
)

resource_cost_percentage = (
    total_resource_cost / revenue * 100
)


# ------------------------------------------
# 17. Create DataFrame
# ------------------------------------------

df = pd.DataFrame({
    "date": dates,

    "customers": customers,
    "employees": employees,
    "operating_hours": operating_hours,

    "land_area_m2": land_area,
    "building_area_m2": building_area,
    "sales_area_m2": sales_area,

    "revenue": revenue,
    "cogs": cogs,

    "electricity_kwh": electricity_kwh,
    "water_m3": water_m3,
    "fuel_liters": fuel_liters,

    "packaging_kg": packaging_kg,
    "cleaning_material_kg": cleaning_material_kg,
    "waste_kg": waste_kg,

    "electricity_price": electricity_price,
    "water_price": water_price,
    "fuel_price": fuel_price,

    "electricity_cost": electricity_cost,
    "water_cost": water_cost,
    "fuel_cost": fuel_cost,
    "packaging_cost": packaging_cost,
    "cleaning_cost": cleaning_cost,

    "total_resource_cost": total_resource_cost,

    "salary_expense": salary_expense,
    "rent_and_maintenance": rent_and_maintenance,
    "other_operating_expense": other_operating_expense,

    "operating_expenses": operating_expenses,

    "gross_profit": gross_profit,
    "operating_profit": operating_profit,
    "tax": tax,
    "net_profit": net_profit,

    "land_value": land_value,
    "building_value": building_value,
    "equipment_value": equipment_value,
    "inventory": inventory,
    "cash": cash,
    "accounts_receivable": accounts_receivable,

    "total_assets": total_assets,

    "bank_loan": bank_loan,
    "accounts_payable": accounts_payable,
    "total_liabilities": total_liabilities,

    "total_equity": total_equity,

    "electricity_per_customer": electricity_per_customer,
    "water_per_customer": water_per_customer,
    "revenue_per_square_meter": revenue_per_square_meter,
    "electricity_per_square_meter": electricity_per_square_meter,
    "resource_cost_percentage": resource_cost_percentage
})


# ------------------------------------------
# 18. Save dataset
# ------------------------------------------

output_file = os.path.join(
    DATA_DIR,
    "smartmart_data.csv"
)

df.to_csv(output_file, index=False)


print("=" * 50)
print("SMARTMART DATASET CREATED SUCCESSFULLY")
print("=" * 50)

print(f"\nRows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print(f"\nSaved to:")
print(output_file)

print("\nFirst 5 rows:")
print(df.head())

print("\nBalance Sheet Check:")

balance_check = (
    df["total_assets"]
    - (
        df["total_liabilities"]
        + df["total_equity"]
    )
)

print(
    f"Maximum difference: "
    f"{balance_check.abs().max():.2f}"
)

if balance_check.abs().max() < 0.01:
    print("✓ Balance sheet is balanced!")
else:
    print("⚠ Balance sheet needs checking.")