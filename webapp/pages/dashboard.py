import streamlit as st
import plotly.express as px

from utils.chart_theme import apply_chart_theme


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard(
    df,
    latest,
    money,
    symbol
):

    st.header("📊 Business Dashboard")

    st.write(
        "Overview of SmartMart's latest business performance."
    )


    # ========================================================
    # KPI CARDS
    # ========================================================

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


    # ========================================================
    # REVENUE TREND
    # ========================================================

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


    # ========================================================
    # PROFIT TREND
    # ========================================================

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
