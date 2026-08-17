import os
import joblib
import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartMart Resource Manager",
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

    if not os.path.exists(DATA_FILE):
        st.error(
            f"Data file not found:\n{DATA_FILE}"
        )
        st.stop()

    data = pd.read_csv(DATA_FILE)

    if "date" in data.columns:
        data["date"] = pd.to_datetime(
            data["date"],
            errors="coerce"
        )

    return data


# ============================================================
# LOAD MACHINE LEARNING MODELS
# ============================================================

@st.cache_resource
def load_models():

    if not os.path.exists(ELECTRICITY_MODEL_FILE):
        st.error(
            "Electricity model not found:\n"
            f"{ELECTRICITY_MODEL_FILE}"
        )
        st.stop()

    if not os.path.exists(WATER_MODEL_FILE):
        st.error(
            "Water model not found:\n"
            f"{WATER_MODEL_FILE}"
        )
        st.stop()

    try:
        electricity_model = joblib.load(
            ELECTRICITY_MODEL_FILE
        )

        water_model = joblib.load(
            WATER_MODEL_FILE
        )

    except Exception as e:
        st.error(
            "Error loading machine-learning models."
        )
        st.exception(e)
        st.stop()

    return electricity_model, water_model


# ============================================================
# INITIALIZE DATA
# ============================================================

df = load_data()

electricity_model, water_model = load_models()


if df.empty:
    st.error("The SmartMart dataset is empty.")
    st.stop()


# Sort data by date if date exists
if "date" in df.columns:
    df = df.sort_values("date").reset_index(drop=True)


latest = df.iloc[-1]


# ============================================================
# CURRENCY SETTINGS
# ============================================================

st.sidebar.title("🏪 SmartMart")

currency = st.sidebar.selectbox(
    "💱 Display Currency",
    [
        "INR (₹)",
        "USD ($)",
        "EUR (€)"
    ]
)

