# ⚙️ MotorGuard AI
### AI-Based Predictive Maintenance System for Electric Motors

MotorGuard AI is an intelligent motor monitoring and predictive maintenance dashboard that combines machine learning, vibration signal analysis, and anomaly detection to support early identification of bearing faults and abnormal operating patterns in electric motors.

The project uses the **Case Western Reserve University (CWRU) Bearing Dataset** for bearing fault classification and the **NASA IMS Bearing Dataset** for experimental anomaly and degradation monitoring.

---

## 🚀 Project Overview

Unexpected motor failures can lead to equipment downtime, increased maintenance costs, and reduced industrial productivity.

MotorGuard AI explores how machine learning can support condition monitoring by analyzing vibration-based features and identifying patterns associated with bearing faults and abnormal behavior.

The system provides an interactive Streamlit dashboard with separate modules for bearing fault diagnosis, vibration feature analytics, model insights, and experimental anomaly monitoring.

## ✨ Key Features

- **Bearing Fault Classification:** Classifies vibration data into Normal and Outer Race Fault categories.
- **Anomaly Detection:** Identifies unusual feature patterns in NASA IMS bearing data.
- **Vibration Analytics:** Explores statistical and vibration-based features.
- **Feature Insights:** Provides explanations of important vibration indicators and degradation-related features.
- **Model Insights:** Displays model information, feature importance, and evaluation results.
- **Interactive Dashboard:** Presents results through an easy-to-use Streamlit interface.
- **Trained Model Integration:** Loads previously trained machine learning models for inference without retraining.

## 🧠 Machine Learning Models

### 1. CWRU Bearing Fault Classification

| Component | Implementation |
|---|---|
| Dataset | CWRU Bearing Dataset |
| Algorithm | Decision Tree Classifier |
| Preprocessing | StandardScaler |
| Classification | Normal / Outer Race Fault |
| Features | 10 statistical vibration features |

**Extracted features:**
- Mean
- RMS
- Standard Deviation
- Variance
- Minimum
- Maximum
- Peak-to-Peak
- Kurtosis
- Skewness
- Crest Factor

### 2. NASA IMS Anomaly Detection

| Component | Implementation |
|---|---|
| Dataset | NASA IMS Bearing Dataset |
| Algorithm | Isolation Forest |
| Number of Estimators | 200 |
| Contamination | 0.03 |
| Random State | 42 |
| Monitoring | Feature anomalies and degradation trends |

The monitoring module uses six engineered features:

- B3 Health Indicator
- B4 Health Indicator
- B3 Degradation Rate
- B4 Degradation Rate
- B3 Acceleration
- B4 Acceleration

The degradation rate and acceleration are calculated over the available record intervals.

## 🏗️ Project Architecture

```text
AI-Motor-Predictive-Maintenance/
│
├── dashboard/
│   ├── app.py
│   └── components/
│       ├── cwru_engine.py
│       ├── diagnosis_ui.py
│       ├── feature_analytics_ui.py
│       ├── model_insights_ui.py
│       ├── model_loader.py
│       └── nasa_monitoring_ui.py
│
├── notebooks/
│   ├── 01_NASA_IMS_Data_Exploration.ipynb
│   ├── 02_Complete_Dataset_Preparation.ipynb
│   ├── 05_Machine_Learning_Model_Training.ipynb
│   └── 06_Model_Validation_and_Deployment.ipynb
│
├── results/
│   ├── models/
│   │   ├── best_bearing_fault_model.pkl
│   │   ├── bearing_feature_scaler.pkl
│   │   ├── nasa_ims_features.pkl
│   │   └── nasa_ims_isolation_forest.pkl
│   │
│   ├── complete_bearing_features.csv
│   ├── feature_importance.csv
│   ├── model_comparison.csv
│   ├── nasa_ims_anomaly_evaluation.csv
│   ├── nasa_ims_feature_ablation.csv
│   └── Final_Project_Evaluation_Report.md
│
├── requirements.txt
└── .gitignore
```

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Machine Learning | Scikit-learn |
| Data Processing | NumPy, Pandas |
| Model Serialization | Joblib |
| Visualization | Plotly |
| Dashboard | Streamlit |
| Development | Jupyter Notebook |
| Version Control | Git, GitHub |
| Deployment | Streamlit Community Cloud |

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.11
- Git
- pip



## 📊 Model Artifacts

The project includes serialized machine learning artifacts:

| Artifact | Purpose |
|---|---|
| `best_bearing_fault_model.pkl` | Trained CWRU Decision Tree model |
| `bearing_feature_scaler.pkl` | Feature scaling for CWRU inference |
| `nasa_ims_isolation_forest.pkl` | Trained NASA IMS anomaly detection model |
| `nasa_ims_features.pkl` | NASA IMS feature configuration |

These files are loaded by the dashboard to perform predictions and monitoring.

## ⚠️ Important Limitations

- CWRU classification is based on the available experimental dataset and may not generalize directly to every real-world motor.
- Model-estimated class probabilities are not guarantees of diagnostic accuracy.
- NASA IMS anomaly flags indicate statistical deviations in the monitored features; they do not independently confirm physical bearing failure.
- The anomaly detection module does not provide validated Remaining Useful Life (RUL) predictions.
- This project is an experimental condition-monitoring and decision-support system, not a replacement for professional industrial inspection.

## 🎯 Project Objectives

1. Apply machine learning to electric motor bearing fault classification.
2. Extract meaningful statistical features from vibration signals.
3. Explore anomaly detection using Isolation Forest.
4. Investigate feature trends associated with bearing degradation.
5. Develop an interactive predictive maintenance dashboard.
6. Demonstrate the integration of machine learning with industrial condition monitoring.

## 🔮 Future Enhancements

- Real-time vibration sensor integration.
- IoT-based motor condition monitoring.
- Deep learning-based fault classification.
- Advanced bearing degradation analysis.
- Validated Remaining Useful Life estimation.
- Integration with industrial monitoring systems such as SCADA.



*MotorGuard AI — Making motor condition monitoring smarter through data-driven intelligence.*
