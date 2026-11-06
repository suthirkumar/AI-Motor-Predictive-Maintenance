
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.components.model_loader import load_models


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = PROJECT_ROOT / "results"
MODEL_DIR = RESULTS_DIR / "models"


# --------------------------------------------------
# REUSABLE UI COMPONENTS
# --------------------------------------------------

def insights_metric(label, value, caption, accent="#24C8B5"):

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
                font-size:26px;
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


def insights_section(number, title, description):

    st.html(
        f"""
        <div style="margin-top:20px;margin-bottom:13px;">
            <div style="
                color:#24C8B5;
                font-size:11px;
                font-weight:700;
                letter-spacing:1.5px;
                margin-bottom:5px;
            ">{number}</div>

            <div style="
                color:#E8F0F6;
                font-size:22px;
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


def style_insights_chart(fig, height=400):

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
        margin=dict(l=20, r=20, t=55, b=25),
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
# MAIN MODEL INSIGHTS PAGE
# --------------------------------------------------

def render_model_insights_page():

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
            ">MODEL INTELLIGENCE / TECHNICAL EVALUATION</div>

            <div style="
                color:#E8F0F6;
                font-family:'Space Grotesk',sans-serif;
                font-size:30px;
                font-weight:700;
            ">Model Insights</div>

            <div style="
                color:#8DA2B5;
                font-size:13px;
                margin-top:7px;
            ">
                Model architecture, evaluation findings, sensitivity
                analysis and system limitations.
            </div>
        </div>
        """
    )

    # --------------------------------------------------
    # LOAD TRAINED MODELS
    # --------------------------------------------------

    try:
        models = load_models()

        cwru_model = models["cwru_model"]
        nasa_model = models["nasa_model"]

        st.success("All trained models loaded successfully.")

    except Exception as error:
        st.error(f"Unable to load trained models: {error}")
        return

    # ==================================================
    # 01 - MODEL SYSTEM OVERVIEW
    # ==================================================

    insights_section(
        "01 / SYSTEM OVERVIEW",
        "Predictive Maintenance Model Architecture",
        "Two independent machine-learning pipelines for bearing "
        "fault classification and experimental anomaly monitoring."
    )

    overview_col1, overview_col2 = st.columns(2)

    with overview_col1:
        insights_metric(
            "CWRU MODEL",
            "Decision Tree",
            "Normal vs Outer Race Fault",
            "#24C8B5"
        )

    with overview_col2:
        insights_metric(
            "NASA IMS MODEL",
            "Isolation Forest",
            "Experimental anomaly detection",
            "#579BFF"
        )

    st.markdown("")

    # ==================================================
    # 02 - CWRU MODEL
    # ==================================================

    insights_section(
        "02 / CWRU CLASSIFICATION",
        "Bearing Fault Classification Model",
        "Decision Tree classifier trained using statistical "
        "vibration features from the CWRU dataset."
    )

    cwru_col1, cwru_col2, cwru_col3 = st.columns(3)

    with cwru_col1:
        insights_metric(
            "Algorithm",
            "Decision Tree",
            "Supervised classification",
            "#24C8B5"
        )

    with cwru_col2:
        insights_metric(
            "Training Records",
            "3,183",
            "CWRU feature observations",
            "#579BFF"
        )

    with cwru_col3:
        insights_metric(
            "Classes",
            len(cwru_model.classes_),
            "Normal and Outer Race Fault",
            "#F5A742"
        )

    st.markdown("")

    st.markdown(
        '<p class="section-title">MODEL CONFIGURATION</p>',
        unsafe_allow_html=True
    )

    cwru_params = cwru_model.get_params()

    cwru_details = pd.DataFrame({
        "Parameter": [
            "Algorithm",
            "Maximum Depth",
            "Class Weight",
            "Random State",
            "Number of Classes",
            "Input Features"
        ],
        "Value": [
            type(cwru_model).__name__,
            cwru_params.get("max_depth"),
            cwru_params.get("class_weight"),
            cwru_params.get("random_state"),
            len(cwru_model.classes_),
            len(models["cwru_scaler"].mean_)
        ]
    })

    st.dataframe(
        cwru_details,
        use_container_width=True,
        hide_index=True
    )

    # ==================================================
    # CWRU MODEL INPUT FEATURES — INTERACTIVE EXPLANATIONS
    # ==================================================

    insights_section(
        "CWRU MODEL INPUT FEATURES",
        "CWRU Model Input Features",
        "Explore the 10 vibration signal features used by the bearing fault classifier."
    )

    cwru_feature_explanations = {
        "Mean": [
            "Represents the average value of the vibration signal.",
            "Helps identify any DC offset or bias in the signal.",
            "A value close to zero is common for a centred vibration signal."
        ],
        "RMS": [
            "RMS stands for Root Mean Square.",
            "Measures the overall vibration signal magnitude.",
            "Higher RMS can indicate increased vibration energy.",
            "Useful for identifying changes in machine vibration."
        ],
        "Standard_Deviation": [
            "Measures how much the vibration values spread around their mean.",
            "A higher value indicates greater signal variation.",
            "Helps describe the variability of the vibration signal."
        ],
        "Variance": [
            "Measures the average squared deviation from the mean.",
            "It represents the spread of vibration signal values.",
            "Higher variance indicates greater signal dispersion.",
            "Its unit is the square of the original signal unit."
        ],
        "Minimum": [
            "Represents the lowest recorded vibration value in a signal window.",
            "Captures the most negative amplitude in the window."
        ],
        "Maximum": [
            "Represents the highest recorded vibration value in a signal window.",
            "Captures the most positive amplitude in the window."
        ],
        "Peak_to_Peak": [
            "Measures the difference between the maximum and minimum values.",
            "Describes the full amplitude range within the signal window."
        ],
        "Kurtosis": [
            "Summarizes the shape of the signal's value distribution.",
            "Is sensitive to values far from the signal mean.",
            "Its interpretation depends on the calculation convention."
        ],
        "Skewness": [
            "Measures the asymmetry of the signal's value distribution.",
            "A value near zero indicates a roughly symmetric distribution.",
            "Positive or negative values describe the direction of asymmetry."
        ],
        "Crest_Factor": [
            "Relates the signal's peak magnitude to its RMS level.",
            "Describes peak size relative to the overall signal magnitude.",
            "It is a statistical ratio, not a fault diagnosis by itself."
        ]
    }

    for feature, explanations in cwru_feature_explanations.items():
        with st.expander(feature.replace("_", " ")):
            st.markdown("\n".join(f"- {item}" for item in explanations))

    st.caption(
        "These descriptions explain statistical feature meanings; no single "
        "feature value independently diagnoses a bearing fault."
    )

    st.markdown(
        '<p class="section-title">CLASSIFICATION OUTPUT</p>',
        unsafe_allow_html=True
    )

    class_col1, class_col2 = st.columns(2)

    with class_col1:
        insights_metric(
            "CLASS 0",
            "Normal",
            "Normal bearing condition",
            "#24C8B5"
        )

    with class_col2:
        insights_metric(
            "CLASS 1",
            "Outer Race Fault",
            "Outer race bearing fault",
            "#F06B75"
        )

    st.markdown("")

    st.html(
        """
        <div style="
            background:#101923;
            border:1px solid #263746;
            border-radius:11px;
            padding:15px 17px;
            color:#B9C9D6;
            font-size:12px;
            line-height:1.8;
        ">
            <b style="color:#24C8B5;">Preprocessing pipeline</b><br>
            StandardScaler is applied before classification.
            Input feature order and units must match the training pipeline.
        </div>
        """
    )

    st.warning(
        "The CWRU model's performance on this dataset does not guarantee "
        "generalization to unseen motors, different test rigs or real "
        "industrial operating conditions. Minimum was identified as an "
        "influential feature, so dataset-related confounding must be considered."
    )

    st.divider()

    # ==================================================
    # 03 - NASA MODEL
    # ==================================================

    insights_section(
        "03 / NASA IMS ANOMALY DETECTION",
        "Isolation Forest Model",
        "Unsupervised anomaly detection using six experimental "
        "bearing degradation indicators."
    )

    nasa_params = nasa_model.get_params()

    nasa_col1, nasa_col2, nasa_col3 = st.columns(3)

    with nasa_col1:
        insights_metric(
            "Algorithm",
            "Isolation Forest",
            "Unsupervised learning",
            "#579BFF"
        )

    with nasa_col2:
        insights_metric(
            "Estimators",
            nasa_params.get("n_estimators"),
            "Number of decision trees",
            "#24C8B5"
        )

    with nasa_col3:
        insights_metric(
            "Contamination",
            f"{nasa_params.get('contamination') * 100:.0f}%",
            "Experimental model setting",
            "#F5A742"
        )

    st.markdown("")

    st.markdown(
        '<p class="section-title">NASA MODEL CONFIGURATION</p>',
        unsafe_allow_html=True
    )

    nasa_details = pd.DataFrame({
        "Parameter": [
            "Algorithm",
            "Number of Estimators",
            "Contamination Setting",
            "Random State",
            "Input Features"
        ],
        "Value": [
            type(nasa_model).__name__,
            nasa_params.get("n_estimators"),
            nasa_params.get("contamination"),
            nasa_params.get("random_state"),
            len(models["nasa_features"])
        ]
    })

    st.dataframe(
        nasa_details,
        use_container_width=True,
        hide_index=True
    )

    # ==================================================
    # MODEL INPUT FEATURES — INTERACTIVE EXPLANATIONS
    # ==================================================

    insights_section(
        "NASA MODEL INPUT FEATURES",
        "Model Input Features",
        "Understand the six features used by the NASA IMS Isolation Forest model."
    )

    st.markdown("### Bearing 3")

    with st.expander("B3_HI — Bearing 3 Health Indicator"):
        st.markdown("""
        - Represents the relative vibration level of Bearing 3.
        - Calculated by comparing its RMS value with a baseline vibration level.
        - A value near 1 indicates a level close to the baseline.
        - A higher value indicates increased vibration relative to the baseline.
        - It is an experimental monitoring indicator, not a health percentage.
        """)

    with st.expander("B3_Degradation_Rate — Bearing 3 Degradation Rate"):
        st.markdown("""
        - Measures how quickly the Bearing 3 Health Indicator changes.
        - A positive value indicates an increasing Health Indicator.
        - A negative value indicates a decreasing Health Indicator.
        - A value near zero indicates relatively little change.
        - It is calculated over record intervals, not fixed time intervals.
        """)

    with st.expander("B3_Acceleration — Bearing 3 Degradation Acceleration"):
        st.markdown("""
        - Measures how the degradation rate of Bearing 3 changes.
        - A positive value indicates that the degradation rate is increasing.
        - A negative value indicates that the degradation rate is decreasing.
        - A value near zero indicates little change in the degradation rate.
        """)

    st.markdown("### Bearing 4")

    with st.expander("B4_HI — Bearing 4 Health Indicator"):
        st.markdown("""
        - Represents the relative vibration level of Bearing 4.
        - Calculated by comparing its RMS value with a baseline vibration level.
        - A value near 1 indicates a level close to the baseline.
        - A higher value indicates increased vibration relative to the baseline.
        - It is an experimental monitoring indicator, not a health percentage.
        """)

    with st.expander("B4_Degradation_Rate — Bearing 4 Degradation Rate"):
        st.markdown("""
        - Measures how quickly the Bearing 4 Health Indicator changes.
        - A positive value indicates an increasing Health Indicator.
        - A negative value indicates a decreasing Health Indicator.
        - A value near zero indicates relatively little change.
        - It is calculated over record intervals, not fixed time intervals.
        """)

    with st.expander("B4_Acceleration — Bearing 4 Degradation Acceleration"):
        st.markdown("""
        - Measures how the degradation rate of Bearing 4 changes.
        - A positive value indicates that the degradation rate is increasing.
        - A negative value indicates that the degradation rate is decreasing.
        - A value near zero indicates little change in the degradation rate.
        """)

    st.markdown(
        '<p class="section-title">ANOMALY OUTPUT INTERPRETATION</p>',
        unsafe_allow_html=True
    )

    output_col1, output_col2 = st.columns(2)

    with output_col1:
        insights_metric(
            "PREDICTION 1",
            "Normal",
            "Observation on normal side",
            "#24C8B5"
        )

    with output_col2:
        insights_metric(
            "PREDICTION -1",
            "Anomaly",
            "Observation on anomaly side",
            "#F06B75"
        )

    st.markdown("")

    st.caption(
        "Positive decision scores indicate observations on the normal "
        "side of the model boundary. Negative scores indicate observations "
        "on the anomaly side."
    )

    st.warning(
        "Isolation Forest identifies statistical feature-distribution "
        "shifts. These are not confirmed physical failures, calibrated "
        "health probabilities or Remaining Useful Life predictions. "
        "The 3% contamination setting is an experimental model parameter."
    )

    st.divider()

    # ==================================================
    # 04 - NASA ANOMALY EVALUATION
    # ==================================================

    insights_section(
        "04 / EVALUATION FINDINGS",
        "NASA Anomaly Evaluation",
        "Comparison of model-flagged observations in the baseline "
        "and post-baseline periods."
    )

    evaluation_path = (
        RESULTS_DIR / "nasa_ims_anomaly_evaluation.csv"
    )

    if evaluation_path.exists():

        evaluation_df = pd.read_csv(evaluation_path)

        if "Anomaly_Prediction" not in evaluation_df.columns:
            st.warning(
                "Anomaly prediction column is missing from evaluation data."
            )
        else:

            total_records = len(evaluation_df)

            valid_df = evaluation_df[
                evaluation_df["Anomaly_Prediction"].isin([1, -1])
            ]

            valid_records = len(valid_df)

            anomaly_count = int(
                (valid_df["Anomaly_Prediction"] == -1).sum()
            )

            normal_count = int(
                (valid_df["Anomaly_Prediction"] == 1).sum()
            )

            overall_rate = (
                anomaly_count / valid_records * 100
                if valid_records else 0
            )

            unclassified_count = total_records - valid_records

            eval_col1, eval_col2, eval_col3, eval_col4 = st.columns(4)

            with eval_col1:
                insights_metric(
                    "CSV RECORDS",
                    f"{total_records:,}",
                    "Total evaluation rows",
                    "#579BFF"
                )

            with eval_col2:
                insights_metric(
                    "CLASSIFIED",
                    f"{valid_records:,}",
                    "Valid model predictions",
                    "#24C8B5"
                )

            with eval_col3:
                insights_metric(
                    "ANOMALIES",
                    f"{anomaly_count:,}",
                    "Model-flagged observations",
                    "#F06B75"
                )

            with eval_col4:
                insights_metric(
                    "ANOMALY RATE",
                    f"{overall_rate:.2f}%",
                    "Of classified observations",
                    "#F5A742"
                )

            st.markdown("")

            comparison = pd.DataFrame({
                "Period": ["Baseline", "Post-baseline"],
                "Valid Observations": [1517, 539],
                "Anomaly Observations": [46, 295],
                "Anomaly Rate": ["3.03%", "54.73%"]
            })

            st.markdown(
                '<p class="section-title">BASELINE VS POST-BASELINE</p>',
                unsafe_allow_html=True
            )

            st.dataframe(
                comparison,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                f"{unclassified_count:,} records were excluded from "
                "the classified-observation anomaly-rate calculation."
            )

            fig_evaluation = px.bar(
                comparison,
                x="Period",
                y="Anomaly Observations",
                color="Period",
                text="Anomaly Observations",
                color_discrete_sequence=[
                    "#24C8B5",
                    "#F06B75"
                ],
                title="Model-Flagged Observations by Period"
            )

            fig_evaluation.update_layout(
                showlegend=False,
                yaxis_title="Anomaly Observations",
                xaxis_title="Monitoring Period"
            )

            fig_evaluation = style_insights_chart(
                fig_evaluation,
                350
            )

            st.plotly_chart(
                fig_evaluation,
                use_container_width=True
            )

            st.info(
                "The post-baseline anomaly rate is higher than the baseline "
                "rate. This indicates a shift in the feature distribution "
                "relative to the baseline, not a validated physical failure."
            )

    else:
        st.warning("NASA anomaly evaluation CSV was not found.")

    st.divider()

    # ==================================================
    # 05 - FEATURE ABLATION
    # ==================================================

    insights_section(
        "05 / MODEL SENSITIVITY",
        "Feature Ablation Analysis",
        "Investigate how removing individual input features changes "
        "the Isolation Forest predictions."
    )

    ablation_path = (
        RESULTS_DIR / "nasa_ims_feature_ablation.csv"
    )

    if ablation_path.exists():

        ablation_df = pd.read_csv(ablation_path)

        st.caption(
            "Each reduced model was trained after removing one feature. "
            "Its predictions were compared with the original model."
        )

        st.dataframe(
            ablation_df,
            use_container_width=True,
            hide_index=True
        )

        if "Removed_Feature" in ablation_df.columns:
            st.caption(
                "The chart below uses the agreement column when available."
            )

            agreement_col = next(
                (
                    col for col in ablation_df.columns
                    if "agreement" in col.lower()
                ),
                None
            )

            if agreement_col:

                fig_ablation = px.bar(
                    ablation_df,
                    x="Removed_Feature",
                    y=agreement_col,
                    title="Prediction Agreement After Feature Removal",
                    color=agreement_col,
                    color_continuous_scale=[
                        "#F06B75",
                        "#24C8B5"
                    ]
                )

                fig_ablation.update_layout(
                    xaxis_title="Removed Feature",
                    yaxis_title="Agreement (%)",
                    coloraxis_showscale=False
                )

                fig_ablation = style_insights_chart(
                    fig_ablation,
                    400
                )

                st.plotly_chart(
                    fig_ablation,
                    use_container_width=True
                )

        st.info(
            "Feature ablation measures model sensitivity to feature "
            "removal. It is not physical feature importance or "
            "predictive accuracy."
        )

    else:
        st.warning("Feature ablation CSV was not found.")

    st.divider()

    # ==================================================
    # 06 - SPEARMAN CORRELATION
    # ==================================================

    insights_section(
        "06 / CORRELATION ANALYSIS",
        "NASA Feature Correlation with Anomaly Score",
        "Exploratory Spearman rank correlations between model input "
        "features and Isolation Forest decision scores."
    )

    correlation_data = pd.DataFrame({
        "Feature": [
            "B3_HI",
            "B4_HI",
            "B3_Degradation_Rate",
            "B4_Degradation_Rate",
            "B4_Acceleration",
            "B3_Acceleration"
        ],
        "Spearman Correlation": [
            -0.599092,
            -0.568349,
            -0.456765,
            -0.308825,
            -0.106569,
            -0.051530
        ]
    })

    fig_correlation = px.bar(
        correlation_data,
        x="Spearman Correlation",
        y="Feature",
        orientation="h",
        color="Spearman Correlation",
        color_continuous_scale="RdBu",
        range_color=[-1, 1],
        title="Spearman Correlation with Anomaly Score"
    )

    fig_correlation.update_layout(
        xaxis_title="Spearman Correlation",
        yaxis_title="NASA Feature",
        coloraxis_showscale=False
    )

    fig_correlation = style_insights_chart(
        fig_correlation,
        420
    )

    st.plotly_chart(
        fig_correlation,
        use_container_width=True
    )

    st.dataframe(
        correlation_data,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Negative correlations indicate that higher feature values "
        "tend to accompany lower anomaly scores in this dataset. "
        "Correlation does not establish causation or feature importance."
    )

    st.divider()

    # ==================================================
    # 07 - SAVED MODEL ARTIFACTS
    # ==================================================

    insights_section(
        "07 / MODEL STORAGE",
        "Saved Model Artifacts",
        "Availability and file sizes of the trained models "
        "and preprocessing artifacts."
    )

    artifact_names = [
        "best_bearing_fault_model.pkl",
        "bearing_feature_scaler.pkl",
        "nasa_ims_isolation_forest.pkl",
        "nasa_ims_features.pkl"
    ]

    artifact_data = []

    for filename in artifact_names:

        file_path = MODEL_DIR / filename

        artifact_data.append({
            "Artifact": filename,
            "Status": (
                "Available" if file_path.exists()
                else "Missing"
            ),
            "Size (KB)": (
                round(file_path.stat().st_size / 1024, 2)
                if file_path.exists()
                else None
            )
        })

    artifact_df = pd.DataFrame(artifact_data)

    st.dataframe(
        artifact_df,
        use_container_width=True,
        hide_index=True
    )

    available_count = sum(
        item["Status"] == "Available"
        for item in artifact_data
    )

    missing_count = len(artifact_data) - available_count

    status_col1, status_col2 = st.columns(2)

    with status_col1:
        insights_metric(
            "AVAILABLE ARTIFACTS",
            available_count,
            "Saved model and preprocessing files",
            "#24C8B5"
        )

    with status_col2:
        insights_metric(
            "MISSING ARTIFACTS",
            missing_count,
            "Files requiring attention",
            "#F06B75" if missing_count else "#579BFF"
        )

    st.markdown("")

    # ==================================================
    # 08 - PROJECT LIMITATIONS
    # ==================================================

    insights_section(
        "08 / SYSTEM LIMITATIONS",
        "Project Limitations and Validation Requirements",
        "Important considerations when interpreting the current "
        "experimental predictive-maintenance system."
    )

    limitations = [
        "CWRU model generalization to real industrial motors is not established.",
        "NASA anomaly detection identifies statistical feature shifts, not confirmed physical failures.",
        "NASA monitoring indicators are experimental and their thresholds are not validated failure boundaries.",
        "Isolation Forest contamination is an experimental model parameter.",
        "No validated Remaining Useful Life prediction is available.",
        "Further validation using real industrial motor data is required."
    ]

    for index, limitation in enumerate(limitations, start=1):

        st.html(
            f"""
            <div style="
                background:#101923;
                border:1px solid #263746;
                border-radius:9px;
                padding:12px 15px;
                margin-bottom:8px;
                color:#B9C9D6;
                font-size:12px;
                line-height:1.6;
            ">
                <span style="
                    color:#F5A742;
                    font-weight:700;
                ">{index:02d}</span>
                &nbsp;&nbsp; {limitation}
            </div>
            """
        )

    st.markdown("")

    # --------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------

    if missing_count == 0:

        st.success(
            "All four trained model artifacts are available. "
            "This dashboard page reads the saved models and does not "
            "retrain or overwrite them."
        )

    else:

        st.warning(
            f"{missing_count} model artifact(s) are missing. "
            "Check the results/models directory."
        )
