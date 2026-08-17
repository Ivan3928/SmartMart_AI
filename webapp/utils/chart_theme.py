import streamlit as st


# ============================================================
# PROFESSIONAL UI STYLE
# ============================================================

def apply_custom_css():

    st.markdown(
        """
        <style>

        [data-testid="stAppViewContainer"] {
            background-color: #F3F4F6;
        }

        [data-testid="stHeader"] {
            background-color: #F3F4F6;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3, h4 {
            color: #111827 !important;
            font-weight: 700 !important;
        }

        p {
            color: #1F2937 !important;
        }

        label {
            color: #1F2937 !important;
        }

        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #D1D5DB;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }

        [data-testid="stMetricLabel"] {
            color: #4B5563 !important;
        }

        [data-testid="stMetricValue"] {
            color: #111827 !important;
        }

        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
        }

        [data-testid="stSidebar"] p {
            color: #1F2937 !important;
        }

        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PLOTLY THEME
# ============================================================

def apply_chart_theme(fig):

    fig.update_layout(

        paper_bgcolor="#F3F4F6",

        plot_bgcolor="#E5E7EB",

        font=dict(
            family="Arial",
            color="#111827",
            size=13
        ),

        title=dict(
            font=dict(
                family="Arial",
                color="#111827",
                size=19
            ),
            x=0.02,
            xanchor="left"
        ),

        xaxis=dict(
            title_font=dict(
                color="#111827",
                size=14
            ),
            tickfont=dict(
                color="#111827",
                size=12
            ),
            gridcolor="#B8BEC8",
            linecolor="#6B7280",
            showline=True
        ),

        yaxis=dict(
            title_font=dict(
                color="#111827",
                size=14
            ),
            tickfont=dict(
                color="#111827",
                size=12
            ),
            gridcolor="#B8BEC8",
            linecolor="#6B7280",
            showline=True
        ),

        legend=dict(
            font=dict(
                color="#111827",
                size=12
            ),
            bgcolor="rgba(255,255,255,0.90)",
            bordercolor="#9CA3AF",
            borderwidth=1
        ),

        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#6B7280",
            font=dict(
                color="#111827",
                size=12
            )
        ),

        margin=dict(
            l=70,
            r=30,
            t=70,
            b=60
        )
    )

    return fig
