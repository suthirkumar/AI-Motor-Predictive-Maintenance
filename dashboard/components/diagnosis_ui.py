
import streamlit as st
import plotly.graph_objects as go

from dashboard.components.cwru_engine import predict_bearing_fault


def render_diagnosis_page():

    # --------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------

    st.markdown(
        '<div class="eyebrow">CWRU BEARING INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="main-title">Bearing Fault Diagnosis</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Vibration-based bearing condition '
        'classification using the trained Decision Tree model.</p>',
        unsafe_allow_html=True
    )

    st.divider()

    # --------------------------------------------------
    # MODEL INFORMATION
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">MODEL ALGORITHM</div>
            <div class="metric-value">Decision Tree</div>
            <div class="metric-caption">Trained CWRU model</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">INPUT FEATURES</div>
            <div class="metric-value">10</div>
            <div class="metric-caption">Statistical vibration features</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">CLASSIFICATION</div>
            <div class="metric-value">2 Classes</div>
            <div class="metric-caption">Normal / Outer Race Fault</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # --------------------------------------------------
    # FEATURE INPUT
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">01 | Vibration Feature Input</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Enter the 10 statistical features extracted from a vibration "
        "signal. Values must use the same feature definitions, units "
        "and preprocessing conventions as the training dataset."
    )

    feature_config = [
        ("Mean", "Mean", 0.01, -100.0, 100.0, 0.001),
        ("RMS", "Root Mean Square", 0.15, 0.0, 100.0, 0.001),
        ("Standard_Deviation", "Standard Deviation", 0.15, 0.0, 100.0, 0.001),
        ("Variance", "Variance", 0.0225, 0.0, 10000.0, 0.001),
        ("Minimum", "Minimum", -0.5, -100.0, 100.0, 0.001),
        ("Maximum", "Maximum", 0.5, -100.0, 100.0, 0.001),
        ("Peak_to_Peak", "Peak to Peak", 1.0, 0.0, 200.0, 0.001),
        ("Kurtosis", "Kurtosis", 3.0, -100.0, 100.0, 0.01),
        ("Skewness", "Skewness", 0.0, -100.0, 100.0, 0.01),
        ("Crest_Factor", "Crest Factor", 3.33, 0.0, 100.0, 0.01)
    ]

    feature_values = {}

    with st.form("bearing_diagnosis_form"):

        st.markdown("#### Statistical Measurement Parameters")

        columns = st.columns(2)

        for index, (
            key, label, default, minimum, maximum, step
        ) in enumerate(feature_config):

            with columns[index % 2]:

                feature_values[key] = st.number_input(
                    label,
                    min_value=float(minimum),
                    max_value=float(maximum),
                    value=float(default),
                    step=float(step),
                    format="%.5f",
                    key=f"cwru_{key}"
                )

        st.markdown("")
        st.caption(
            "The initial values are demonstration inputs. Replace them "
            "with actual extracted vibration features for meaningful testing."
        )

        st.divider()

        submitted = st.form_submit_button(
            "⚡  RUN BEARING DIAGNOSIS",
            use_container_width=True,
            type="primary"
        )

    # --------------------------------------------------
    # DIAGNOSIS RESULTS
    # --------------------------------------------------

    if submitted:

        try:

            result = predict_bearing_fault(feature_values)

            prediction = result["prediction"]
            confidence = result["confidence"]
            probabilities = result["probabilities"]

            st.divider()

            st.markdown(
                '<div class="section-title">02 | Diagnostic Assessment</div>',
                unsafe_allow_html=True
            )

            if prediction == "Normal":

                st.markdown(f"""
                <div style="
                    background: linear-gradient(110deg,#102B25,#142B2B);
                    border: 1px solid #287F65;
                    border-radius: 14px;
                    padding: 22px;
                    margin: 10px 0 20px 0;
                ">
                    <div style="color:#54D9B7;font-size:11px;
                    font-weight:700;letter-spacing:1.5px;">
                        CLASSIFICATION RESULT
                    </div>
                    <div style="color:#F4F8FC;font-size:27px;
                    font-weight:700;margin-top:9px;">
                        ✓ NORMAL CONDITION
                    </div>
                    <div style="color:#A8BAC8;font-size:13px;
                    margin-top:7px;">
                        The Decision Tree classified this input as Normal.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:

                st.markdown(f"""
                <div style="
                    background: linear-gradient(110deg,#321B22,#291A22);
                    border: 1px solid #944653;
                    border-radius: 14px;
                    padding: 22px;
                    margin: 10px 0 20px 0;
                ">
                    <div style="color:#FF8791;font-size:11px;
                    font-weight:700;letter-spacing:1.5px;">
                        CLASSIFICATION RESULT
                    </div>
                    <div style="color:#F4F8FC;font-size:27px;
                    font-weight:700;margin-top:9px;">
                        ⚠ OUTER RACE FAULT
                    </div>
                    <div style="color:#D6B5BA;font-size:13px;
                    margin-top:7px;">
                        The Decision Tree classified this input as
                        Outer Race Fault.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">PREDICTED CONDITION</div>
                """, unsafe_allow_html=True)

                st.markdown(
                    f'<div class="metric-value" style="font-size:23px;">'
                    f'{prediction}</div>',
                    unsafe_allow_html=True
                )

                st.markdown("</div>", unsafe_allow_html=True)

            with col2:

                st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">MODEL-ESTIMATED CLASS PROBABILITY</div>
                """, unsafe_allow_html=True)

                st.markdown(
                    f'<div class="metric-value">{confidence:.2f}%</div>',
                    unsafe_allow_html=True
                )

                st.markdown("</div>", unsafe_allow_html=True)

                st.caption(
                    "Probability represents the Decision Tree's estimated class "
                    "distribution at the reached leaf. It should not be interpreted "
                    "as a guarantee of diagnostic accuracy or actual motor health."
                )

            # --------------------------------------------------
            # CLASS PROBABILITY CHART
            # --------------------------------------------------

            st.markdown(
                '<div class="section-title">03 | Class Probability Distribution</div>',
                unsafe_allow_html=True
            )

            class_names = list(probabilities.keys())
            probability_values = list(probabilities.values())

            bar_colors = [
                "#24C8B5" if name == "Normal" else "#F06B75"
                for name in class_names
            ]

            fig = go.Figure(
                go.Bar(
                    x=class_names,
                    y=probability_values,
                    marker=dict(
                        color=bar_colors,
                        line=dict(width=0)
                    ),
                    text=[
                        f"{value:.2f}%"
                        for value in probability_values
                    ],
                    textposition="outside"
                )
            )

            fig.update_layout(
                title=dict(
                    text="Decision Tree Class Probabilities",
                    font=dict(size=17, color="#E8F0F6")
                ),
                yaxis_title="Model-estimated probability (%)",
                yaxis=dict(
                    range=[0, 115],
                    gridcolor="#253746",
                    zeroline=False
                ),
                xaxis=dict(
                    title="Bearing Condition",
                    gridcolor="#253746"
                ),
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="#E8F0F6",
                    family="DM Sans"
                ),
                height=400,
                margin=dict(l=30, r=30, t=70, b=40),
                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        except Exception as error:

            st.error(f"Diagnosis failed: {error}")
