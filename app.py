import os
import joblib
import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartMart | Business Intelligence",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL UI STYLE
# ============================================================

st.markdown("""
<style>

    /* Main application */
    .stApp {
        background-color: #f5f7fa;
    }

    /* Remove extra top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }

    section[data-testid="stSidebar"] * {
        color: #f9fafb;
    }

    /* Brand */
    .brand {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 3px;
    }

    .brand-subtitle {
        font-size: 12px;
        color: #9ca3af;
        margin-bottom: 25px;
    }

    /* Page title */
    .page-title {
        font-size: 32px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 4px;
    }

    .page-subtitle {
        color: #6b7280;
        font-size: 15px;
        margin-bottom: 25px;
    }

    /* KPI Cards */
    .kpi-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .kpi-label {
        color: #6b7280;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: #111827;
        font-size: 25px;
        font-weight: 800;
    }

    .kpi-description {
        color: #9ca3af;
        font-size: 12px;
        margin-top: 7px;
    }

    /* Section cards */
    .section-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    /* Status */
    .status-good {
        background: #ecfdf5;
        color: #047857;
        padding: 8px 14px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
    }

    .status-info {
        background: #eff6ff;
        color: #1d4ed8;
        padding: 8px 14px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
    }

    /* AI badge */
    .ai-badge {
        background: #eef2ff;
        color: #4338ca;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
    }

    /* SDG cards */
    .sdg-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 17px;
        min-height: 145px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }

    .sdg-number {
        font-size: 12px;
        font-weight: 800;
        color: #047857;
        margin-bottom: 7px;
    }

    .sdg-title {
        font-weight: 700;
        color: #111827;
        margin-bottom: 7px;
    }

    .sdg-text {
        color: #6b7280;
        font-size: 12px;
        line-height: 1.5;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 9px;
        font-weight: 700;
        min-height: 42px;
    }

    /* Dataframes */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 12px;
        padding-top: 30px;
        padding-bottom: 10px;
    }

</style>
""", unsafe_allow_html=True)


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
# CURRENCY SETTINGS
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
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">🏪 SmartMart</div>
        <div class="brand-subtitle">
        Business Intelligence Platform
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### Navigation")

    page = st.radio(
        "",
        [
            "Overview",
            "Resource Management",
            "Financial Analysis",
            "Balance Sheet",
            "AI Forecast",
            "Sustainability"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("### Business Model")

    st.info(
        "Supermarket / Retail Business"
    )

    st.markdown("---")

    st.caption("SmartMart AI/ML Minor Project")
    st.caption("RGU • Artificial Intelligence & Data Science")


# ============================================================
# HEADER FUNCTION
# ============================================================

def page_header(title, subtitle):

    st.markdown(
        f"""
        <div class="page-title">{title}</div>
        <div class="page-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    page_header(
        "Business Overview",
        "Monitor financial performance, customers and operational resource efficiency."
    )

    latest = df.iloc[-1]

    # KPI ROW
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">TOTAL REVENUE</div>
                <div class="kpi-value">{money(latest['revenue'])}</div>
                <div class="kpi-description">Latest business revenue</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">NET PROFIT</div>
                <div class="kpi-value">{money(latest['net_profit'])}</div>
                <div class="kpi-description">Latest net profit</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">CUSTOMERS</div>
                <div class="kpi-value">{latest['customers']:,.0f}</div>
                <div class="kpi-description">Latest customer volume</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">RESOURCE COST</div>
                <div class="kpi-value">{money(latest['total_resource_cost'])}</div>
                <div class="kpi-description">Operational resource cost</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # PERFORMANCE
    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.subheader("Revenue Performance")

        revenue_chart = df.set_index("date")[["revenue"]]

        st.line_chart(revenue_chart)

        st.markdown("</div>", unsafe_allow_html=True)

    with right:

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.subheader("Profit Performance")

        profit_chart = df.set_index("date")[["net_profit"]]

        st.line_chart(profit_chart)

        st.markdown("</div>", unsafe_allow_html=True)

    # BUSINESS HEALTH
    st.subheader("Business Health")

    col1, col2, col3 = st.columns(3)

    profit_margin = (
        latest["net_profit"] / latest["revenue"] * 100
        if latest["revenue"] != 0 else 0
    )

    resource_percentage = latest["resource_cost_percentage"]

    with col1:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">NET PROFIT MARGIN</div>
                <div class="kpi-value">{profit_margin:.2f}%</div>
                <div class="kpi-description">
                    Net profit as percentage of revenue
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">RESOURCE COST / REVENUE</div>
                <div class="kpi-value">{resource_percentage:.2f}%</div>
                <div class="kpi-description">
                    Resource cost contribution
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">ELECTRICITY / CUSTOMER</div>
                <div class="kpi-value">
                    {latest['electricity_per_customer']:.2f} kWh
                </div>
                <div class="kpi-description">
                    Operational energy efficiency
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# RESOURCE MANAGEMENT
# ============================================================

elif page == "Resource Management":

    page_header(
        "Resource Management",
        "Track electricity, water, fuel and waste consumption across the supermarket."
    )

    latest = df.iloc[-1]

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

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.subheader("Electricity Consumption")

        electricity_chart = df.set_index("date")[["electricity_kwh"]]

        st.line_chart(electricity_chart)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.subheader("Water Consumption")

        water_chart = df.set_index("date")[["water_m3"]]

        st.line_chart(water_chart)

        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.subheader("Fuel Consumption")

        fuel_chart = df.set_index("date")[["fuel_liters"]]

        st.line_chart(fuel_chart)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.subheader("Waste Generation")

        waste_chart = df.set_index("date")[["waste_kg"]]

        st.line_chart(waste_chart)

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FINANCIAL ANALYSIS
# ============================================================

elif page == "Financial Analysis":

    page_header(
        "Financial Analysis",
        "Analyze revenue, profitability and operational resource costs."
    )

    latest = df.iloc[-1]

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

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.subheader("Revenue vs Net Profit")

        financial_chart = df.set_index("date")[
            ["revenue", "net_profit"]
        ]

        st.line_chart(financial_chart)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.subheader("Resource Cost Trend")

        resource_chart = df.set_index("date")[
            ["total_resource_cost"]
        ]

        st.line_chart(resource_chart)

        st.markdown("</div>", unsafe_allow_html=True)

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
            latest["electricity_cost"] * rate,
            latest["water_cost"] * rate,
            latest["fuel_cost"] * rate,
            latest["packaging_cost"] * rate,
            latest["cleaning_cost"] * rate
        ]
    })

    st.bar_chart(
        cost_data.set_index("Cost Type")
    )


# ============================================================
# BALANCE SHEET
# ============================================================

elif page == "Balance Sheet":

    page_header(
        "Balance Sheet",
        "Review assets, liabilities and equity for the supermarket business."
    )

    latest = df.iloc[-1]

    # Assets
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
            latest["land_value"] * rate,
            latest["building_value"] * rate,
            latest["equipment_value"] * rate,
            latest["inventory"] * rate,
            latest["cash"] * rate,
            latest["accounts_receivable"] * rate
        ]
    })

    assets_display = assets.copy()

    assets_display["Amount"] = assets_display["Amount"].apply(
        lambda x: f"{symbol}{x:,.0f}"
    )

    st.dataframe(
        assets_display,
        use_container_width=True,
        hide_index=True
    )

    total_assets = latest["total_assets"]

    st.metric(
        "Total Assets",
        money(total_assets)
    )

    st.write("")

    # Liabilities
    st.subheader("Liabilities")

    liabilities = pd.DataFrame({
        "Liability": [
            "Bank Loan",
            "Accounts Payable"
        ],
        "Amount": [
            latest["bank_loan"] * rate,
            latest["accounts_payable"] * rate
        ]
    })

    liabilities_display = liabilities.copy()

    liabilities_display["Amount"] = liabilities_display["Amount"].apply(
        lambda x: f"{symbol}{x:,.0f}"
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

    # Equity
    st.subheader("Equity")

    st.metric(
        "Total Equity",
        money(latest["total_equity"])
    )

    st.divider()

    # Accounting equation
    st.subheader("Accounting Equation")

    st.info(
        "Assets = Liabilities + Equity"
    )

    left, right = st.columns(2)

    with left:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">TOTAL ASSETS</div>
                <div class="kpi-value">{money(latest['total_assets'])}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">LIABILITIES + EQUITY</div>
                <div class="kpi-value">
                    {money(latest['total_liabilities'] + latest['total_equity'])}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.success(
        "✓ The balance sheet is balanced."
    )


# ============================================================
# AI FORECAST
# ============================================================

elif page == "AI Forecast":

    page_header(
        "AI Resource Forecast",
        "Use trained machine-learning models to estimate future resource consumption."
    )

    st.markdown(
        '<span class="ai-badge">AI / MACHINE LEARNING</span>',
        unsafe_allow_html=True
    )

    st.write("")

    st.info(
        "The system uses trained Random Forest models to estimate "
        "electricity and water consumption based on business operating conditions."
    )

    # Inputs
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
        "Run AI Prediction",
        type="primary",
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

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">PREDICTED ELECTRICITY</div>
                    <div class="kpi-value">
                        {predicted_electricity:,.0f} kWh
                    </div>
                    <div class="kpi-description">
                        Estimated future electricity consumption
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">PREDICTED WATER</div>
                    <div class="kpi-value">
                        {predicted_water:,.0f} m³
                    </div>
                    <div class="kpi-description">
                        Estimated future water consumption
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.success(
            "Prediction completed successfully using the trained Random Forest models."
        )


# ============================================================
# SUSTAINABILITY
# ============================================================

elif page == "Sustainability":

    page_header(
        "Sustainability & SDG Analysis",
        "Measure resource efficiency and connect business operations with the UN Sustainable Development Goals."
    )

    latest = df.iloc[-1]

    electricity_efficiency = latest["electricity_per_customer"]

    water_efficiency = latest["water_per_customer"]

    resource_cost = latest["resource_cost_percentage"]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">ELECTRICITY / CUSTOMER</div>
                <div class="kpi-value">
                    {electricity_efficiency:.2f} kWh
                </div>
                <div class="kpi-description">
                    Energy efficiency indicator
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">WATER / CUSTOMER</div>
                <div class="kpi-value">
                    {water_efficiency:.3f} m³
                </div>
                <div class="kpi-description">
                    Water efficiency indicator
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">RESOURCE COST / REVENUE</div>
                <div class="kpi-value">
                    {resource_cost:.2f}%
                </div>
                <div class="kpi-description">
                    Resource cost efficiency
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.subheader("Sustainable Development Goals")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="sdg-card">
                <div class="sdg-number">SDG 6</div>
                <div class="sdg-title">
                    Clean Water & Sanitation
                </div>
                <div class="sdg-text">
                    Monitor and reduce water consumption
                    through resource efficiency.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="sdg-card">
                <div class="sdg-number">SDG 7</div>
                <div class="sdg-title">
                    Affordable & Clean Energy
                </div>
                <div class="sdg-text">
                    Monitor electricity consumption and
                    improve energy efficiency.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="sdg-card">
                <div class="sdg-number">SDG 9</div>
                <div class="sdg-title">
                    Industry & Innovation
                </div>
                <div class="sdg-text">
                    Apply AI and machine learning to
                    improve business resource management.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="sdg-card">
                <div class="sdg-number">SDG 12</div>
                <div class="sdg-title">
                    Responsible Consumption
                </div>
                <div class="sdg-text">
                    Monitor raw materials, packaging,
                    waste and operational resources.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="sdg-card">
                <div class="sdg-number">SDG 13</div>
                <div class="sdg-title">
                    Climate Action
                </div>
                <div class="sdg-text">
                    Reduce unnecessary energy and fuel
                    consumption through better planning.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.subheader("Resource Consumption Trends")

    sustainability_chart = df.set_index("date")[
        [
            "electricity_kwh",
            "water_m3",
            "waste_kg"
        ]
    ]

    st.line_chart(sustainability_chart)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        SmartMart AI/ML • Business Resource & Sustainability Management
        <br>
        Developed as an AI & Data Science Minor Project
    </div>
    """,
    unsafe_allow_html=True
)
