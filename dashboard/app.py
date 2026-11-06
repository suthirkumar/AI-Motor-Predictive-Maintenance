
import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="MotorGuard AI | Predictive Maintenance",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# PREMIUM INDUSTRIAL THEME
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --background: #080E14;
    --surface: #101923;
    --surface-light: #16232E;
    --border: #253746;
    --text: #E8F0F6;
    --muted: #8DA2B5;
    --teal: #24C8B5;
    --blue: #579BFF;
    --orange: #F5A742;
    --red: #F06B75;
}

.stApp {
    background:
        radial-gradient(ellipse at 80% 0%, #10232B 0%, transparent 38%),
        var(--background);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #0D1721;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: var(--muted);
}

[data-testid="stSidebar"] .stRadio label {
    color: #DCE6EE;
    font-size: 14px;
}

[data-testid="stSidebar"] hr {
    border-color: var(--border);
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
}

.main-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(46px, 5.5vw, 64px);
    font-weight: 700;
    letter-spacing: -1.2px;
    color: #F4F8FC;
    margin-bottom: 12px;
    text-align: center;
}

.subtitle {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.7;
    margin-top: 0;
}

.eyebrow {
    color: var(--teal);
    font-size: 30px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 10px;
}

.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 19px;
    font-weight: 600;
    color: var(--text);
    margin-top: 24px;
    margin-bottom: 14px;
}

.brand-title {
    font-family: 'Space Grotesk', sans-serif;
    color: #F4F8FC;
    font-size: 23px;
    font-weight: 700;
    letter-spacing: -0.8px;
}

.brand-accent {
    color: var(--teal);
}

.brand-caption {
    color: var(--muted);
    font-size: 10px;
    letter-spacing: 1.5px;
    font-weight: 600;
}

.sidebar-status {
    background: #102720;
    border: 1px solid #205345;
    border-radius: 9px;
    padding: 10px 12px;
    color: #54D9B7;
    font-size: 12px;
    font-weight: 600;
}

