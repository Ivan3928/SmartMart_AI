import os
import joblib
import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartMart Business Intelligence",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT PATHS
# ============================================================

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


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)


@st.cache_resource
def load_models():
    electricity_model = joblib.load(ELECTRICITY_MODEL_FILE)
    water_model = joblib.load(WATER_MODEL_FILE)

    return electricity_model, water_model


df = load_data()

electricity_model, water_model = load_models()


# ============================================================
# PREPARE DATE
# ============================================================

df["date"] = pd.to_datetime(df["date"])


# ============================================================
# CURRENCY
# ============================================================

currency = st.sidebar.selectbox(
    "Currency",
    ["INR (₹)", "USD ($)", "EUR (€)"]
)

currency_rates = {
    "INR (₹)": 1.0,
    "USD ($)": 0.0117,
    "EUR (€)": 0.0100
}

currency_symbols = {
    "INR (₹)": "₹",
    "USD ($)": "$",
    "EUR (€)": "€"
}

rate = currency_rates[currency]
symbol = currency_symbols[currency]


def money(value):
    return f"{symbol}{value * rate:,.0f}"


# ============================================================
# PLOTLY CHART THEME
# ============================================================

CHART_BACKGROUND = "#4B5563"
PAPER_BACKGROUND = "#D9DDE3"
TEXT_COLOR = "white"


def apply_chart_theme(fig):

    fig.update_layout(
        paper_bgcolor="#D9DDE3",
        plot_bgcolor="#4B5563",

        font=dict(
            color="#FFFFFF",
            size=13
        ),

        title_font=dict(
            color="#FFFFFF",
            size=18
        ),

        xaxis=dict(
            title_font=dict(
                color="#FFFFFF"
            ),

            tickfont=dict(
                color="#E5E7EB"
            ),

            gridcolor="#6B7280",
            linecolor="#9CA3AF",
            zerolinecolor="#9CA3AF"
        ),

        yaxis=dict(
            title_font=dict(
                color="#FFFFFF"
            ),

            tickfont=dict(
                color="#E5E7EB"
            ),

            gridcolor="#6B7280",
            linecolor="#9CA3AF",
            zerolinecolor="#9CA3AF"
        ),

        legend=dict(
            font=dict(
                color="#FFFFFF"
            )
        ),

        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font=dict(
                color="#111827"
            )
        ),

        margin=dict(
            l=60,
            r=30,
            t=60,
            b=60
        )
    )

    return fig

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏪 SmartMart")

st.sidebar.caption(
    "Business Intelligence & Resource Management"
)

st.sidebar.divider()

st.sidebar.subheader("Navigation")

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

st.sidebar.divider()

st.sidebar.subheader("Business Model")

st.sidebar.info(
    "Supermarket / Retail Business"
)

st.sidebar.divider()

st.sidebar.caption(
    "AI & Data Science Minor Project"
)

st.sidebar.caption(
    "Royal Global University"
)


# ============================================================
# COMMON DATA
# ============================================================

