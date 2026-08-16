import os
import joblib
import pandas as pd
import streamlit as st


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="SmartMart Resource Manager",
    page_icon="🏪",
    layout="wide"
)


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "smartmart_data.csv"
)

ELECTRICITY_MODEL_FILE = os.path.join(
    BASE_DIR,
    "models",
    "electricity_model.pkl"
)

WATER_MODEL_FILE = os.path.join(
    BASE_DIR,
    "models",
    "water_model.pkl"
)


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)


@st.cache_resource
def load_models():

    electricity_model = joblib.load(
        ELECTRICITY_MODEL_FILE
    )

    water_model = joblib.load(
        WATER_MODEL_FILE
    )

    return electricity_model, water_model


df = load_data()

electricity_model, water_model = load_models()


# ==========================================
# TITLE
# ==========================================

st.title("🏪 SmartMart Resource & Financial Management System")

st.write(
    """
    An AI/ML-based business resource management system
    for analyzing resource consumption, financial performance,
    and sustainability of a supermarket.
    """
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Section",
    [
        "Dashboard",
        "Resource Consumption",
        "Financial Analysis",
        "Balance Sheet",
        "AI Predictions",
        "Sustainability"
    ]
)


# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    st.header("📊 Business Dashboard")

    latest = df.iloc[-1]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Revenue",
            f"₹{latest['revenue']:,.0f}"
        )

    with col2:
        st.metric(
            "Net Profit",
            f"₹{latest['net_profit']:,.0f}"
        )

    with col3:
        st.metric(
            "Customers",
            f"{latest['customers']:,.0f}"
        )

    with col4:
        st.metric(
            "Resource Cost",
            f"₹{latest['total_resource_cost']:,.0f}"
        )

    st.subheader("Revenue Trend")

    revenue_chart = df.set_index("date")[
        ["revenue"]
    ]

    st.line_chart(revenue_chart)

    st.subheader("Net Profit Trend")

    profit_chart = df.set_index("date")[
        ["net_profit"]
    ]

    st.line_chart(profit_chart)


# ==========================================
# RESOURCE CONSUMPTION
# ==========================================

elif page == "Resource Consumption":

    st.header("⚡ Resource Consumption")

    latest = df.iloc[-1]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Electricity",
            f"{latest['electricity_kwh']:,.0f} kWh"
        )

    with col2:

        st.metric(
            "Water",
            f"{latest['water_m3']:,.0f} m³"
        )

    with col3:

        st.metric(
            "Fuel",
            f"{latest['fuel_liters']:,.0f} L"
        )

    st.subheader("Electricity Consumption")

    electricity_chart = df.set_index("date")[
        ["electricity_kwh"]
    ]

    st.line_chart(electricity_chart)

    st.subheader("Water Consumption")

    water_chart = df.set_index("date")[
        ["water_m3"]
    ]

    st.line_chart(water_chart)

    st.subheader("Fuel Consumption")

    fuel_chart = df.set_index("date")[
        ["fuel_liters"]
    ]

    st.line_chart(fuel_chart)

    st.subheader("Waste Generation")

    waste_chart = df.set_index("date")[
        ["waste_kg"]
    ]

    st.line_chart(waste_chart)


# ==========================================
# FINANCIAL ANALYSIS
# ==========================================

elif page == "Financial Analysis":

    st.header("💰 Financial Analysis")

    latest = df.iloc[-1]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Revenue",
            f"₹{latest['revenue']:,.0f}"
        )

    with col2:

        st.metric(
            "Operating Profit",
            f"₹{latest['operating_profit']:,.0f}"
        )

    with col3:

        st.metric(
            "Net Profit",
            f"₹{latest['net_profit']:,.0f}"
        )

    st.subheader("Revenue vs Net Profit")

    financial_chart = df.set_index("date")[
        [
            "revenue",
            "net_profit"
        ]
    ]

    st.line_chart(financial_chart)

    st.subheader("Resource Cost")

    resource_chart = df.set_index("date")[
        ["total_resource_cost"]
    ]

    st.line_chart(resource_chart)

    st.subheader("Cost Breakdown")

    cost_data = pd.DataFrame({
        "Cost Type": [
            "Electricity",
            "Water",
            "Fuel",
            "Packaging",
            "Cleaning"
        ],
        "Cost": [
            latest["electricity_cost"],
            latest["water_cost"],
            latest["fuel_cost"],
            latest["packaging_cost"],
            latest["cleaning_cost"]
        ]
    })

    st.bar_chart(
        cost_data.set_index("Cost Type")
    )


# ==========================================
# BALANCE SHEET
# ==========================================

