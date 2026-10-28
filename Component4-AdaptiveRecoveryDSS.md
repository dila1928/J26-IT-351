# PepperCare AI — Adaptive Recovery Decision Support System (Component 4)

## 1. Project Overview

The **AI-Based Adaptive Recovery Decision Support System (DSS)** is Component 4 of the research project titled:

**Development of a Multimodal AI Framework for Early Bell Pepper Stress Detection and Adaptive Recovery in Greenhouse Environments**

PepperCare AI aims to help greenhouse farmers identify appropriate recovery actions when bell pepper plants experience stress.

The Adaptive Recovery DSS receives results from the RGB-based plant stress detection, thermal-based plant stress detection, and environmental stress prediction components. It combines the available evidence with contextual information, such as the plant's growth stage, to generate explainable and prioritized recovery recommendations.

Unlike a system that only identifies plant stress, this component focuses on **what action should be considered, why it is recommended, and what evidence supports the decision**.

## 2. Objectives

The main objectives of Component 4 are to:

- Integrate results from the RGB, thermal, and environmental components.
- Identify the primary plant stress concern using available evidence.
- Consider stress severity, growth stage, and environmental conditions.
- Select suitable recovery actions using transparent decision rules.
- Assign an appropriate priority to each recommendation.
- Explain the reasoning behind each recommendation.
- Provide supporting agronomic evidence where available.
- Identify conflicting or insufficient evidence that requires further verification.
- Support integration with the PepperCare AI mobile application.

## 3. System Architecture

The component follows this general workflow:

```text
RGB Stress Detection Results
             |
Thermal Stress Detection Results
             |
Environmental Prediction Results
             |
Growth Stage and Contextual Data
             |
             v
      Input Validation
             |
             v
       Evidence Fusion
             |
             v
    Recovery Decision Engine
             |
             v
     Agronomic Knowledge Base
             |
             v
   Explanation and Prioritization
             |
             v
       Recovery Plan Output
             |
             v
       PepperCare AI Mobile App
```

The workflow represents the intended architecture. The actual implementation should be checked against the current source code before treating every stage as completed.

## 4. Main Features

### 4.1 Multimodal Evidence Integration

The DSS is designed to receive information from three upstream components:

- **RGB component:** Provides plant stress classification based on visible plant characteristics.
- **Thermal component:** Provides relevant thermal analysis results.
- **Environmental component:** Provides environmental stress predictions and available greenhouse measurements.

The DSS evaluates the available outputs together rather than relying on a single signal in every situation.

### 4.2 Context-Aware Recovery Recommendations

The decision process considers the plant's condition and relevant context, including its growth stage and environmental conditions.

This helps the system select recommendations that are appropriate to the available evidence and the situation being assessed.

### 4.3 Rule-Based Decision Engine

A transparent rule-based engine is used to evaluate available evidence and select recovery actions.

Rules can consider:

- Plant stress category.
- Severity.
- Growth stage.
- Environmental conditions.
- Supporting evidence.
- Missing or conflicting information.

The rules should be based on reliable agricultural sources and reviewed by an agricultural expert before being treated as validated recommendations.

### 4.4 Explainable Recommendations

Each recovery plan is designed to explain:

- The primary identified concern.
- The recommended action.
- Why the action was selected.
- Which inputs and rules support the recommendation.
- Any uncertainty or missing information.

### 4.5 Safe Handling of Uncertain Results

When input results conflict or the evidence is insufficient, the DSS should request further verification instead of producing an unsupported recommendation.

A healthy status should not be assigned merely because the system cannot find a matching recovery rule.

### 4.6 Farmer-Friendly Output

The system is intended to provide understandable recovery guidance through the PepperCare AI mobile application.

The interface should present recommendations in simple language so that farmers can understand the identified concern and the suggested next steps.

## 5. Supported Plant Stress Categories

The component is intended to handle the stress categories used by the upstream research components.

