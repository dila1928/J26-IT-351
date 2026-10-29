# Environmental Stress Prediction Component

**Project:** PepperCare AI --- Multimodal AI Framework for Bell Pepper
Plant Stress Detection and Adaptive Recovery Decision Support\
**Component:** AI-Based Environmental Stress Prediction\
**Model version recorded in metadata:** `environmental-stress-v2`\
**Status:** Research prototype

## Overview

This component analyses environmental readings for greenhouse bell
pepper cultivation and estimates possible stress risks over the next
**30 minutes** and **60 minutes**. It connects a Flutter mobile
interface to a Python FastAPI backend.

It provides two functions:

1.  **Current environment assessment:** compares readings with
    growth-stage-based reference ranges and reports whether each factor
    is within or outside its range.
2.  **Future stress prediction:** uses saved machine-learning models to
    estimate stress type, risk level, and risk score for 30 and
    60 minute horizons.


## Objectives

-   Assess current environmental readings for bell pepper plants.
-   Consider plant growth stage when checking environmental conditions.
-   Predict short term stress type, risk level, and risk score.
-   Explain the main environmental factors contributing to predicted
    risk.
-   Display results in a mobile interface and save them for later
    review.
-   Prepare structured prediction data for the Adaptive Recovery
    workflow.

## Main Features

-   **Manual mode:** users enter environmental readings.
-   **Auto mode:** a virtual sensor replay provides simulated readings
    from a dataset.
-   **Current environment check:** compares readings with reference
    ranges.
-   **Future prediction:** returns separate 30 minute and 60 minute
    predictions.
-   **Contributing factors:** identifies environmental factors
    associated with the result.
-   **History:** supports saving and retrieving readings and predictions
    through Firebase Firestore.
-   **API testing:** endpoints can be tested with Swagger UI and
    Postman.

## Architecture

``` mermaid
flowchart TD
    A["Greenhouse Worker / Supervisor"] --> B["Flutter Mobile App"]
    B -->|"HTTP + JSON"| C["FastAPI Backend"]
    C --> D["Request Validation"]
    D --> E["Rule-Based Current Assessment"]
    D --> F["Machine-Learning Prediction"]
    E --> G["Growth-Stage Reference Ranges"]
    F --> H["Saved Random Forest Models"]
    H --> I["30-minute and 60-minute predictions"]
    E --> J["Current Environment Status"]
    I --> K["Stress Type, Risk Levels and Scores"]
    J --> L["JSON Response"]
    K --> L
    L --> B
    B <--> M["Firebase Firestore"]
    N["Virtual Sensor Replay Dataset"] --> C
```

| Layer | Responsibility |
|---|---|
| Presentation | Flutter screens for entering readings and viewing results. |
| API/service | FastAPI receives and validates requests and returns JSON responses. |
| Current assessment | Compares readings with growth-stage-based reference ranges. |
| ML prediction | Predicts stress type, risk level, and risk score for 30 and 60 minutes. |
| Storage | Firestore stores user-specific readings and prediction history; model artifacts are stored separately. |


## Technology Stack

  | Technology | Purpose |
|---|---|
| Flutter / Dart | Mobile user interface. |
| Python | Data preparation, feature engineering, and backend integration. |
| FastAPI | REST API endpoints. |
| Random Forest | Saved models used by the current prediction prototype. |
| pandas / NumPy | Dataset processing and numerical feature preparation. |
| scikit-learn | Machine-learning utilities and model processing. |
| joblib / `.pkl` files | Loading and reusing trained model artifacts. |
| Firebase Firestore | Saving and retrieving readings and predictions. |
| Swagger UI / Postman | API testing. |
| Virtual sensor CSV replay | Simulated readings for Auto mode. |


## Inputs

  -------------------------------------------------------------------------
  Input                     Description             Unit / format
  ------------------------- ----------------------- -----------------------
  `timestamp`               Time associated with    ISO date-time string
                            the reading             

  `growth_stage`            Current bell pepper     Text category
                            growth stage            

  `air_temperature_c`       Air temperature         °C

  `relative_humidity_pct`   Relative humidity       \%

  `light_intensity_lux`     Light intensity         lux

  `soil_temperature_c`      Soil temperature        °C

  `historical_context`      Optional previous       List of readings
                            readings                
  -------------------------------------------------------------------------

The feature pipeline also creates historical and time-related features,
including lagged readings, rolling statistics, and time encodings.

## Outputs

The future-prediction API can return:

-   `stress_type` --- predicted environmental stress category.
-   `risk_30m` --- risk level and score for 30 minutes.
-   `risk_60m` --- risk level and score for 60 minutes.
-   `main_contributing_factors` --- environmental factors associated
    with the result.
-   `explanation` --- explanation of the predicted risk.
-   `current_environment` --- readings used for prediction.
-   `model_version` --- model version recorded by the backend.
-   `recovery_handoff` --- structured information prepared for the
    Adaptive Recovery workflow.
-   `data_source_mode` --- identifies the data-source mode.

Current-environment assessment is rule-based and separate from the
future ML prediction.