.metric-card {
    background: linear-gradient(145deg, #172631, #101923);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 19px;
    min-height: 140px;
    transition: all 0.2s ease;
}

.metric-card:hover {
    border-color: #287F79;
    transform: translateY(-3px);
}

.metric-label {
    color: var(--muted);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.1px;
}

.metric-value {
    color: #F4F8FC;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 29px;
    font-weight: 700;
    margin-top: 12px;
}

.metric-caption {
    color: var(--teal);
    font-size: 12px;
    margin-top: 6px;
}

.module-card {
    background: linear-gradient(145deg, #15232E, #101923);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    min-height: 155px;
    margin-bottom: 12px;
}

.module-icon {
    font-size: 23px;
    margin-bottom: 10px;
}

.module-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 600;
    color: #F1F6FA;
    margin-bottom: 8px;
}

.module-description {
    font-size: 13px;
    line-height: 1.6;
    color: var(--muted);
}

.status-online {
    color: var(--teal);
    font-weight: 600;
}

.hero-panel {
    background: linear-gradient(110deg, #142832, #10202A 65%, #122A31);
    border: 1px solid #28504F;
    border-radius: 16px;
    padding: 24px;
    margin-top: 20px;
    margin-bottom: 22px;
}

.hero-heading {
    font-family: 'Space Grotesk', sans-serif;
    color: #F4F8FC;
    font-size: 21px;
    font-weight: 700;
}

.hero-description {
    color: #A8BAC8;
    font-size: 13px;
    line-height: 1.7;
}

.footer-note {
    color: #71879A;
    font-size: 11px;
    text-align: center;
    padding-top: 22px;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

.stButton button {
    border-radius: 9px;
}

@media (max-width: 768px) {
    .block-container {
        padding-top: 1rem;
    }

    .metric-card {
        min-height: 120px;
    }
}

/* --------------------------------
   STREAMLIT WIDGET PREMIUM STYLING
--------------------------------- */

/* Main content */
[data-testid="stMain"] {
    background-color: transparent;
}

/* Input containers */
[data-testid="stNumberInput"] > div {
    background: #101923 !important;
    border: 1px solid #304454 !important;
    border-radius: 10px !important;
}

[data-testid="stNumberInput"] input {
    color: #E8F0F6 !important;
    background: transparent !important;
}

/* Input focus */
[data-testid="stNumberInput"] > div:focus-within {
    border: 1px solid #24C8B5 !important;
    box-shadow: 0 0 0 2px rgba(36, 200, 181, 0.12) !important;
}

/* Input labels */
[data-testid="stWidgetLabel"] p {
    color: #B9C9D6 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(110deg, #168F83, #24C8B5) !important;
    color: #061411 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    min-height: 45px !important;
    transition: all 0.2s ease !important;
}

/* Button hover */
.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(110deg, #24C8B5, #46E0CB) !important;
    box-shadow: 0 4px 18px rgba(36, 200, 181, 0.22) !important;
    transform: translateY(-1px);
}

/* Form container */
[data-testid="stForm"] {
    background: linear-gradient(145deg, #111F29, #0D1720) !important;
    border: 1px solid #263746 !important;
    border-radius: 15px !important;
    padding: 22px !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid #304454 !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #13212C !important;
    border: 1px solid #263746 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

[data-testid="stMetricLabel"] {
    color: #8DA2B5 !important;
}

[data-testid="stMetricValue"] {
    color: #24C8B5 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Dividers */
hr {
    border-color: #263746 !important;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div class="brand-title">
        ⚙️ MOTORGUARD <span class="brand-accent">AI</span>
    </div>
    <div class="brand-caption">
        INTELLIGENT CONDITION MONITORING
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("##### WORKSPACE")

    page = st.radio(
        "NAVIGATION",
        [
            "Executive Overview",
            "Bearing Fault Diagnosis",
            "NASA Anomaly Monitoring",
            "Feature Analytics",
            "Model Insights"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("##### SYSTEM STATUS")

    st.markdown(
        '<div class="sidebar-status">● &nbsp; Dashboard Interface Ready</div>',
        unsafe_allow_html=True
    )

    st.markdown("")

    st.caption("DATA SOURCES")
    st.caption("◈ CWRU Bearing Dataset")
    st.caption("◈ NASA IMS Dataset")

    st.divider()

    st.caption("MOTORGUARD AI")
    st.caption("Version 1.0.0")
    st.caption("Research Prototype")


# --------------------------------------------------
# EXECUTIVE OVERVIEW
# --------------------------------------------------

if page == "Executive Overview":

    st.markdown(
        """
        <div style="text-align:center; padding: 20px 0 12px 0;">
            <div class="eyebrow">
                INTELLIGENT MOTOR MONITORING SYSTEM
            </div>
            <p class="main-title">
                Motor Predictive Maintenance
            </p>
            <p class="subtitle">
                AI-powered bearing fault classification, vibration analytics
                and experimental anomaly monitoring.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="hero-panel">
        <div class="hero-heading">Industrial Intelligence. Data-Driven Decisions.</div>
        <div class="hero-description">
            A machine-learning research prototype combining CWRU bearing
            fault classification with NASA IMS condition-monitoring
            experiments in one interactive dashboard.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # SYSTEM METRICS

    st.markdown(
        '<div class="section-title">System Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("DIAGNOSIS MODEL", "READY", "CWRU Decision Tree"),
        ("MONITORING MODEL", "READY", "NASA Isolation Forest"),
        ("CWRU RECORDS", "3,183", "Extracted feature windows"),
        ("NASA RECORDS", "2,156", "Experimental observations")
    ]

    for column, metric in zip(
        [col1, col2, col3, col4],
        metrics
    ):
        with column:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{metric[0]}</div>
                <div class="metric-value">{metric[1]}</div>
                <div class="metric-caption">{metric[2]}</div>
            </div>
            """, unsafe_allow_html=True)

    # PROJECT MODULES

    st.markdown(
        '<div class="section-title">Platform Modules</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:
        st.markdown("""
        <div class="module-card">
            <div class="module-icon">⚙️</div>
            <div class="module-heading">Bearing Fault Diagnosis</div>
            <div class="module-description">
                Classifies vibration feature inputs as Normal or
                Outer Race Fault using the trained CWRU Decision Tree.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="module-card">
            <div class="module-icon">📊</div>
            <div class="module-heading">Feature Analytics</div>
            <div class="module-description">
                Explores vibration feature distributions, feature
                relationships and NASA degradation trends.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="module-card">
            <div class="module-icon">📡</div>
            <div class="module-heading">NASA Anomaly Monitoring</div>
            <div class="module-description">
                Uses Isolation Forest to identify statistical
                changes in NASA IMS monitoring features.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="module-card">
            <div class="module-icon">🧠</div>
            <div class="module-heading">Model Insights</div>
            <div class="module-description">
                Presents model configurations, evaluation findings,
                feature ablation and technical limitations.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # PROJECT SCOPE

    st.markdown(
        '<div class="section-title">Monitoring Scope</div>',
        unsafe_allow_html=True
    )

    st.warning(
        "Research prototype: NASA anomaly flags indicate statistical "
        "feature-distribution changes, not confirmed physical failures "
        "or Remaining Useful Life predictions. CWRU model performance "
        "on unseen industrial motors is not established."
    )

    st.markdown(
        '<div class="footer-note">MOTORGUARD AI · '
        'AI-BASED PREDICTIVE MAINTENANCE · RESEARCH PROTOTYPE</div>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# OTHER DASHBOARD PAGES
# --------------------------------------------------

elif page == "Bearing Fault Diagnosis":

    from dashboard.components.diagnosis_ui import render_diagnosis_page
    render_diagnosis_page()


elif page == "NASA Anomaly Monitoring":

    from dashboard.components.nasa_monitoring_ui import render_nasa_page
    render_nasa_page()


elif page == "Feature Analytics":

    from dashboard.components.feature_analytics_ui import render_feature_analytics_page
    render_feature_analytics_page()


elif page == "Model Insights":

    from dashboard.components.model_insights_ui import render_model_insights_page
    render_model_insights_page()