| Stress category | Purpose |
|---|---|
| Healthy | Supports routine monitoring when the available evidence indicates a healthy plant. |
| Water Deficit | Supports assessment of possible water-related stress and relevant recovery guidance. |
| Nutrient Deficiency | Supports assessment of possible nutrient-related stress. |
| Aphid | Supports assessment of possible aphid-related plant damage. |
| Thrips | Supports assessment of possible thrips-related plant damage. |
| Environmental stress | Provides relevant context, such as heat stress, when reported by the environmental component. |

The exact input categories and field names must match the interfaces agreed upon with the other research components.

## 6. Technology Stack

The planned technology stack includes:

| Technology | Purpose |
|---|---|
| Python | Main programming language for the backend and decision logic. |
| FastAPI | REST API development and integration. |
| Uvicorn | Running the FastAPI application during development. |
| Pydantic | Request and response data validation. |
| Pandas | Dataset preparation and evaluation where required. |
| Pytest | Automated testing of the decision engine and API. |
| Rule-based engine | Transparent selection and prioritization of recovery actions. |
| Agronomic knowledge base | Stores recovery rules and supporting agricultural evidence. |
| Firebase Firestore | Optional data persistence if implemented and required. |
| React Native | Mobile application development, handled as part of the wider system. |
| Figma / Stitch | UI design and prototyping. |

The table describes the intended technology stack. Only technologies actually installed and integrated should be reported as implemented.

## 7. Project Structure

A suggested project structure is:

```text
adaptive-recovery-dss/
│
├── app.py
├── models.py
├── config.py
├── fusion.py
├── decision_engine.py
├── knowledge_base.py
├── explanation.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── tests/
│   ├── test_models.py
│   ├── test_fusion.py
│   ├── test_decision_engine.py
│   └── test_api.py
│
└── dataset/
    └── README.md
```

### Main files

- `app.py` — FastAPI application and API endpoints.
- `models.py` — Input and output data models.
- `config.py` — Application configuration.
- `fusion.py` — Integration and evaluation of incoming component evidence.
- `decision_engine.py` — Recovery action selection and prioritization.
- `knowledge_base.py` — Agronomic rules and supporting references.
- `explanation.py` — Generation of explanations for selected actions.
- `requirements.txt` — Python package dependencies.
- `tests/` — Automated software tests.
- `dataset/` — Dataset-related files, where applicable.

This structure is a recommended layout. Update it to reflect the actual files in the repository.

## 8. Installation and Setup

### Prerequisites

Install:

- Python 3.12.10 or a compatible version supported by the selected dependencies.
- Visual Studio Code or another Python-compatible editor.
- Git, if version control is required.

### Step 1: Clone the repository

Replace the example URL with the actual repository URL.

```bash
git clone <YOUR_REPOSITORY_URL>
cd adaptive-recovery-dss
```

Alternatively, open the project folder directly in VS Code.

### Step 2: Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Ensure that `requirements.txt` contains the dependencies actually used by the project.

### Step 4: Start the backend

If `app.py` exposes a FastAPI application named `app`, run:

```powershell
uvicorn app:app --reload --host 127.0.0.1 --port 8002
```

The server should start if the dependencies and application configuration are correct.

## 9. API Documentation

If the backend provides the expected FastAPI endpoints, the following URLs can be used during local development:

| Endpoint | Purpose |
|---|---|
| `GET /health` | Checks whether the API is running. |
| `POST /generate-recovery-plan` | Accepts plant analysis results and returns a recovery plan. |
| `/docs` | Interactive API documentation. |

Open the API documentation in a browser:

```text
http://127.0.0.1:8002/docs
```

Health endpoint:

```text
http://127.0.0.1:8002/health
```

These paths assume that the application implements the corresponding endpoints. Verify them against `app.py`.

## 10. Example Request

The following is an illustrative request for software testing. It is not a real plant diagnosis.

```json
{
  "plant_id": "BP-001",
  "rgb_result": {
    "stress_type": "Water Deficit",
    "severity": "High"
  },
  "thermal_result": {
    "stress_type": "Heat Stress",
    "severity": "Moderate"
  },
  "environmental_result": {
    "stress_type": "Heat Stress",
    "risk_level": "High"
  },
  "growth_stage": "Flowering & pollination"
}
```

