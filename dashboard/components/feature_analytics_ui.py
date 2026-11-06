
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = PROJECT_ROOT / "results"

CWRU_FEATURES = [
    "Mean",
    "RMS",
    "Standard_Deviation",
    "Variance",
    "Minimum",
    "Maximum",
    "Peak_to_Peak",
    "Kurtosis",
    "Skewness",
    "Crest_Factor"
]

NASA_FEATURES = [
    "B3_HI",
    "B4_HI",
    "B3_Degradation_Rate",
    "B4_Degradation_Rate",
    "B3_Acceleration",
    "B4_Acceleration"
]


# --------------------------------------------------
# REUSABLE UI COMPONENTS
# --------------------------------------------------

def analytics_metric(label, value, caption, accent="#24C8B5"):

    st.html(
        f"""
        <div style="
            background:linear-gradient(145deg,#14232E,#101923);
            border:1px solid #263746;
            border-left:4px solid {accent};
            border-radius:13px;
            padding:19px 20px;
            min-height:120px;
        ">
            <div style="
                color:#8DA2B5;
                font-size:12px;
                font-weight:600;
                letter-spacing:1px;
                text-transform:uppercase;
            ">{label}</div>

            <div style="
                color:#E8F0F6;
                font-size:29px;
                font-weight:700;
                margin-top:10px;
                font-family:'Space Grotesk',sans-serif;
            ">{value}</div>

            <div style="
                color:#8DA2B5;
                font-size:11px;
                margin-top:5px;
            ">{caption}</div>
        </div>
        """
    )


def style_analytics_chart(fig, height=430):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#101923",
        plot_bgcolor="#101923",
        font=dict(
            color="#DCE6EE",
            family="DM Sans, sans-serif",
            size=12
        ),
        height=height,
        margin=dict(
            l=20,
            r=20,
            t=55,
            b=25
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor="rgba(0,0,0,0)"
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor="#304454"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(141,162,181,0.13)",
            zeroline=False,
            linecolor="#304454"
        )
    )

    return fig


def section_header(number, title, description):

    st.html(
        f"""
        <div style="margin-top:18px;margin-bottom:12px;">
            <div style="
                color:#24C8B5;
                font-size:11px;
                font-weight:700;
                letter-spacing:1.5px;
                margin-bottom:5px;
            ">{number}</div>

            <div style="
                color:#E8F0F6;
                font-size:21px;
                font-weight:700;
                font-family:'Space Grotesk',sans-serif;
            ">{title}</div>

            <div style="
                color:#8DA2B5;
                font-size:12px;
                margin-top:5px;
            ">{description}</div>
        </div>
        """
    )


# --------------------------------------------------
# MAIN FEATURE ANALYTICS PAGE
# --------------------------------------------------

