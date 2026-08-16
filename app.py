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
    BASE_DIR, "data", "raw", "smartmart_data.csv"
)

ELECTRICITY_MODEL_FILE = os.path.join(
    BASE_DIR, "models", "electricity_model.pkl"
)

WATER_MODEL_FILE = os.path.join(
    BASE_DIR, "models", "water_model.pkl"
)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    data = pd.read_csv(DATA_FILE)
    data["date"] = pd.to_datetime(data["date"])
    return data.sort_values("date")


@st.cache_resource
def load_models():
    electricity_model = joblib.load(ELECTRICITY_MODEL_FILE)
    water_model = joblib.load(WATER_MODEL_FILE)
    return electricity_model, water_model


df = load_data()
electricity_model, water_model = load_models()
latest = df.iloc[-1]

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
# PROFESSIONAL PLOTLY THEME
# ============================================================
def apply_chart_theme(fig):
    """
    Light-grey chart background with dark readable text.
    This fixes the previous white-text-on-dark-chart problem.
    """

    fig.update_layout(
        # Outside and inside chart backgrounds
        paper_bgcolor="#E5E7EB",
        plot_bgcolor="#D1D5DB",

        # Main text
        font=dict(
            family="Arial, sans-serif",
            color="#111827",
            size=13
        ),

        # Title
        title=dict(
            font=dict(
                family="Arial, sans-serif",
                color="#111827",
                size=18
            ),
            x=0.02,
            xanchor="left"
        ),

        # X axis
        xaxis=dict(
            title_font=dict(
                family="Arial, sans-serif",
                color="#111827",
                size=13
            ),
            tickfont=dict(
                family="Arial, sans-serif",
                color="#1F2937",
                size=11
            ),
            gridcolor="#B6BDC8",
            linecolor="#6B7280",
            zerolinecolor="#9CA3AF",
            showline=True
        ),

        # Y axis
        yaxis=dict(
            title_font=dict(
                family="Arial, sans-serif",
                color="#111827",
                size=13
            ),
            tickfont=dict(
                family="Arial, sans-serif",
                color="#1F2937",
                size=11
            ),
            gridcolor="#B6BDC8",
            linecolor="#6B7280",
            zerolinecolor="#9CA3AF",
            showline=True
        ),

        # Legend
        legend=dict(
            font=dict(
                family="Arial, sans-serif",
                color="#111827",
                size=11
            ),
            bgcolor="rgba(229,231,235,0.85)",
            bordercolor="#9CA3AF",
            borderwidth=1
        ),

        # Hover box
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#6B7280",
            font=dict(
                family="Arial, sans-serif",
                color="#111827",
                size=12
            )
        ),

        margin=dict(
            l=70,
            r=30,
            t=65,
            b=65
        ),

        hovermode="x unified"
    )

    # Make line-chart labels, when present, readable.
    fig.update_traces(
        selector=dict(type="scatter"),
        textfont=dict(
            color="#111827",
            size=11
        )
    )

    # Make bar labels readable.
    fig.update_traces(
        selector=dict(type="bar"),
        textfont=dict(
            color="#111827",
            size=11
        )
    )

    return fig