The actual request format must match the Pydantic models and the API contract agreed upon with the upstream components.

## 11. Expected Recovery Plan Output

A successful decision may return a structured response containing fields similar to:

```json
{
  "plant_id": "BP-001",
  "primary_problem": "Water Deficit",
  "severity": "High",
  "recommended_action": "Verify soil moisture and assess irrigation conditions.",
  "priority": "High",
  "why_this_action": "The incoming evidence indicates possible water-related stress. The recommendation must be assessed against the available environmental measurements and applicable agronomic rules.",
  "supporting_evidence": [],
  "verification_required": true
}
```

This JSON is an illustrative output schema, not a claim that the current implementation returns these exact fields or that this example recommendation is agronomically validated.

The final response should include genuine supporting references where available. It should request further verification when evidence is insufficient.

## 12. Testing and Validation

Testing should cover both software correctness and the agricultural suitability of the recommendations.

### Software testing

Test the system with:

- Healthy plant inputs.
- Water deficit.
- Nutrient deficiency.
- Aphid detection.
- Thrips detection.
- Environmental heat stress.
- Missing component results.
- Invalid input values.
- Conflicting predictions.
- Unknown stress categories.
- Insufficient evidence.
- API errors.

### Evaluation

Potential evaluation methods include:

- Recommendation agreement with expert or reference decisions.
- Precision, recall and F1-score for suitable classification tasks.
- Correct handling of missing and conflicting inputs.
- API and integration testing.
- Agricultural expert review of the recommendations.

Evaluation metrics should only be reported after the tests have been implemented and run. Synthetic test results must not be presented as real-world agricultural validation.

## 13. Safety and Limitations

The DSS is a decision-support tool. Its recommendations require appropriate evidence and validation.

- Do not treat every environmental risk as proof of a plant disease.
- Do not declare a plant healthy solely because no decision rule matches.
- Do not invent missing sensor readings or supporting references.
- Do not prescribe arbitrary fertilizer dosages or pesticide applications.
- Identify contradictory or insufficient evidence.
- Refer uncertain or potentially harmful decisions for further inspection or expert review.
- Clearly distinguish provisional rules from agronomically validated recommendations.

The quality of the final recommendations depends on the reliability of the upstream component outputs, the knowledge base, and the validation process.

## 14. Research Contribution

The intended contribution of Component 4 is a context-aware, explainable recovery decision-support mechanism that transforms outputs from multiple plant and environmental analysis components into prioritized recovery recommendations.

The component emphasizes:

- Integration of multimodal evidence.
- Growth-stage-aware decision-making.
- Transparent, rule-based reasoning.
- Evidence-supported recommendations.
- Explainability for farmers.
- Explicit handling of uncertainty and conflicting inputs.

These contributions should be evaluated against relevant prior research and agricultural expert feedback before making claims about novelty or effectiveness.

## 15. Scope Exclusions

The component focuses on recovery decision support.

The following are outside its defined scope unless the research requirements are formally changed:

- Training the RGB plant stress detection model.
- Training the thermal stress detection model.
- Replacing the environmental prediction component.
- Yield prediction or production forecasting.
- Unverified automated pesticide or fertilizer prescriptions.

## 16. Future Improvements

Possible future improvements include:

- Integration with real outputs from all upstream components.
- Expansion of the agronomic knowledge base.
- Agricultural expert validation.
- Integration with the mobile application.
- Evaluation using suitable reference datasets.
- Improved handling of conflicting or missing evidence.
- Persistent recommendation history, if required.
- Support for additional crops after suitable adaptation and validation.

## 17. Conclusion

The PepperCare AI Adaptive Recovery Decision Support System is designed to support greenhouse bell pepper management by converting available plant stress and environmental information into transparent, prioritized, and understandable recovery guidance.

Its effectiveness depends on correct integration, reliable agronomic evidence, careful uncertainty handling, and systematic evaluation. The ultimate goal is to help farmers understand both **what action to consider and why that action is recommended**.