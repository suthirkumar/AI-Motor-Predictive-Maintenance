
import pandas as pd

from dashboard.components.model_loader import (
    load_models,
    CWRU_FEATURES
)


def predict_bearing_fault(feature_values):

    # Load trained models
    models = load_models()

    model = models["cwru_model"]
    scaler = models["cwru_scaler"]

    # Arrange input features in training order
    input_df = pd.DataFrame(
        [feature_values],
        columns=CWRU_FEATURES
    )

    # Apply the original trained scaler
    scaled_array = scaler.transform(input_df)
    scaled_input = pd.DataFrame(
        scaled_array,
        columns=CWRU_FEATURES
    )

    # Predict bearing condition
    prediction = model.predict(scaled_input)[0]

    # Get model-estimated class probabilities
    probabilities = model.predict_proba(scaled_input)[0]

    # Map class labels
    class_names = {
        0: "Normal",
        1: "Outer Race Fault"
    }

    result = class_names[int(prediction)]

    confidence = float(max(probabilities)) * 100

    return {
        "prediction": result,
        "confidence": round(confidence, 2),
        "probabilities": {
            class_names[int(label)]: round(float(prob) * 100, 2)
            for label, prob in zip(model.classes_, probabilities)
        }
    }