currency_rates = {
    "INR (₹)": 1.00,
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
    """
    Convert and format financial values
    according to the selected currency.
    """

    try:
        return f"{symbol}{float(value) * rate:,.0f}"

    except (ValueError, TypeError):
        return f"{symbol}0"


# ============================================================
# PROFESSIONAL UI STYLE
# ============================================================

st.markdown(
    """
    <style>

    [data-testid="stAppViewContainer"] {
        background-color: #F3F4F6;
    }

    [data-testid="stHeader"] {
        background-color: #F3F4F6;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3, h4 {
        color: #111827 !important;
        font-weight: 700 !important;
    }

    p {
        color: #1F2937 !important;
    }

    label {
        color: #1F2937 !important;
    }

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }

    [data-testid="stMetricLabel"] {
        color: #4B5563 !important;
    }

    [data-testid="stMetricValue"] {
        color: #111827 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
    }

    [data-testid="stSidebar"] p {
        color: #1F2937 !important;
    }

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PLOTLY THEME
# ============================================================

def apply_chart_theme(fig):

    fig.update_layout(

        paper_bgcolor="#F3F4F6",

        plot_bgcolor="#E5E7EB",

        font=dict(
            family="Arial",
            color="#111827",
            size=13
        ),

        title=dict(
            font=dict(
                family="Arial",
                color="#111827",
                size=19
            ),
            x=0.02,
            xanchor="left"
        ),

        xaxis=dict(
            title_font=dict(
                color="#111827",
                size=14
            ),
            tickfont=dict(
                color="#111827",
                size=12
            ),
            gridcolor="#B8BEC8",
            linecolor="#6B7280",
            showline=True
        ),

        yaxis=dict(
            title_font=dict(
                color="#111827",
                size=14
            ),
            tickfont=dict(
                color="#111827",
                size=12
            ),
            gridcolor="#B8BEC8",
            linecolor="#6B7280",
            showline=True
        ),

        legend=dict(
            font=dict(
                color="#111827",
                size=12
            ),
            bgcolor="rgba(255,255,255,0.90)",
            bordercolor="#9CA3AF",
            borderwidth=1
        ),

        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#6B7280",
            font=dict(
                color="#111827",
                size=12
            )
        ),

        margin=dict(
            l=70,
            r=30,
            t=70,
            b=60
        )
    )

    return fig


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.divider()

st.sidebar.subheader("🧭 Navigation")


# ------------------------------------------------------------
# MAIN NAVIGATION
# ------------------------------------------------------------

page = st.sidebar.radio(
    "Main Section",
    [
        "📊 Dashboard",
        "💰 Financial Analysis",
        "📑 Balance Sheet",
        "🤖 AI Predictions",
        "🌱 Sustainability",
        "⚡ Resource Consumption"
    ],
    label_visibility="collapsed"
)


# ============================================================
# RESOURCE CONSUMPTION SUB-MENU
# ============================================================

resource_category = "📊 Overview"

if page == "⚡ Resource Consumption":

    st.sidebar.divider()

    st.sidebar.subheader(
        "⚡ Resource Categories"
    )

    resource_category = st.sidebar.radio(
        "Select Resource",
        [
            "📊 Overview",
            "⚡ Electricity",
            "💧 Water",
            "⛽ Fuel",
            "♻️ Waste"
        ],
        label_visibility="collapsed"
    )


# ============================================================
# PAGE HEADER
# ============================================================

st.title(
    "🏪 SmartMart Resource & Financial Management System"
)

st.write(
    """
    An AI/ML-based business resource management system
    for analyzing resource consumption, financial performance,
    and sustainability of a supermarket.
    """
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.header("📊 Business Dashboard")

    st.write(
        "Overview of SmartMart's latest business performance."
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Revenue",
            money(latest["revenue"])
        )

    with col2:
        st.metric(
            "📈 Net Profit",
            money(latest["net_profit"])
        )

    with col3:
        st.metric(
            "👥 Customers",
            f"{latest['customers']:,.0f}"
        )

    with col4:
        st.metric(
            "⚡ Resource Cost",
            money(latest["total_resource_cost"])
        )

    st.divider()

    # --------------------------------------------------------
    # REVENUE TREND
    # --------------------------------------------------------

    st.subheader("📈 Revenue Trend")

    fig = px.line(
        df,
        x="date",
        y="revenue",
        title="Revenue Trend",
        markers=True
    )

    fig.update_yaxes(
        title="Revenue",
        tickprefix=symbol
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=7)
    )

    st.plotly_chart(
        apply_chart_theme(fig),
        use_container_width=True
    )

    # --------------------------------------------------------
    # PROFIT TREND
    # --------------------------------------------------------

    st.subheader("📈 Net Profit Trend")

    fig = px.line(
        df,
        x="date",
        y="net_profit",
        title="Net Profit Trend",
        markers=True
    )

    fig.update_yaxes(
        title="Net Profit",
        tickprefix=symbol
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=7)
    )

    st.plotly_chart(
        apply_chart_theme(fig),
        use_container_width=True
    )


# ============================================================
# RESOURCE CONSUMPTION
# ============================================================

elif page == "⚡ Resource Consumption":

    st.header("⚡ Resource Consumption")

    st.write(
        "Select a resource category from the sidebar."
    )

    st.divider()

    # ========================================================
    # RESOURCE OVERVIEW
    # ========================================================

    if resource_category == "📊 Overview":

        st.subheader("📊 Resource Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "⚡ Electricity",
                f"{latest['electricity_kwh']:,.0f} kWh"
            )

        with col2:
            st.metric(
                "💧 Water",
                f"{latest['water_m3']:,.0f} m³"
            )

        with col3:
            st.metric(
                "⛽ Fuel",
                f"{latest['fuel_liters']:,.0f} L"
            )

        with col4:
            st.metric(
                "♻️ Waste",
                f"{latest['waste_kg']:,.0f} kg"
            )

        st.subheader(
            "📈 All Resource Consumption Trends"
        )

        resource_data = df[
            [
                "date",
                "electricity_kwh",
                "water_m3",
                "fuel_liters",
                "waste_kg"
            ]
        ].melt(
            id_vars="date",
            var_name="Resource",
            value_name="Consumption"
        )

        fig = px.line(
            resource_data,
            x="date",
            y="Consumption",
            color="Resource",
            title="Resource Consumption Overview",
            markers=True
        )

        fig.update_yaxes(
            title="Consumption"
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=6)
        )

        st.plotly_chart(
            apply_chart_theme(fig),
            use_container_width=True
        )

    # ========================================================
    # ELECTRICITY
    # ========================================================

    elif resource_category == "⚡ Electricity":

        st.subheader("⚡ Electricity Consumption")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Current",
                f"{latest['electricity_kwh']:,.0f} kWh"
            )

        with col2:

            average = df[
                "electricity_kwh"
            ].mean()

            st.metric(
                "Average",
                f"{average:,.0f} kWh"
            )

        with col3:

            maximum = df[
                "electricity_kwh"
            ].max()

            st.metric(
                "Maximum",
                f"{maximum:,.0f} kWh"
            )

        fig = px.line(
            df,
            x="date",
            y="electricity_kwh",
            title="Electricity Consumption Trend",
            markers=True
        )

        fig.update_yaxes(
            title="Electricity (kWh)"
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=7)
        )

        st.plotly_chart(
            apply_chart_theme(fig),
            use_container_width=True
        )

    # ========================================================
    # WATER
    # ========================================================

    elif resource_category == "💧 Water":

        st.subheader("💧 Water Consumption")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Current",
                f"{latest['water_m3']:,.0f} m³"
            )

        with col2:

            average = df[
                "water_m3"
            ].mean()

            st.metric(
                "Average",
                f"{average:,.0f} m³"
            )

        with col3:

            maximum = df[
                "water_m3"
            ].max()

            st.metric(
                "Maximum",
                f"{maximum:,.0f} m³"
            )

        fig = px.line(
            df,
            x="date",
            y="water_m3",
            title="Water Consumption Trend",
            markers=True
        )

        fig.update_yaxes(
            title="Water (m³)"
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=7)
        )

        st.plotly_chart(
            apply_chart_theme(fig),
            use_container_width=True
        )

    # ========================================================
    # FUEL
    # ========================================================

    elif resource_category == "⛽ Fuel":

        st.subheader("⛽ Fuel Consumption")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Current",
                f"{latest['fuel_liters']:,.0f} L"
            )

        with col2:

            average = df[
                "fuel_liters"
            ].mean()

            st.metric(
                "Average",
                f"{average:,.0f} L"
            )

        with col3:

            maximum = df[
                "fuel_liters"
            ].max()

            st.metric(
                "Maximum",
                f"{maximum:,.0f} L"
            )

        fig = px.line(
            df,
            x="date",
            y="fuel_liters",
            title="Fuel Consumption Trend",
            markers=True
        )

        fig.update_yaxes(
            title="Fuel (L)"
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=7)
        )

        st.plotly_chart(
            apply_chart_theme(fig),
            use_container_width=True
        )

    # ========================================================
    # WASTE
    # ========================================================

    elif resource_category == "♻️ Waste":

        st.subheader("♻️ Waste Generation")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Current",
                f"{latest['waste_kg']:,.0f} kg"
            )

        with col2:

            average = df[
                "waste_kg"
            ].mean()

            st.metric(
                "Average",
                f"{average:,.0f} kg"
            )

        with col3:

            maximum = df[
                "waste_kg"
            ].max()

            st.metric(
                "Maximum",
                f"{maximum:,.0f} kg"
            )

        fig = px.line(
            df,
            x="date",
            y="waste_kg",
            title="Waste Generation Trend",
            markers=True
        )

        fig.update_yaxes(
            title="Waste (kg)"
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=7)
        )

        st.plotly_chart(
            apply_chart_theme(fig),
            use_container_width=True
        )


# ============================================================
# FINANCIAL ANALYSIS
# ============================================================

elif page == "💰 Financial Analysis":

    st.header("💰 Financial Analysis")

    # --------------------------------------------------------
    # FINANCIAL KPI
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 Revenue",
            money(latest["revenue"])
        )

    with col2:
        st.metric(
            "📊 Operating Profit",
            money(latest["operating_profit"])
        )

    with col3:
        st.metric(
            "📈 Net Profit",
            money(latest["net_profit"])
        )

    st.divider()

    # --------------------------------------------------------
    # REVENUE VS PROFIT
    # --------------------------------------------------------

    st.subheader("📊 Revenue vs Net Profit")

    financial_data = df[
        [
            "date",
            "revenue",
            "net_profit"
        ]
    ].melt(
        id_vars="date",
        var_name="Metric",
        value_name="Amount"
    )

    fig = px.line(
        financial_data,
        x="date",
        y="Amount",
        color="Metric",
        title="Revenue vs Net Profit",
        markers=True
    )

    fig.update_yaxes(
        title="Amount",
        tickprefix=symbol
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6)
    )

    st.plotly_chart(
        apply_chart_theme(fig),
        use_container_width=True
    )

    # --------------------------------------------------------
    # RESOURCE COST
    # --------------------------------------------------------

    st.subheader("💸 Resource Cost Trend")

    fig = px.line(
        df,
        x="date",
        y="total_resource_cost",
        title="Total Resource Cost",
        markers=True
    )

    fig.update_yaxes(
        title="Resource Cost",
        tickprefix=symbol
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=7)
    )

    st.plotly_chart(
        apply_chart_theme(fig),
        use_container_width=True
    )

    # --------------------------------------------------------
    # COST BREAKDOWN
    # --------------------------------------------------------

    st.subheader("📊 Current Cost Breakdown")

    cost_data = pd.DataFrame({

        "Cost Type": [
            "Electricity",
            "Water",
            "Fuel",
            "Packaging",
            "Cleaning"
        ],

        "Cost": [
            float(latest["electricity_cost"]) * rate,
            float(latest["water_cost"]) * rate,
            float(latest["fuel_cost"]) * rate,
            float(latest["packaging_cost"]) * rate,
            float(latest["cleaning_cost"]) * rate
        ]
    })

    fig = px.bar(
        cost_data,
        x="Cost Type",
        y="Cost",
        title="Resource Cost Breakdown",
        text="Cost"
    )

    fig.update_yaxes(
        title="Cost",
        tickprefix=symbol
    )

    fig.update_traces(
        texttemplate=symbol + "%{text:,.0f}",
        textposition="outside"
    )

    st.plotly_chart(
        apply_chart_theme(fig),
        use_container_width=True
    )


# ============================================================
# BALANCE SHEET
# ============================================================

elif page == "📑 Balance Sheet":

    st.header("📑 Balance Sheet")

    # --------------------------------------------------------
    # ASSETS
    # --------------------------------------------------------

    st.subheader("🏢 Assets")

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

    assets_display["Amount"] = (
        assets_display["Amount"].apply(money)
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

    st.divider()

    # --------------------------------------------------------
    # LIABILITIES
    # --------------------------------------------------------

    st.subheader("🏦 Liabilities")

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

    liabilities_display["Amount"] = (
        liabilities_display["Amount"].apply(money)
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

    st.divider()

    # --------------------------------------------------------
    # EQUITY
    # --------------------------------------------------------

    st.subheader("📊 Equity")

    st.metric(
        "Total Equity",
        money(latest["total_equity"])
    )

    st.divider()

    # --------------------------------------------------------
    # ACCOUNTING EQUATION
    # --------------------------------------------------------

    st.subheader("🧮 Accounting Equation")

    st.write(
        "Assets = Liabilities + Equity"
    )

    left, right = st.columns(2)

    with left:

        st.metric(
            "Assets",
            money(latest["total_assets"])
        )

    with right:

        liabilities_equity = (
            float(latest["total_liabilities"])
            + float(latest["total_equity"])
        )

        st.metric(
            "Liabilities + Equity",
            money(liabilities_equity)
        )

    difference = (
        float(latest["total_assets"])
        - liabilities_equity
    )

    if abs(difference) < 1:

        st.success(
            "✓ The balance sheet is balanced."
        )

    else:

        st.warning(
            f"Difference: {money(difference)}"
        )


# ============================================================
# AI PREDICTIONS
# ============================================================

elif page == "🤖 AI Predictions":

    st.header(
        "🤖 AI Resource Consumption Prediction"
    )

    st.write(
        """
        Enter the expected business conditions below.
        The trained machine-learning models will estimate
        electricity and water consumption.
        """
    )

    st.divider()

    # --------------------------------------------------------
    # INPUT SECTION
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        customers = st.number_input(
            "👥 Expected Customers",
            min_value=1000,
            max_value=100000,
            value=20000,
            step=1000
        )

        employees = st.number_input(
            "👷 Employees",
            min_value=1,
            max_value=500,
            value=50,
            step=1
        )

        operating_hours = st.number_input(
            "🕐 Operating Hours per Day",
            min_value=1.0,
            max_value=24.0,
            value=14.0,
            step=0.5
        )

        sales_area = st.number_input(
            "🏪 Sales Area (m²)",
            min_value=100.0,
            max_value=10000.0,
            value=2500.0,
            step=100.0
        )

    with col2:

        revenue = st.number_input(
            "💰 Expected Revenue (₹)",
            min_value=100000.0,
            max_value=100000000.0,
            value=15000000.0,
            step=100000.0
        )

        water = st.number_input(
            "💧 Expected Water Consumption (m³)",
            min_value=100.0,
            max_value=10000.0,
            value=1500.0,
            step=100.0
        )

        fuel = st.number_input(
            "⛽ Expected Fuel Consumption (L)",
            min_value=100.0,
            max_value=50000.0,
            value=4000.0,
            step=100.0
        )

        electricity = st.number_input(
            "⚡ Expected Electricity (kWh)",
            min_value=10000.0,
            max_value=1000000.0,
            value=100000.0,
            step=5000.0
        )

    st.divider()

    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    if st.button(
        "🔮 Predict Resource Consumption",
        use_container_width=True
    ):

        try:

            # ------------------------------------------------
            # ELECTRICITY MODEL INPUT
            # ------------------------------------------------

            electricity_input = pd.DataFrame({

                "customers": [customers],

                "employees": [employees],

                "operating_hours": [operating_hours],

                "sales_area_m2": [sales_area],

                "revenue": [revenue],

                "water_m3": [water],

                "fuel_liters": [fuel]
            })

            # ------------------------------------------------
            # WATER MODEL INPUT
            # ------------------------------------------------

            water_input = pd.DataFrame({

                "customers": [customers],

                "employees": [employees],

                "operating_hours": [operating_hours],

                "sales_area_m2": [sales_area],

                "revenue": [revenue],

                "electricity_kwh": [electricity]
            })

            # ------------------------------------------------
            # ELECTRICITY PREDICTION
            # ------------------------------------------------

            predicted_electricity = (
                electricity_model.predict(
                    electricity_input
                )[0]
            )

            # ------------------------------------------------
            # WATER PREDICTION
            # ------------------------------------------------

            predicted_water = (
                water_model.predict(
                    water_input
                )[0]
            )

            # ------------------------------------------------
            # RESULTS
            # ------------------------------------------------

            st.subheader(
                "🔮 Prediction Results"
            )

            result1, result2 = st.columns(2)

            with result1:

                st.metric(
                    "⚡ Predicted Electricity",
                    f"{predicted_electricity:,.0f} kWh"
                )

            with result2:

                st.metric(
                    "💧 Predicted Water",
                    f"{predicted_water:,.0f} m³"
                )

            st.success(
                "Prediction completed using the trained "
                "Random Forest machine-learning models."
            )

        except Exception as e:

            st.error(
                "The prediction could not be completed. "
                "Please verify that the input columns match "
                "the features used when training the models."
            )

            st.exception(e)


# ============================================================
# SUSTAINABILITY
# ============================================================

elif page == "🌱 Sustainability":

    st.header(
        "🌱 Sustainability & SDG Analysis"
    )

    # --------------------------------------------------------
    # EFFICIENCY METRICS
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
            "⚡ Electricity / Customer",
            f"{electricity_efficiency:.2f} kWh"
        )

    with col2:

        st.metric(
            "💧 Water / Customer",
            f"{water_efficiency:.3f} m³"
        )

    with col3:

        st.metric(
            "💰 Resource Cost / Revenue",
            f"{resource_cost:.2f}%"
        )

    st.divider()

    # --------------------------------------------------------
    # SDG ANALYSIS
    # --------------------------------------------------------

    st.subheader(
        "🌍 Relevant Sustainable Development Goals"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            """
            **SDG 6 – Clean Water and Sanitation**

            Monitor and reduce water consumption.
            """
        )

        st.info(
            """
            **SDG 7 – Affordable and Clean Energy**

            Monitor electricity consumption and
            improve energy efficiency.
            """
        )

        st.info(
            """
            **SDG 9 – Industry, Innovation and Infrastructure**

            Use AI/ML to improve resource management.
            """
        )

    with col2:

        st.info(
            """
            **SDG 12 – Responsible Consumption and Production**

            Monitor raw materials, packaging and waste.
            """
        )

        st.info(
            """
            **SDG 13 – Climate Action**

            Reduce unnecessary energy and fuel consumption.
            """
        )

    # --------------------------------------------------------
    # SUSTAINABILITY CHART
    # --------------------------------------------------------

    st.subheader(
        "📈 Resource Consumption Trends"
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
        title="Resource Consumption Trends",
        markers=True
    )

    fig.update_yaxes(
        title="Consumption"
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6)
    )

    st.plotly_chart(
        apply_chart_theme(fig),
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