latest = df.iloc[-1]


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.title("🏪 SmartMart Business Dashboard")

    st.write(
        "AI/ML-powered business intelligence for financial performance, "
        "resource consumption and sustainability."
    )

    st.divider()

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Revenue",
            money(latest["revenue"])
        )

    with col2:

        st.metric(
            "Net Profit",
            money(latest["net_profit"])
        )

    with col3:

        st.metric(
            "Customers",
            f"{latest['customers']:,.0f}"
        )

    with col4:

        st.metric(
            "Resource Cost",
            money(latest["total_resource_cost"])
        )

    st.write("")

    # --------------------------------------------------------
    # REVENUE & PROFIT
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        revenue_chart = px.line(
            df,
            x="date",
            y="revenue",
            title="Revenue Trend",
            markers=True
        )

        revenue_chart.update_yaxes(
            tickprefix=symbol
        )

        revenue_chart = apply_chart_theme(
            revenue_chart
        )

        st.plotly_chart(
            revenue_chart,
            use_container_width=True
        )

    with col2:

        profit_chart = px.line(
            df,
            x="date",
            y="net_profit",
            title="Net Profit Trend",
            markers=True
        )

        profit_chart.update_yaxes(
            tickprefix=symbol
        )

        profit_chart = apply_chart_theme(
            profit_chart
        )

        st.plotly_chart(
            profit_chart,
            use_container_width=True
        )

    # --------------------------------------------------------
    # BUSINESS HEALTH
    # --------------------------------------------------------

    st.subheader("Business Health")

    profit_margin = (
        latest["net_profit"]
        / latest["revenue"]
        * 100
    )

    resource_percentage = (
        latest["resource_cost_percentage"]
    )

    electricity_per_customer = (
        latest["electricity_per_customer"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Net Profit Margin",
            f"{profit_margin:.2f}%"
        )

    with col2:

        st.metric(
            "Resource Cost / Revenue",
            f"{resource_percentage:.2f}%"
        )

    with col3:

        st.metric(
            "Electricity / Customer",
            f"{electricity_per_customer:.2f} kWh"
        )


# ============================================================
# RESOURCE CONSUMPTION
# ============================================================

elif page == "Resource Consumption":

    st.title("⚡ Resource Consumption")

    st.write(
        "Monitor the supermarket's consumption of electricity, "
        "water, fuel and waste."
    )

    st.divider()

    # --------------------------------------------------------
    # RESOURCE KPIs
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

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

    with col4:

        st.metric(
            "Waste",
            f"{latest['waste_kg']:,.0f} kg"
        )

    st.write("")

    # --------------------------------------------------------
    # ELECTRICITY
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig = px.line(
            df,
            x="date",
            y="electricity_kwh",
            title="Electricity Consumption",
            markers=True
        )

        fig.update_yaxes(
            title="Electricity (kWh)"
        )

        fig = apply_chart_theme(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # WATER
    # --------------------------------------------------------

    with col2:

        fig = px.line(
            df,
            x="date",
            y="water_m3",
            title="Water Consumption",
            markers=True
        )

        fig.update_yaxes(
            title="Water (m³)"
        )

        fig = apply_chart_theme(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # FUEL
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig = px.line(
            df,
            x="date",
            y="fuel_liters",
            title="Fuel Consumption",
            markers=True
        )

        fig.update_yaxes(
            title="Fuel (Liters)"
        )

        fig = apply_chart_theme(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # WASTE
    # --------------------------------------------------------

    with col2:

        fig = px.line(
            df,
            x="date",
            y="waste_kg",
            title="Waste Generation",
            markers=True
        )

        fig.update_yaxes(
            title="Waste (kg)"
        )

        fig = apply_chart_theme(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# FINANCIAL ANALYSIS
# ============================================================

elif page == "Financial Analysis":

    st.title("💰 Financial Analysis")

    st.write(
        "Analyze revenue, operating profit, net profit and "
        "resource-related business costs."
    )

    st.divider()

    # --------------------------------------------------------
    # FINANCIAL KPIs
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Revenue",
            money(latest["revenue"])
        )

    with col2:

        st.metric(
            "Operating Profit",
            money(latest["operating_profit"])
        )

    with col3:

        st.metric(
            "Net Profit",
            money(latest["net_profit"])
        )

    st.write("")

    # --------------------------------------------------------
    # REVENUE VS PROFIT
    # --------------------------------------------------------

    financial_long = df[
        [
            "date",
            "revenue",
            "operating_profit",
            "net_profit"
        ]
    ].melt(
        id_vars="date",
        var_name="Metric",
        value_name="Amount"
    )

    fig = px.line(
        financial_long,
        x="date",
        y="Amount",
        color="Metric",
        title="Revenue and Profit Performance",
        markers=True
    )

    fig.update_yaxes(
        tickprefix=symbol
    )

    fig = apply_chart_theme(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # RESOURCE COST TREND
    # --------------------------------------------------------

    fig = px.area(
        df,
        x="date",
        y="total_resource_cost",
        title="Total Resource Cost Trend"
    )

    fig.update_yaxes(
        tickprefix=symbol
    )

    fig = apply_chart_theme(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # COST BREAKDOWN
    # --------------------------------------------------------

    st.subheader("Resource Cost Breakdown")

    cost_data = pd.DataFrame({
        "Cost Type": [
            "Electricity",
            "Water",
            "Fuel",
            "Packaging",
            "Cleaning"
        ],
        "Cost": [
            latest["electricity_cost"] * rate,
            latest["water_cost"] * rate,
            latest["fuel_cost"] * rate,
            latest["packaging_cost"] * rate,
            latest["cleaning_cost"] * rate
        ]
    })

    fig = px.bar(
        cost_data,
        x="Cost Type",
        y="Cost",
        title="Current Resource Cost Breakdown"
    )

    fig.update_yaxes(
        tickprefix=symbol
    )

    fig = apply_chart_theme(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# BALANCE SHEET
# ============================================================

elif page == "Balance Sheet":

    st.title("📑 Balance Sheet")

    st.write(
        "Financial position of the supermarket based on "
        "assets, liabilities and equity."
    )

    st.divider()

    # --------------------------------------------------------
    # ASSETS
    # --------------------------------------------------------

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

    assets_display = assets.copy()

    assets_display["Amount"] = assets_display[
        "Amount"
    ].apply(
        lambda x: money(x)
    )

    st.dataframe(
        assets_display,
        use_container_width=True,
        hide_index=True
    )

    st.metric(
        "Total Assets",
        money(latest["total_assets"])
    )

    st.write("")

    # --------------------------------------------------------
    # LIABILITIES
    # --------------------------------------------------------

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

    liabilities_display = liabilities.copy()

    liabilities_display["Amount"] = liabilities_display[
        "Amount"
    ].apply(
        lambda x: money(x)
    )

    st.dataframe(
        liabilities_display,
        use_container_width=True,
        hide_index=True
    )

    st.metric(
        "Total Liabilities",
        money(latest["total_liabilities"])
    )

    st.write("")

    # --------------------------------------------------------
    # EQUITY
    # --------------------------------------------------------

    st.subheader("Equity")

    st.metric(
        "Total Equity",
        money(latest["total_equity"])
    )

    st.divider()

    # --------------------------------------------------------
    # ACCOUNTING EQUATION
    # --------------------------------------------------------

    st.subheader("Accounting Equation")

    st.info(
        "Assets = Liabilities + Equity"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Assets",
            money(latest["total_assets"])
        )

    with col2:

        liabilities_equity = (
            latest["total_liabilities"]
            + latest["total_equity"]
        )

        st.metric(
            "Liabilities + Equity",
            money(liabilities_equity)
        )

    difference = (
        latest["total_assets"]
        - liabilities_equity
    )

    if abs(difference) < 1:

        st.success(
            "✓ Balance sheet is balanced."
        )

    else:

        st.warning(
            f"Balance sheet difference: {money(difference)}"
        )


# ============================================================
# AI PREDICTIONS
# ============================================================

elif page == "AI Predictions":

    st.title("🤖 AI Resource Consumption Prediction")

    st.write(
        "Use the trained machine-learning models to estimate "
        "future electricity and water consumption."
    )

    st.divider()

    st.info(
        "The application uses trained Random Forest models "
        "for resource consumption prediction."
    )

    # --------------------------------------------------------
    # INPUTS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

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

    with col2:

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

    st.write("")

    # --------------------------------------------------------
    # PREDICTION BUTTON
    # --------------------------------------------------------

    if st.button(
        "🔮 Run AI Prediction",
        use_container_width=True
    ):

        # Electricity model input
        electricity_input = pd.DataFrame({
            "customers": [customers],
            "employees": [employees],
            "operating_hours": [operating_hours],
            "sales_area_m2": [sales_area],
            "revenue": [revenue],
            "water_m3": [water],
            "fuel_liters": [fuel]
        })

        # Water model input
        water_input = pd.DataFrame({
            "customers": [customers],
            "employees": [employees],
            "operating_hours": [operating_hours],
            "sales_area_m2": [sales_area],
            "revenue": [revenue],
            "electricity_kwh": [electricity]
        })

        # Predictions
        predicted_electricity = (
            electricity_model.predict(
                electricity_input
            )[0]
        )

        predicted_water = (
            water_model.predict(
                water_input
            )[0]
        )

        st.write("")

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

        st.success(
            "Prediction completed successfully."
        )

        st.caption(
            "Predictions are generated using the trained "
            "Random Forest machine-learning models."
        )


# ============================================================
# SUSTAINABILITY
# ============================================================

elif page == "Sustainability":

    st.title("🌱 Sustainability & SDG Analysis")

    st.write(
        "Measure resource efficiency and connect SmartMart's "
        "operations with relevant Sustainable Development Goals."
    )

    st.divider()

    # --------------------------------------------------------
    # EFFICIENCY KPIs
    # --------------------------------------------------------

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

    st.write("")

    # --------------------------------------------------------
    # SDGs
    # --------------------------------------------------------

    st.subheader(
        "Relevant Sustainable Development Goals"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            "SDG 6 – Clean Water and Sanitation\n\n"
            "Monitor and reduce water consumption "
            "through improved resource efficiency."
        )

        st.info(
            "SDG 7 – Affordable and Clean Energy\n\n"
            "Monitor electricity consumption and "
            "improve energy efficiency."
        )

        st.info(
            "SDG 9 – Industry, Innovation and Infrastructure\n\n"
            "Use AI and machine learning to improve "
            "business resource management."
        )

    with col2:

        st.info(
            "SDG 12 – Responsible Consumption and Production\n\n"
            "Monitor raw materials, packaging, "
            "waste and operational resources."
        )

        st.info(
            "SDG 13 – Climate Action\n\n"
            "Reduce unnecessary energy and fuel "
            "consumption through better planning."
        )

    st.write("")

    # --------------------------------------------------------
    # SUSTAINABILITY CHART
    # --------------------------------------------------------

    st.subheader(
        "Resource Consumption Trends"
    )

    sustainability_data = df[
        [
            "date",
            "electricity_kwh",
            "water_m3",
            "waste_kg"
        ]
    ].melt(
        id_vars="date",
        var_name="Resource",
        value_name="Consumption"
    )

    fig = px.line(
        sustainability_data,
        x="date",
        y="Consumption",
        color="Resource",
        title="Electricity, Water and Waste Trends",
        markers=True
    )

    fig = apply_chart_theme(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "SmartMart AI/ML Minor Project"
)

st.sidebar.caption(
    "Business Resource & Sustainability Management"
)