def render_feature_analytics_page():

    # --------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------

    st.html(
        """
        <div style="margin-bottom:18px;">
            <div style="
                color:#24C8B5;
                font-size:11px;
                font-weight:700;
                letter-spacing:2px;
                margin-bottom:8px;
            ">DATA EXPLORATION / FEATURE ENGINEERING</div>

            <div style="
                color:#E8F0F6;
                font-family:'Space Grotesk',sans-serif;
                font-size:30px;
                font-weight:700;
            ">Feature Analytics</div>

            <div style="
                color:#8DA2B5;
                font-size:13px;
                margin-top:7px;
            ">
                Explore vibration characteristics, bearing-condition
                distributions and NASA IMS degradation indicators.
            </div>
        </div>
        """
    )

    # ==================================================
    # 01 - CWRU FEATURE ANALYTICS
    # ==================================================

    section_header(
        "01 / CWRU DATASET",
        "Bearing Vibration Feature Analysis",
        "Statistical feature distributions and relationships "
        "between Normal and Outer Race bearing conditions."
    )

    cwru_path = RESULTS_DIR / "complete_bearing_features.csv"

    if not cwru_path.exists():
        st.error("CWRU feature dataset was not found.")
        return

    cwru_df = pd.read_csv(cwru_path)

    available_features = [
        feature for feature in CWRU_FEATURES
        if feature in cwru_df.columns
    ]

    if "Label" not in cwru_df.columns or not available_features:
        st.error("Required CWRU feature columns are missing.")
        return

    # --------------------------------------------------
    # CWRU SUMMARY
    # --------------------------------------------------

    cwru_records = len(cwru_df)
    cwru_feature_count = len(available_features)

    class_count = cwru_df["Label"].nunique()

    c1, c2, c3 = st.columns(3)

    with c1:
        analytics_metric(
            "Total Records",
            f"{cwru_records:,}",
            "CWRU feature observations",
            "#579BFF"
        )

    with c2:
        analytics_metric(
            "Vibration Features",
            cwru_feature_count,
            "Available statistical features",
            "#24C8B5"
        )

    with c3:
        analytics_metric(
            "Bearing Classes",
            class_count,
            "Distinct dataset labels",
            "#F5A742"
        )

    st.markdown("")

    # --------------------------------------------------
    # CWRU FEATURE DISTRIBUTION
    # --------------------------------------------------

    st.markdown(
        '<p class="section-title">FEATURE DISTRIBUTION EXPLORER</p>',
        unsafe_allow_html=True
    )

    selected_feature = st.selectbox(
        "Select a CWRU vibration feature",
        available_features
    )

    fig_hist = px.histogram(
        cwru_df,
        x=selected_feature,
        color="Label",
        barmode="overlay",
        opacity=0.65,
        marginal="box",
        title=f"{selected_feature} — Distribution by Bearing Condition",
        color_discrete_sequence=[
            "#24C8B5",
            "#F06B75",
            "#579BFF"
        ],
        template="plotly_dark"
    )

    fig_hist.update_layout(
        xaxis_title=selected_feature,
        yaxis_title="Number of Observations",
        legend_title_text="Bearing Condition",
        bargap=0.08
    )

    fig_hist = style_analytics_chart(fig_hist, 460)

    st.plotly_chart(
        fig_hist,
        use_container_width=True
    )

    st.caption(
        "The histogram compares feature-value distributions across "
        "the available bearing-condition labels. The box plot provides "
        "an additional view of spread and potential outliers."
    )

    # --------------------------------------------------
    # CWRU CORRELATION MATRIX
    # --------------------------------------------------

    st.markdown(
        '<p class="section-title">CWRU FEATURE CORRELATION</p>',
        unsafe_allow_html=True
    )

    correlation = cwru_df[available_features].corr(
        method="pearson"
    )

    fig_corr = px.imshow(
        correlation,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        aspect="auto",
        title="Pearson Correlation Matrix — CWRU",
        template="plotly_dark"
    )

    fig_corr.update_layout(
        height=570,
        margin=dict(l=20, r=20, t=60, b=100),
        coloraxis_colorbar=dict(
            title="Correlation",
            thickness=14
        )
    )

    fig_corr.update_xaxes(tickangle=45)

    st.plotly_chart(
        fig_corr,
        use_container_width=True
    )

    st.html(
        """
        <div style="
            background:#101923;
            border:1px solid #263746;
            border-radius:10px;
            padding:13px 16px;
            color:#A8B8C6;
            font-size:12px;
        ">
            <b style="color:#24C8B5;">Interpretation:</b>
            Pearson correlation describes linear relationships
            between CWRU features. Correlation does not establish
            causation or prove that features are independent.
        </div>
        """
    )

    st.divider()

    # ==================================================
    # 02 - NASA IMS FEATURE ANALYTICS
    # ==================================================

    section_header(
        "02 / NASA IMS DATASET",
        "Bearing Degradation Feature Analysis",
        "Explore relative health indicators, degradation rates "
        "and acceleration trends from the NASA IMS dataset."
    )

    nasa_path = RESULTS_DIR / "nasa_ims_anomaly_evaluation.csv"

    if not nasa_path.exists():
        st.error("NASA IMS evaluation dataset was not found.")
        return

    nasa_df = pd.read_csv(nasa_path)

    if "Timestamp" not in nasa_df.columns:
        st.error("NASA dataset does not contain Timestamp.")
        return

    nasa_df["Timestamp"] = pd.to_datetime(
        nasa_df["Timestamp"],
        errors="coerce"
    )

    nasa_df = (
        nasa_df.dropna(subset=["Timestamp"])
        .sort_values("Timestamp")
        .reset_index(drop=True)
    )

    available_nasa_features = [
        feature for feature in NASA_FEATURES
        if feature in nasa_df.columns
    ]

    if not available_nasa_features:
        st.warning("NASA feature columns were not found.")
        return

    # --------------------------------------------------
    # NASA FILTERS
    # --------------------------------------------------

    st.markdown(
        '<p class="section-title">NASA MONITORING FILTERS</p>',
        unsafe_allow_html=True
    )

    filter_col, feature_col = st.columns(2)

    period_options = ["All Periods"] + sorted(
        nasa_df["Data_Period"].dropna().unique().tolist()
    ) if "Data_Period" in nasa_df.columns else ["All Periods"]

    with filter_col:

        selected_period = st.selectbox(
            "Select monitoring period",
            period_options
        )

    with feature_col:

        selected_nasa_feature = st.selectbox(
            "Select a NASA IMS feature",
            available_nasa_features
        )

    if selected_period != "All Periods":
        nasa_df = nasa_df[
            nasa_df["Data_Period"] == selected_period
        ].copy()

    if nasa_df.empty:
        st.warning("No NASA records available for this selection.")
        return

    # --------------------------------------------------
    # NASA SUMMARY
    # --------------------------------------------------

    nasa_records = len(nasa_df)

    nasa_valid_features = nasa_df[
        available_nasa_features
    ].notna().sum().sum()

    n1, n2 = st.columns(2)

    with n1:
        analytics_metric(
            "NASA Observations",
            f"{nasa_records:,}",
            "Records in selected period",
            "#579BFF"
        )

    with n2:
        analytics_metric(
            "Available Features",
            len(available_nasa_features),
            "Selected degradation indicators",
            "#24C8B5"
        )

    st.markdown("")

    # --------------------------------------------------
    # NASA FEATURE TREND
    # --------------------------------------------------

    st.markdown(
        '<p class="section-title">DEGRADATION TREND EXPLORER</p>',
        unsafe_allow_html=True
    )

    fig_nasa = px.line(
        nasa_df,
        x="Timestamp",
        y=selected_nasa_feature,
        title=f"{selected_nasa_feature} — NASA IMS Trend",
        template="plotly_dark"
    )

    fig_nasa.update_traces(
        line=dict(
            color="#24C8B5",
            width=2
        )
    )

    fig_nasa.update_layout(
        xaxis_title="Recorded Timestamp",
        yaxis_title=selected_nasa_feature
    )

    fig_nasa = style_analytics_chart(fig_nasa, 440)

    st.plotly_chart(
        fig_nasa,
        use_container_width=True
    )

    st.caption(
        "NASA IMS timestamps are not evenly spaced. Interpret the "
        "trend using the recorded timestamps rather than assuming "
        "a fixed time interval between observations."
    )

    # --------------------------------------------------
    # NASA SPEARMAN CORRELATION
    # --------------------------------------------------

    st.markdown(
        '<p class="section-title">NASA IMS FEATURE CORRELATION</p>',
        unsafe_allow_html=True
    )

    nasa_correlation = nasa_df[
        available_nasa_features
    ].corr(
        method="spearman"
    )

    fig_nasa_corr = px.imshow(
        nasa_correlation,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        aspect="auto",
        title="Spearman Correlation Matrix — NASA IMS",
        template="plotly_dark"
    )

    fig_nasa_corr.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=60, b=100),
        coloraxis_colorbar=dict(
            title="Correlation",
            thickness=14
        )
    )

    fig_nasa_corr.update_xaxes(tickangle=35)

    st.plotly_chart(
        fig_nasa_corr,
        use_container_width=True
    )

    st.html(
        """
        <div style="
            background:#101923;
            border:1px solid #263746;
            border-radius:10px;
            padding:14px 16px;
            color:#A8B8C6;
            font-size:12px;
            line-height:1.7;
        ">
            <b style="color:#24C8B5;">Interpretation note:</b>
            Spearman correlation measures monotonic statistical
            relationships between NASA IMS indicators. These
            relationships do not establish causation or physical
            bearing failure. The anomaly-monitoring results are
            experimental and are not validated Remaining Useful
            Life predictions.
        </div>
        """
    )