# ============================================================
# GENERAL STREAMLIT STYLING
# ============================================================
st.markdown(
    """
    <style>
        .main {
            background-color: #F3F4F6;
        }

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

        h1, h2, h3 {
            color: #111827 !important;
        }

        p, label, span {
            color: #1F2937;
        }

        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #D1D5DB;
            border-radius: 12px;
            padding: 14px;
        }

        [data-testid="stMetricLabel"] {
            color: #4B5563 !important;
        }

        [data-testid="stMetricValue"] {
            color: #111827 !important;
        }

        .stDataFrame {
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("🏪 SmartMart")
st.sidebar.caption("Business Intelligence & Resource Management")

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
st.sidebar.info("Supermarket / Retail Business")

st.sidebar.divider()

st.sidebar.caption("AI & Data Science Minor Project")
st.sidebar.caption("Royal Global University")

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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Revenue", money(latest["revenue"]))

    with col2:
        st.metric("Net Profit", money(latest["net_profit"]))

    with col3:
        st.metric("Customers", f"{latest['customers']:,.0f}")

    with col4:
        st.metric("Resource Cost", money(latest["total_resource_cost"]))

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
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
            marker=dict(size=7),
            hovertemplate="Date: %{x|%b %Y}<br>Revenue: "
                          + symbol + "%{y:,.0f}<extra></extra>"
        )

        st.plotly_chart(
            apply_chart_theme(fig),
            use_container_width=True
        )

    with col2:
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
            marker=dict(size=7),
            hovertemplate="Date: %{x|%b %Y}<br>Net Profit: "
                          + symbol + "%{y:,.0f}<extra></extra>"
        )

        st.plotly_chart(
            apply_chart_theme(fig),
            use_container_width=True
        )

    st.subheader("Business Health")

    profit_margin = (
        latest["net_profit"] / latest["revenue"] * 100
    )

    resource_percentage = latest["resource_cost_percentage"]
    electricity_per_customer = latest["electricity_per_customer"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Net Profit Margin", f"{profit_margin:.2f}%")

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
        "Monitor electricity, water, fuel and waste consumption."
    )

    st.divider()

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

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(
            df,
            x="date",
            y="electricity_kwh",
            title="Electricity Consumption",
            markers=True
        )
        fig.update_yaxes(title="Electricity (kWh)")
        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=7)
        )
        st.plotly_chart(
            apply_chart_theme(fig),
            use_container_width=True
        )

    with col2:
        fig = px.line(
            df,
            x="date",
            y="water_m3",
            title="Water Consumption",
            markers=True
        )
        fig.update_yaxes(title="Water (m³)")
        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=7)
        )
        st.plotly_chart(
            apply_chart_theme(fig),
            use_container_width=True
        )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(
            df,
            x="date",
            y="fuel_liters",
            title="Fuel Consumption",
            markers=True
        )
        fig.update_yaxes(title="Fuel (Liters)")
        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=7)
        )
        st.plotly_chart(
            apply_chart_theme(fig),
            use_container_width=True
        )

    with col2:
        fig = px.line(
            df,
            x="date",
            y="waste_kg",
            title="Waste Generation",
            markers=True
        )
        fig.update_yaxes(title="Waste (kg)")
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

    st.title("💰 Financial Analysis")

    st.write(
        "Analyze revenue, operating profit, net profit and "
        "resource-related business costs."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Revenue", money(latest["revenue"]))

    with col2:
        st.metric(
            "Operating Profit",
            money(latest["operating_profit"])
        )

    with col3:
        st.metric("Net Profit", money(latest["net_profit"]))

    st.write("")

    financial_long = df[
        ["date", "revenue", "operating_profit", "net_profit"]
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

    fig = px.area(
        df,
        x="date",
        y="total_resource_cost",
        title="Total Resource Cost Trend"
    )

    fig.update_yaxes(
        title="Resource Cost",
        tickprefix=symbol
    )

    st.plotly_chart(
        apply_chart_theme(fig),
        use_container_width=True
    )

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

    st.title("📑 Balance Sheet")

    st.write(
        "Financial position based on assets, liabilities and equity."
    )

    st.divider()

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
    assets_display["Amount"] = assets_display["Amount"].apply(money)

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
    liabilities_display["Amount"] = liabilities_display["Amount"].apply(money)

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

    st.subheader("Equity")

    st.metric(
        "Total Equity",
        money(latest["total_equity"])
    )

    st.divider()

    st.subheader("Accounting Equation")

    st.info("Assets = Liabilities + Equity")

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
        latest["total_assets"] - liabilities_equity
    )

    if abs(difference) < 1:
        st.success("✓ Balance sheet is balanced.")
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

    if st.button(
        "🔮 Run AI Prediction",
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

        predicted_electricity = electricity_model.predict(
            electricity_input
        )[0]

        predicted_water = water_model.predict(
            water_input
        )[0]

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

        st.success("Prediction completed successfully.")

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

    electricity_efficiency = latest["electricity_per_customer"]
    water_efficiency = latest["water_per_customer"]
    resource_cost = latest["resource_cost_percentage"]

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

    st.subheader("Relevant Sustainable Development Goals")

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
            "Monitor raw materials, packaging, waste "
            "and operational resources."
        )

        st.info(
            "SDG 13 – Climate Action\n\n"
            "Reduce unnecessary energy and fuel "
            "consumption through better planning."
        )

    st.write("")

    st.subheader("Resource Consumption Trends")

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

    fig.update_yaxes(title="Consumption")

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
st.sidebar.caption("SmartMart AI/ML Minor Project")
st.sidebar.caption("Business Resource & Sustainability Management")


path = path("/mnt/data/app.py")
path.write_text(app_code, encoding="utf-8")
print(f"Created: {path}")
print(f"Lines: {len(app_code.splitlines())}")
