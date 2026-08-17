import os
import streamlit as st

from utils.data_loader import load_data
from utils.model_loader import load_models
from utils.currency import setup_currency
from utils.chart_theme import apply_custom_css

from pages.dashboard import show_dashboard
from pages.financial_analysis import show_financial_analysis
from pages.balance_sheet import show_balance_sheet
from pages.ai_predictions import show_ai_predictions
from pages.sustainability import show_sustainability
from pages.resource_consumption import show_resource_consumption


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

df = load_data(DATA_FILE)


# ============================================================
# LOAD MACHINE LEARNING MODELS
# ============================================================

electricity_model, water_model = load_models(
    ELECTRICITY_MODEL_FILE,
    WATER_MODEL_FILE
)


# ============================================================
# LATEST DATA
# ============================================================

latest = df.iloc[-1]


# ============================================================
# CURRENCY
# ============================================================

currency, rate, symbol, money = setup_currency()


# ============================================================
# PROFESSIONAL UI STYLE
# ============================================================

apply_custom_css()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏪 SmartMart")

st.sidebar.divider()

st.sidebar.subheader("🧭 Navigation")


# ============================================================
# MAIN NAVIGATION
# ============================================================

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
# PAGE ROUTING
# ============================================================

if page == "📊 Dashboard":

    show_dashboard(
        df=df,
        latest=latest,
        money=money,
        symbol=symbol
    )


elif page == "💰 Financial Analysis":

    show_financial_analysis(
        df=df,
        latest=latest,
        money=money,
        symbol=symbol,
        rate=rate
    )


elif page == "📑 Balance Sheet":

    show_balance_sheet(
        latest=latest,
        money=money
    )


elif page == "🤖 AI Predictions":

    show_ai_predictions(
        electricity_model=electricity_model,
        water_model=water_model
    )


elif page == "🌱 Sustainability":

    show_sustainability(
        df=df,
        latest=latest
    )


elif page == "⚡ Resource Consumption":

    show_resource_consumption(
        df=df,
        latest=latest,
        resource_category=resource_category
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
