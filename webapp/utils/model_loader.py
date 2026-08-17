import os
import joblib
import streamlit as st


# ============================================================
# MACHINE LEARNING MODEL LOADER
# ============================================================

@st.cache_resource
def load_models(
    electricity_model_file,
    water_model_file
):

    # --------------------------------------------------------
    # CHECK ELECTRICITY MODEL
    # --------------------------------------------------------

    if not os.path.exists(electricity_model_file):

        st.error(
            f"Electricity model not found: "
            f"{electricity_model_file}"
        )

        st.stop()


    # --------------------------------------------------------
    # CHECK WATER MODEL
    # --------------------------------------------------------

    if not os.path.exists(water_model_file):

        st.error(
            f"Water model not found: "
            f"{water_model_file}"
        )

        st.stop()


    # --------------------------------------------------------
    # LOAD ELECTRICITY MODEL
    # --------------------------------------------------------

    electricity_model = joblib.load(
        electricity_model_file
    )


    # --------------------------------------------------------
    # LOAD WATER MODEL
    # --------------------------------------------------------

    water_model = joblib.load(
        water_model_file
    )


    # --------------------------------------------------------
    # RETURN MODELS
    # --------------------------------------------------------

    return electricity_model, water_model
