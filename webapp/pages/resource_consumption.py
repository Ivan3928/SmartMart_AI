import streamlit as st
import plotly.express as px

from utils.chart_theme import apply_chart_theme


# ============================================================
# RESOURCE CONSUMPTION
# ============================================================

def show_resource_consumption(
    df,
    latest,
    resource_category
):

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
