
from pathlib import Path
import joblib

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Saved model directory
MODEL_DIR = PROJECT_ROOT / "results" / "models"

# CWRU feature order used during training
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


def load_models():

    # Check that all required files exist
    required_files = [
        "best_bearing_fault_model.pkl",
        "bearing_feature_scaler.pkl",
        "nasa_ims_isolation_forest.pkl",
        "nasa_ims_features.pkl"
    ]

    for filename in required_files:
        file_path = MODEL_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Required model file not found: {file_path}"
            )

    # Load existing trained models
    cwru_model = joblib.load(
        MODEL_DIR / "best_bearing_fault_model.pkl"
    )

    cwru_scaler = joblib.load(
        MODEL_DIR / "bearing_feature_scaler.pkl"
    )

    nasa_model = joblib.load(
        MODEL_DIR / "nasa_ims_isolation_forest.pkl"
    )

    nasa_features = joblib.load(
        MODEL_DIR / "nasa_ims_features.pkl"
    )

    return {
        "cwru_model": cwru_model,
        "cwru_scaler": cwru_scaler,
        "nasa_model": nasa_model,
        "nasa_features": nasa_features
    }