elif page == "Balance Sheet":

    st.header("📑 Balance Sheet")

    latest = df.iloc[-1]

    st.subheader("Assets")

    assets = pd.DataFrame({
        "Asset": [
            "Land",
            "Building",
            "Equipment",
            "Inventory",
            "Cash",
            "Accounts Receivable"
        ],
        "Amount": [
            latest["land_value"],
            latest["building_value"],
            latest["equipment_value"],
            latest["inventory"],
            latest["cash"],
            latest["accounts_receivable"]
        ]
    })

    st.dataframe(
        assets,
        use_container_width=True
    )

    total_assets = latest["total_assets"]

    st.metric(
        "Total Assets",
        f"₹{total_assets:,.0f}"
    )

    st.subheader("Liabilities")

    liabilities = pd.DataFrame({
        "Liability": [
            "Bank Loan",
            "Accounts Payable"
        ],
        "Amount": [
            latest["bank_loan"],
            latest["accounts_payable"]
        ]
    })

    st.dataframe(
        liabilities,
        use_container_width=True
    )

    st.metric(
        "Total Liabilities",
        f"₹{latest['total_liabilities']:,.0f}"
    )

    st.subheader("Equity")

    st.metric(
        "Total Equity",
        f"₹{latest['total_equity']:,.0f}"
    )

    st.divider()

    st.subheader("Accounting Equation")

    st.write(
        "Assets = Liabilities + Equity"
    )

    left, right = st.columns(2)

    with left:

        st.metric(
            "Assets",
            f"₹{latest['total_assets']:,.0f}"
        )

    with right:

        st.metric(
            "Liabilities + Equity",
            f"₹{latest['total_liabilities'] + latest['total_equity']:,.0f}"
        )

    st.success(
        "✓ The balance sheet is balanced."
    )


# ==========================================
# AI PREDICTIONS
# ==========================================

elif page == "AI Predictions":

    st.header("🤖 AI Resource Consumption Prediction")

    st.write(
        """
        Use the business inputs below to estimate
        future electricity and water consumption.
        """
    )

    customers = st.number_input(
        "Expected Customers",
        min_value=1000,
        max_value=100000,
        value=20000,
        step=1000
    )

    employees = st.number_input(
        "Employees",
        min_value=1,
        max_value=500,
        value=50
    )

    operating_hours = st.number_input(
        "Operating Hours per Day",
        min_value=1.0,
        max_value=24.0,
        value=14.0
    )

    sales_area = st.number_input(
        "Sales Area (m²)",
        min_value=100.0,
        max_value=10000.0,
        value=2500.0
    )

    revenue = st.number_input(
        "Expected Revenue (₹)",
        min_value=100000.0,
        max_value=100000000.0,
        value=15000000.0,
        step=100000.0
    )

    water = st.number_input(
        "Expected Water Consumption (m³)",
        min_value=100.0,
        max_value=10000.0,
        value=1500.0
    )

    fuel = st.number_input(
        "Expected Fuel Consumption (L)",
        min_value=100.0,
        max_value=50000.0,
        value=4000.0
    )

    electricity = st.number_input(
        "Expected Electricity (kWh)",
        min_value=10000.0,
        max_value=1000000.0,
        value=100000.0
    )

    if st.button("🔮 Predict Resource Consumption"):

        electricity_input = pd.DataFrame({
            "customers": [customers],
            "employees": [employees],
            "operating_hours": [operating_hours],
            "sales_area_m2": [sales_area],
            "revenue": [revenue],
            "water_m3": [water],
            "fuel_liters": [fuel]
        })

        water_input = pd.DataFrame({
            "customers": [customers],
            "employees": [employees],
            "operating_hours": [operating_hours],
            "sales_area_m2": [sales_area],
            "revenue": [revenue],
            "electricity_kwh": [electricity]
        })

        predicted_electricity = electricity_model.predict(
            electricity_input
        )[0]

        predicted_water = water_model.predict(
            water_input
        )[0]

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Predicted Electricity",
                f"{predicted_electricity:,.0f} kWh"
            )

        with col2:

            st.metric(
                "Predicted Water",
                f"{predicted_water:,.0f} m³"
            )

        st.info(
            "These predictions are generated by the trained "
            "Random Forest machine-learning models."
        )


# ==========================================
# SUSTAINABILITY
# ==========================================

elif page == "Sustainability":

    st.header("🌱 Sustainability & SDG Analysis")

    latest = df.iloc[-1]

    electricity_efficiency = (
        latest["electricity_per_customer"]
    )

    water_efficiency = (
        latest["water_per_customer"]
    )

    resource_cost = (
        latest["resource_cost_percentage"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Electricity / Customer",
            f"{electricity_efficiency:.2f} kWh"
        )

    with col2:

        st.metric(
            "Water / Customer",
            f"{water_efficiency:.3f} m³"
        )

    with col3:

        st.metric(
            "Resource Cost / Revenue",
            f"{resource_cost:.2f}%"
        )

    st.subheader("Relevant Sustainable Development Goals")

    st.markdown(
        """
        **SDG 6 – Clean Water and Sanitation**

        Monitor and reduce water consumption.

        **SDG 7 – Affordable and Clean Energy**

        Monitor electricity consumption and improve energy efficiency.

        **SDG 9 – Industry, Innovation and Infrastructure**

        Use AI/ML to improve resource management.

        **SDG 12 – Responsible Consumption and Production**

        Monitor raw materials, packaging and waste.

        **SDG 13 – Climate Action**

        Reduce unnecessary energy and fuel consumption.
        """
    )

    st.subheader("Resource Consumption Trends")

    sustainability_chart = df.set_index("date")[
        [
            "electricity_kwh",
            "water_m3",
            "waste_kg"
        ]
    ]

    st.line_chart(sustainability_chart)


# ==========================================
# FOOTER
# ==========================================

st.sidebar.divider()

st.sidebar.caption(
    "SmartMart AI/ML Minor Project"
)

st.sidebar.caption(
    "Business Resource & Sustainability Management"
)