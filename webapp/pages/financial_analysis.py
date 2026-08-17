import streamlit as st
import pandas as pd
import plotly.express as px

from utils.chart_theme import apply_chart_theme


# ============================================================
# FINANCIAL ANALYSIS
# ============================================================

def show_financial_analysis(
    df,
    latest,
    money,
    symbol,
    rate
):

    st.header("💰 Financial Analysis")


    # ========================================================
    # FINANCIAL KPI
    # ========================================================

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


    # ========================================================
    # REVENUE VS PROFIT
    # ========================================================

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


    # ========================================================
    # RESOURCE COST
    # ========================================================

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


    # ========================================================
    # COST BREAKDOWN
    # ========================================================

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