## Model and Dataset Details

-   **Model version:** `environmental-stress-v2`
-   **Recorded training date:** `2026-09-26`
-   **Dataset:** approximately 5,758 records in
    `model_training_table.csv`
-   **Feature count:** 45
-   **Prediction horizons:** 30 and 60 minutes
-   **Saved artifacts:** six model files covering stress type, risk
    level, and risk score at both horizons
-   **Artifact format:** `.pkl`

The recorded split files contain 4,031 training records, 864 validation
records, and 863 test records.

### Recorded Prototype Evaluation Metrics

These values were recorded in the model metadata. They are prototype
metrics, not proof of real-world greenhouse accuracy.

  Metric                         30 minutes   60 minutes
  ---------------------------- ------------ ------------
  Stress-type accuracy               69.87%       68.02%
  Stress-type macro F1-score          0.528        0.387
  Risk-level accuracy                96.41%       95.02%
  Risk-level macro F1-score           0.872        0.834
  Risk-score MAE                       4.49         5.09

Accuracy should be interpreted alongside macro F1-score and the label
distribution. Stronger evaluation requires an untouched test set and
independent validation against observed greenhouse outcomes.

## API Endpoints

### Integrated unified backend

  ------------------------------------------------------------------------------------
  Method                  Endpoint                             Purpose
  ----------------------- ------------------------------------ -----------------------
  `GET`                   `/environmental/health`              Checks whether model
                                                               artifacts are loaded.

  `POST`                  `/environmental/auto-log`            Retrieves and saves the
                                                               next simulated reading.

  `POST`                  `/environmental/check-environment`   Assesses current
                                                               environmental readings.

  `POST`                  `/environmental/predict`             Generates 30- and
                                                               60-minute predictions.
  ------------------------------------------------------------------------------------

### Standalone model API

  Method   Endpoint               Purpose
  -------- ---------------------- -------------------------------
  `GET`    `/health`              Checks model readiness.
  `POST`   `/check-environment`   Assesses current readings.
  `POST`   `/predict`             Generates future predictions.

The standalone service uses root-level paths; the unified backend adds
the `/environmental` prefix.

### Example prediction request

``` json
{
  "timestamp": "2026-10-21T14:00:00",
  "growth_stage": "Flowering",
  "air_temperature_c": 36.0,
  "relative_humidity_pct": 45.0,
  "light_intensity_lux": 50000.0,
  "soil_temperature_c": 30.0
}
```

## Run the Standalone API on Windows

These commands start the existing API and do not retrain the models.

1.  Open PowerShell or the VS Code terminal in the
    `ENVIRONMENTAL-STRESS-PREDICTION` folder.

2.  Create and activate a Windows virtual environment:

    ``` powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

3.  Install dependencies:

    ``` powershell
    python -m pip install -r requirements.txt
    ```

4.  Start the API:

    ``` powershell
    python -m uvicorn app:app --reload --port 8001
    ```

5.  Open Swagger UI: `http://127.0.0.1:8001/docs`

6.  Test `GET /health`, then try `POST /check-environment` or
    `POST /predict`.

If PowerShell blocks activation, run
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that
terminal and activate again.

**Testing versus retraining** - To test predictions, start `app.py` with
Uvicorn; it loads existing model artifacts. - To retrain, run
`python train.py` only when retraining is intended. Back up existing
artifacts first because the training script may replace model files.

## Firestore Storage

The Flutter app stores user-specific records under:

``` text
users/{uid}/environmental_readings/{autoId}
users/{uid}/stress_predictions/{autoId}
```

The backend Auto mode writes simulated readings to:

``` text
environmental_auto_readings
```

## Limitations and Future Work

### Current limitations

-   The training targets use derived/synthetic prototype labels, not
    confirmed plant-stress observations.
-   Auto mode uses simulated replay data rather than physical sensors.
-   Results may vary across greenhouses, cultivars, growth stages, and
    data distributions.
-   Recorded metrics require stronger independent validation before
    real-world reliability claims.
-   Predictions should be reviewed alongside greenhouse observations and
    expert advice.

### Future improvements

-   Validate and retrain with real greenhouse observations and verified
    labels.
-   Use an untouched test set and suitable time-aware validation.
-   Evaluate model calibration and performance across growth stages.
-   Integrate physical sensors when hardware becomes available.
-   Complete and test the Adaptive Recovery handoff.
-   Improve monitoring, error handling, and model-version tracking.

## Security

-   Do not commit Firebase service-account JSON keys, API secrets, or
    credentials to GitHub.
-   Keep credentials outside source control and use environment
    variables or an appropriate secrets-management mechanism.
-   Configure Firestore security rules so users can access only
    authorized records.

## Summary

The Environmental Stress Prediction component combines a Flutter mobile
interface, a FastAPI backend, rule-based current-environment assessment,
and Random Forest models for 30-minute and 60-minute risk prediction.
Firebase Firestore supports saved readings and prediction history. This
is a research prototype and requires validation using real greenhouse
observations before its predictions can be treated as confirmed
plant-stress outcomes.
