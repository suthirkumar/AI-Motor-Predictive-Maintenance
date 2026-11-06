
# AI-Based Predictive Maintenance for Electric Motors
## Final Model Evaluation Report

### 1. Project Overview

This project explores machine-learning-based condition monitoring
for rotating machinery using two datasets:

1. Case Western Reserve University (CWRU) bearing dataset.
2. NASA IMS bearing run-to-failure dataset.

Two separate machine-learning approaches were developed.

### 2. CWRU Bearing Fault Classification

**Algorithm:** Decision Tree Classifier  
**Preprocessing:** StandardScaler  
**Classification task:** Normal vs Outer Race fault

Input features:
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

Saved artifacts:
- best_bearing_fault_model.pkl
- bearing_feature_scaler.pkl

Dataset feature table: 3,183 rows and 14 columns.

A held-out source-recording evaluation showed 100% accuracy
on the evaluated dataset. However, dataset-specific patterns
and recording or test-rig differences may influence this result.
Further independent validation is required.

### 3. NASA IMS Anomaly Detection

**Algorithm:** Isolation Forest  
**Number of estimators:** 200  
**Contamination:** 0.03  
**Random state:** 42

Six input features:
- B3_HI
- B4_HI
- B3_Degradation_Rate
- B4_Degradation_Rate
- B3_Acceleration
- B4_Acceleration

Training baseline:
1,517 valid observations.

Baseline anomaly observations:
46 (3.03%).

Full valid timeline:
2,056 observations.

Overall anomaly observations:
341 (16.59%).

Post-baseline anomaly observations:
295 out of 539 (54.73%).

The increased post-baseline anomaly rate indicates a change
in the feature distribution relative to the baseline.
It does not independently establish physical bearing failure.

### 4. Feature Correlation Analysis

The strongest observed feature correlation was between
B3_HI and B4_HI (Spearman correlation approximately 0.74).

Most other feature pairs showed weaker relationships.

No feature was removed solely based on correlation.

### 5. Feature Ablation Analysis

Six reduced models were evaluated by removing one feature
at a time.

The original six-feature model was retained provisionally.

Removing B3_HI increased post-baseline anomaly detection
to 83.67%.

Removing B4_Acceleration increased it to 69.39%.

These results demonstrate model sensitivity to feature selection.
They do not establish physical feature importance or accuracy.

### 6. Saved Model Artifacts

CWRU:
- models/best_bearing_fault_model.pkl
- models/bearing_feature_scaler.pkl

NASA IMS:
- models/nasa_ims_isolation_forest.pkl
- models/nasa_ims_features.pkl

Evaluation files:
- nasa_ims_anomaly_evaluation.csv
- nasa_ims_feature_ablation.csv

### 7. Limitations

1. NASA IMS sampling intervals are irregular.
2. The Isolation Forest contamination value is experimental.
3. NASA anomaly labels are not independently verified fault labels.
4. The monitoring index is an experimental relative indicator,
   not a health percentage or failure probability.
5. No validated remaining-useful-life prediction was developed.
6. CWRU results require independent validation across different
   recordings, operating conditions and machines.
7. The NASA feature-ablation results measure model sensitivity,
   not predictive accuracy.

### 8. Conclusion

The project developed two separate machine-learning prototypes:

- A supervised Decision Tree classifier for CWRU bearing faults.
- An unsupervised Isolation Forest model for NASA IMS
  experimental anomaly detection.

Both models and their required preprocessing artifacts
have been saved for future integration.

The next development stage is dashboard integration,
followed by further validation using independent data
and realistic operating conditions.
