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
    data = pd.read_csv(DATA_FILE)

    if "date" in data.columns:
        data["date"] = pd.to_datetime(data["date"])

    return data


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

latest = df.iloc[-1]


# ============================================================
# CURRENCY
# ============================================================

st.sidebar.title("🏪 SmartMart")

currency = st.sidebar.selectbox(
    "Display Currency",
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
    return f"{symbol}{float(value) * rate:,.0f}"


# ============================================================
# PROFESSIONAL UI STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* Main application background */
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

    /* Headings */
    h1, h2, h3, h4 {
        color: #111827 !important;
    }

    /* Normal text */
    p, label {
        color: #1F2937 !important;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-radius: 12px;
        padding: 15px;
    }

    [data-testid="stMetricLabel"] {
        color: #4B5563 !important;
    }

    [data-testid="stMetricValue"] {
        color: #111827 !important;
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

        # Light chart backgrounds
        paper_bgcolor="#F3F4F6",
        plot_bgcolor="#E5E7EB",

        # Main text
        font=dict(
            family="Arial",
            color="#111827",
            size=13
        ),

        # Chart title
        title=dict(
            font=dict(
                family="Arial",
                color="#111827",
                size=19
            ),
            x=0.02,
            xanchor="left"
        ),

        # X axis
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

        # Y axis
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

        # Legend
        legend=dict(
            font=dict(
                color="#111827",
                size=12
            ),
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="#9CA3AF",
            borderwidth=1
        ),

        # Hover box
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
# TITLE
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
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.divider()

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


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.header("📊 Business Dashboard")

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

    # Revenue
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

    # Profit
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

elif page == "Resource Consumption":

    st.header("⚡ Resource Consumption")

    st.write(
        "Select a resource category to analyze its consumption."
    )

    # --------------------------------------------------------
    # RESOURCE CATEGORY SELECTOR
    # --------------------------------------------------------

    resource_category = st.selectbox(
        "Select Resource Category",
        [
            "📊 All Resources",
            "⚡ Electricity",
            "💧 Water",
            "⛽ Fuel",
            "♻️ Waste"
        ]
    )

    st.divider()

    # --------------------------------------------------------
    # ALL RESOURCES
    # --------------------------------------------------------

    if resource_category == "📊 All Resources":

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

        st.subheader("📈 Resource Consumption Trends")

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
            title="All Resource Consumption",
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


    # --------------------------------------------------------
    # ELECTRICITY
    # --------------------------------------------------------

    elif resource_category == "⚡ Electricity":

        st.subheader("⚡ Electricity Consumption")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Current Electricity",
                f"{latest['electricity_kwh']:,.0f} kWh"
            )

        with col2:

            electricity_average = df[
                "electricity_kwh"
            ].mean()

            st.metric(
                "Average Electricity",
                f"{electricity_average:,.0f} kWh"
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


    # --------------------------------------------------------
    # WATER
    # --------------------------------------------------------

    elif resource_category == "💧 Water":

        st.subheader("💧 Water Consumption")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Current Water",
                f"{latest['water_m3']:,.0f} m³"
            )

        with col2:

            water_average = df[
                "water_m3"
            ].mean()

            st.metric(
                "Average Water",
                f"{water_average:,.0f} m³"
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


    # --------------------------------------------------------
    # FUEL
    # --------------------------------------------------------

    elif resource_category == "⛽ Fuel":

        st.subheader("⛽ Fuel Consumption")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Current Fuel",
                f"{latest['fuel_liters']:,.0f} L"
            )

        with col2:

            fuel_average = df[
                "fuel_liters"
            ].mean()

            st.metric(
                "Average Fuel",
                f"{fuel_average:,.0f} L"
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


    # --------------------------------------------------------
    # WASTE
    # --------------------------------------------------------

    elif resource_category == "♻️ Waste":

        st.subheader("♻️ Waste Generation")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Current Waste",
                f"{latest['waste_kg']:,.0f} kg"
            )

        with col2:

            waste_average = df[
                "waste_kg"
            ].mean()

            st.metric(
                "Average Waste",
                f"{waste_average:,.0f} kg"
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

elif page == "Financial Analysis":

    st.header("💰 Financial Analysis")

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

    # Revenue vs Profit
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

    # Resource cost
    st.subheader("💸 Resource Cost")

    fig = px.line(
        df,
        x="date",
        y="total_resource_cost",
        title="Resource Cost Trend",
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

    # Cost breakdown
    st.subheader("📊 Cost Breakdown")

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
        title="Current Resource Cost Breakdown",
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

elif page == "Balance Sheet":

    st.header("📑 Balance Sheet")

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
    ].apply(money)

    st.dataframe(
        assets_display,
        use_container_width=True,
        hide_index=True
    )

    st.metric(
        "Total Assets",
        money(latest["total_assets"])
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

    liabilities_display = liabilities.copy()

    liabilities_display["Amount"] = liabilities_display[
        "Amount"
    ].apply(money)

    st.dataframe(
        liabilities_display,
        use_container_width=True,
        hide_index=True
    )

    st.metric(
        "Total Liabilities",
        money(latest["total_liabilities"])
    )

    st.subheader("Equity")

    st.metric(
        "Total Equity",
        money(latest["total_equity"])
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
            money(latest["total_assets"])
        )

    with right:

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
            "✓ The balance sheet is balanced."
        )

    else:

        st.warning(
            f"Difference: {money(difference)}"
        )


# ============================================================
# AI PREDICTIONS
# ============================================================

elif page == "AI Predictions":

    st.header(
        "🤖 AI Resource Consumption Prediction"
    )

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

    if st.button(
        "🔮 Predict Resource Consumption",
        use_container_width=True
    ):

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
            "Prediction completed using the trained "
            "Random Forest machine-learning models."
        )


# ============================================================
# SUSTAINABILITY
# ============================================================

elif page == "Sustainability":

    st.header(
        "🌱 Sustainability & SDG Analysis"
    )

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
