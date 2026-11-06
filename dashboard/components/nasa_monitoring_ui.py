
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


# --------------------------------------------------
# REUSABLE DASHBOARD STYLES
# --------------------------------------------------

def metric_card(label, value, caption, accent="#24C8B5"):
    st.html(
        f"""
        <div style="
            background: linear-gradient(145deg, #14232E, #101923);
            border: 1px solid #263746;
            border-left: 4px solid {accent};
            border-radius: 13px;
            padding: 19px 20px;
            min-height: 125px;
        ">
            <div style="
                color: #8DA2B5;
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 1px;
                text-transform: uppercase;
            ">{label}</div>

            <div style="
                color: #E8F0F6;
                font-size: 29px;
                font-weight: 700;
                margin-top: 10px;
                font-family: 'Space Grotesk', sans-serif;
            ">{value}</div>

            <div style="
                color: #8DA2B5;
                font-size: 11px;
                margin-top: 5px;
            ">{caption}</div>
        </div>
        """
    )


def style_chart(fig, height=430):
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
        margin=dict(l=20, r=20, t=35, b=20),
        hovermode="x unified",
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


# --------------------------------------------------
# MAIN NASA MONITORING PAGE
# --------------------------------------------------

def render_nasa_page():

    # --------------------------------------------------
    # LOAD NASA EVALUATION DATA
    # --------------------------------------------------

    project_root = Path(__file__).resolve().parents[2]

    data_path = (
        project_root
        / "results"
        / "nasa_ims_anomaly_evaluation.csv"
    )

    if not data_path.exists():
        st.error(f"NASA evaluation file not found: {data_path}")
        return

    df = pd.read_csv(data_path)

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    df = (
        df.dropna(subset=["Timestamp"])
        .sort_values("Timestamp")
        .reset_index(drop=True)
    )

    if df.empty:
        st.warning("No valid NASA monitoring records were found.")
        return

    # --------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------

    st.html(
        """
        <div style="margin-bottom: 8px;">
            <div style="
                color:#24C8B5;
                font-size:11px;
                font-weight:700;
                letter-spacing:2px;
                margin-bottom:8px;
            ">CONDITION MONITORING / NASA IMS</div>

            <div style="
                color:#E8F0F6;
                font-family:'Space Grotesk',sans-serif;
                font-size:30px;
                font-weight:700;
            ">NASA IMS Anomaly Monitoring</div>

            <div style="
                color:#8DA2B5;
                font-size:13px;
                margin-top:7px;
            ">
                Experimental bearing-condition analysis using
                Isolation Forest anomaly detection.
            </div>
        </div>
        """
    )

    st.markdown("")

    # --------------------------------------------------
    # FILTER SECTION
    # --------------------------------------------------

    st.html(
        '<p class="section-title">MONITORING CONFIGURATION</p>'
    )

    filter_col, info_col = st.columns([1, 2])

    period_options = ["All Periods"] + sorted(
        df["Data_Period"].dropna().unique().tolist()
    )

    with filter_col:
        selected_period = st.selectbox(
            "Monitoring period",
            period_options
        )

    if selected_period != "All Periods":
        filtered_df = df[
            df["Data_Period"] == selected_period
        ].copy()
    else:
        filtered_df = df.copy()

    if filtered_df.empty:
        st.warning("No records available for this selection.")
        return

    with info_col:
        st.html(
            f"""
            <div style="
                background:#101923;
                border:1px solid #263746;
                border-radius:11px;
                padding:14px 17px;
                margin-top:27px;
            ">
                <div style="color:#8DA2B5;font-size:11px;">
                    SELECTED DATA RANGE
                </div>
                <div style="
                    color:#E8F0F6;
                    font-size:14px;
                    font-weight:600;
                    margin-top:5px;
                ">
                    {filtered_df["Timestamp"].min():%d %b %Y}
                    &nbsp; — &nbsp;
                    {filtered_df["Timestamp"].max():%d %b %Y}
                </div>
            </div>
            """
        )

    # --------------------------------------------------
    # SUMMARY METRICS
    # --------------------------------------------------

    total = len(filtered_df)

    anomaly_count = int(
        (filtered_df["Anomaly_Prediction"] == -1).sum()
    )

    normal_count = int(
        (filtered_df["Anomaly_Prediction"] == 1).sum()
    )

    classified_count = normal_count + anomaly_count
    unclassified_count = total - classified_count

    anomaly_rate = (
        anomaly_count / classified_count * 100
        if classified_count > 0 else 0
    )

    st.html(
        '<p class="section-title">MONITORING OVERVIEW</p>'
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Total Observations",
            f"{total:,}",
            "CSV records in selected period",
            "#579BFF"
        )

    with c2:
        metric_card(
            "Normal Observations",
            f"{normal_count:,}",
            "Model-labelled normal",
            "#24C8B5"
        )

    with c3:
        metric_card(
            "Anomaly Observations",
            f"{anomaly_count:,}",
            "Model-flagged observations",
            "#F06B75"
        )

    with c4:
        metric_card(
            "Anomaly Rate",
            f"{anomaly_rate:.2f}%",
            "Share of flagged records",
            "#F5A742"
        )

    st.markdown("")

    # --------------------------------------------------
    # ANOMALY SCORE TIMELINE
    # --------------------------------------------------

    st.html(
        '<p class="section-title">01 / ISOLATION FOREST SCORE TIMELINE</p>'
    )

    st.caption(
        "Positive scores indicate normal observations; "
        "negative scores indicate model-detected anomalies. "
        "The zero line is the model decision boundary."
    )

    normal_df = filtered_df[
        filtered_df["Anomaly_Prediction"] == 1
    ]

    anomaly_df = filtered_df[
        filtered_df["Anomaly_Prediction"] == -1
    ]

    fig_score = go.Figure()

    fig_score.add_trace(
        go.Scatter(
            x=normal_df["Timestamp"],
            y=normal_df["Anomaly_Score"],
            mode="markers",
            name="Normal",
            marker=dict(
                color="#24C8B5",
                size=5,
                opacity=0.75
            ),
            hovertemplate=(
                "<b>Normal</b><br>"
                "Time: %{x}<br>"
                "Score: %{y:.5f}"
                "<extra></extra>"
            )
        )
    )

    fig_score.add_trace(
        go.Scatter(
            x=anomaly_df["Timestamp"],
            y=anomaly_df["Anomaly_Score"],
            mode="markers",
            name="Anomaly",
            marker=dict(
                color="#F06B75",
                size=6,
                opacity=0.9
            ),
            hovertemplate=(
                "<b>Anomaly</b><br>"
                "Time: %{x}<br>"
                "Score: %{y:.5f}"
                "<extra></extra>"
            )
        )
    )

    fig_score.add_hline(
        y=0,
        line_dash="dash",
        line_color="#F5A742",
        line_width=1.5,
        annotation_text="Decision boundary",
        annotation_position="top left",
        annotation_font_color="#F5A742"
    )

    fig_score.update_layout(
        xaxis_title="Timestamp",
        yaxis_title="Isolation Forest Score"
    )

    fig_score = style_chart(fig_score, 440)

    st.plotly_chart(
        fig_score,
        use_container_width=True
    )

    # --------------------------------------------------
    # BEARING HEALTH INDICATORS
    # --------------------------------------------------

    st.html(
        '<p class="section-title">02 / BEARING HEALTH INDICATORS</p>'
    )

    st.caption(
        "Relative health-indicator trends for Bearing 3 and Bearing 4."
    )

    fig_hi = go.Figure()

    fig_hi.add_trace(
        go.Scatter(
            x=filtered_df["Timestamp"],
            y=filtered_df["B3_HI"],
            mode="lines",
            name="Bearing 3",
            line=dict(
                color="#24C8B5",
                width=2.5
            )
        )
    )

    fig_hi.add_trace(
        go.Scatter(
            x=filtered_df["Timestamp"],
            y=filtered_df["B4_HI"],
            mode="lines",
            name="Bearing 4",
            line=dict(
                color="#F5A742",
                width=2.5
            )
        )
    )

    fig_hi.update_layout(
        xaxis_title="Timestamp",
        yaxis_title="Relative Health Indicator"
    )

    fig_hi = style_chart(fig_hi, 430)

    st.plotly_chart(
        fig_hi,
        use_container_width=True
    )

    st.html(
        """
        <div style="
            background:rgba(245,167,66,0.08);
            border:1px solid rgba(245,167,66,0.3);
            border-radius:10px;
            padding:12px 15px;
            color:#D9C39F;
            font-size:12px;
        ">
            <b style="color:#F5A742;">Interpretation note:</b>
            These are relative monitoring indicators.
            An HI value above 1 is not a validated physical
            bearing-failure threshold.
        </div>
        """
    )

    st.markdown("")

    # --------------------------------------------------
    # EXPERIMENTAL MONITORING INDEX
    # --------------------------------------------------

    st.html(
        '<p class="section-title">03 / EXPERIMENTAL MONITORING INDEX</p>'
    )

    st.caption(
        "Compare the raw experimental index with its exponentially "
        "smoothed trend."
    )

    bearing_choice = st.radio(
        "Select bearing",
        ["Bearing 3", "Bearing 4"],
        horizontal=True
    )

    if bearing_choice == "Bearing 3":
        raw_col = "B3_Monitoring_Index"
        ema_col = "B3_Monitoring_Index_EMA"
    else:
        raw_col = "B4_Monitoring_Index"
        ema_col = "B4_Monitoring_Index_EMA"

    fig_index = go.Figure()

    fig_index.add_trace(
        go.Scatter(
            x=filtered_df["Timestamp"],
            y=filtered_df[raw_col],
            mode="lines",
            name="Raw Index",
            line=dict(
                color="#8DA2B5",
                width=1
            ),
            opacity=0.45
        )
    )

    fig_index.add_trace(
        go.Scatter(
            x=filtered_df["Timestamp"],
            y=filtered_df[ema_col],
            mode="lines",
            name="EMA Smoothed Index",
            line=dict(
                color="#24C8B5",
                width=3
            )
        )
    )

    fig_index.update_layout(
        xaxis_title="Timestamp",
        yaxis_title="Experimental Monitoring Index"
    )

    fig_index = style_chart(fig_index, 410)

    st.plotly_chart(
        fig_index,
        use_container_width=True
    )

    st.html(
        """
        <div style="
            background:#101923;
            border:1px solid #263746;
            border-radius:10px;
            padding:12px 15px;
            color:#A8B8C6;
            font-size:12px;
        ">
            The monitoring index is an experimental composite indicator.
            It is not a health percentage, failure probability,
            or remaining useful life estimate.
        </div>
        """
    )

    st.markdown("")

    # --------------------------------------------------
    # RECENT ANOMALY OBSERVATIONS
    # --------------------------------------------------

    st.html(
        '<p class="section-title">04 / RECENT ANOMALY OBSERVATIONS</p>'
    )

    recent_anomalies = (
        filtered_df[
            filtered_df["Anomaly_Prediction"] == -1
        ]
        .sort_values("Timestamp", ascending=False)
        .head(10)
    )

    display_columns = [
        "Timestamp",
        "Anomaly_Score",
        "B3_HI",
        "B4_HI",
        "Status"
    ]

    if recent_anomalies.empty:
        st.success(
            "No model-flagged anomalies in the selected period."
        )
    else:
        display_df = recent_anomalies[display_columns].copy()

        display_df["Timestamp"] = (
            display_df["Timestamp"].dt.strftime("%d %b %Y, %H:%M:%S")
        )

        display_df = display_df.rename(
            columns={
                "Timestamp": "Timestamp",
                "Anomaly_Score": "Anomaly Score",
                "B3_HI": "Bearing 3 HI",
                "B4_HI": "Bearing 4 HI",
                "Status": "Model Status"
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------
    # FINAL DISCLAIMER
    # --------------------------------------------------

    st.html(
        """
        <div style="
            background:rgba(240,107,117,0.07);
            border:1px solid rgba(240,107,117,0.28);
            border-radius:12px;
            padding:16px 18px;
            margin-top:18px;
        ">
            <div style="
                color:#F06B75;
                font-weight:700;
                font-size:13px;
                margin-bottom:6px;
            ">EXPERIMENTAL MODEL — IMPORTANT LIMITATION</div>

            <div style="
                color:#B9C9D6;
                font-size:12px;
                line-height:1.7;
            ">
                Isolation Forest identifies observations that differ
                from the baseline feature distribution. These flags
                indicate statistical changes, not confirmed physical
                bearing failures. This monitoring system has not been
                validated for failure prediction or remaining useful
                life estimation.
            </div>
        </div>
        """
    )
