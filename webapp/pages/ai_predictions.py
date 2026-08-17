import streamlit as st
import pandas as pd


# ============================================================
# AI PREDICTIONS
# ============================================================

def show_ai_predictions(
    electricity_model,
    water_model
):

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


    # ========================================================
    # INPUT SECTION
    # ========================================================

    col1, col2 = st.columns(2)


    # ========================================================
    # LEFT INPUTS
    # ========================================================

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


    # ========================================================
    # RIGHT INPUTS
    # ========================================================

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


    # ========================================================
    # PREDICTION BUTTON
    # ========================================================

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


            # =================================================
            # RESULTS
            # =================================================

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
                "The prediction could not be completed."
            )

            st.exception(e)
