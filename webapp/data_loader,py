import os
import pandas as pd
import streamlit as st


# ============================================================
# DATA LOADER
# ============================================================

@st.cache_data
def load_data(data_file):

    # --------------------------------------------------------
    # CHECK DATA FILE
    # --------------------------------------------------------

    if not os.path.exists(data_file):

        st.error(
            f"Data file not found: {data_file}"
        )

        st.stop()


    # --------------------------------------------------------
    # READ CSV FILE
    # --------------------------------------------------------

    data = pd.read_csv(data_file)


    # --------------------------------------------------------
    # CONVERT DATE COLUMN
    # --------------------------------------------------------

    if "date" in data.columns:

        data["date"] = pd.to_datetime(
            data["date"],
            errors="coerce"
        )


    # --------------------------------------------------------
    # RETURN DATA
    # --------------------------------------------------------

    return data
