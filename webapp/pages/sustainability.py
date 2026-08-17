import streamlit as st
import plotly.express as px

from utils.chart_theme import apply_chart_theme


# ============================================================
# SUSTAINABILITY
# ============================================================

def show_sustainability(
    df,
    latest
):

    st.header(
        "🌱 Sustainability & SDG Analysis"
    )


    # ========================================================
    # EFFICIENCY METRICS
    # ========================================================

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


    # ========================================================
    # SDG ANALYSIS
    # ========================================================

    st.subheader(
        "🌍 Relevant Sustainable Development Goals"
    )


    col1, col2 = st.columns(2)


    # ========================================================
    # LEFT SDGS
    # ========================================================

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


    # ========================================================
    # RIGHT SDGS
    # ========================================================

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


    # ========================================================
    # SUSTAINABILITY CHART
    # ========================================================

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
