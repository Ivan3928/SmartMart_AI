import streamlit as st
import pandas as pd


# ============================================================
# BALANCE SHEET
# ============================================================

def show_balance_sheet(
    latest,
    money
):

    st.header("📑 Balance Sheet")


    # ========================================================
    # ASSETS
    # ========================================================

    st.subheader("🏢 Assets")


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


    assets_display["Amount"] = (
        assets_display["Amount"].apply(money)
    )


    st.dataframe(
        assets_display,
        use_container_width=True,
        hide_index=True
    )


    st.metric(
        "Total Assets",
        money(latest["total_assets"])
    )


    st.divider()


    # ========================================================
    # LIABILITIES
    # ========================================================

    st.subheader("🏦 Liabilities")


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


    liabilities_display["Amount"] = (
        liabilities_display["Amount"].apply(money)
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


    st.divider()


    # ========================================================
    # EQUITY
    # ========================================================

    st.subheader("📊 Equity")


    st.metric(
        "Total Equity",
        money(latest["total_equity"])
    )


    st.divider()


    # ========================================================
    # ACCOUNTING EQUATION
    # ========================================================

    st.subheader("🧮 Accounting Equation")


    st.write(
        "Assets = Liabilities + Equity"
    )


    left, right = st.columns(2)


    with left:

        st.metric(
            "Assets",
            money(latest["total_assets"])
        )


    with right:

        liabilities_equity = (
            float(latest["total_liabilities"])
            + float(latest["total_equity"])
        )


        st.metric(
            "Liabilities + Equity",
            money(liabilities_equity)
        )


    # ========================================================
    # BALANCE CHECK
    # ========================================================

    difference = (
        float(latest["total_assets"])
        - liabilities_equity
    )


    if abs(difference) < 1:

        st.success(
            "✓ The balance sheet is balanced."
        )

    else:

        st.warning(
            f"Difference: {money(difference)}"
        )
