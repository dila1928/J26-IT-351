
# AI-Based RGB Bell Pepper Plant Stress Detection

**Project ID:** J26_IT_351  
**Individual Component:** AI-Based RGB Bell Pepper Plant Stress Detection  
**Student ID:** IT22552174  
**Crop:** Bell Pepper (*Capsicum annuum*)  
**Application:** PepperCare AI

---

## 1. Project Overview

The AI-Based RGB Bell Pepper Plant Stress Detection component focuses on identifying visible signs of stress in bell pepper plants using RGB images.

This component is part of the research project:

**Development of a Multimodal AI Framework for Early Bell Pepper Plant Stress Detection and Adaptive Recovery Decision Support in Greenhouse Environments.**

The component analyses plant images to identify visible plant conditions and provides relevant information to support greenhouse monitoring and adaptive recovery decision-making.

Unlike systems that focus only on plant diseases, this research considers water deficit, nutrient deficiency, and pest-related damage.

## 2. Research Objectives

The main objective is to develop and evaluate an AI-based RGB image analysis approach for detecting visible stress conditions in bell pepper plants.

### Specific Objectives

- Collect and prepare RGB images of bell pepper plants.
- Preprocess images and assess their suitability for analysis.
- Develop an image classification model for identifying target plant conditions.
- Investigate stress severity assessment and affected-region estimation.
- Evaluate classification performance using appropriate metrics.
- Display RGB assessment results through the mobile application.
- Support follow-up monitoring and integration with the wider research framework.

## 3. Problem Background

Bell pepper plants can experience different forms of stress during greenhouse cultivation. Visible symptoms may include leaf discolouration, curling, wilting, changes in leaf texture, and pest-related damage.

Manual inspection can be time-consuming, and similar visible symptoms may have different underlying causes. Early symptoms can also be difficult to identify consistently.

This component investigates how image-based artificial intelligence can support the identification of visible plant conditions.

**Research focus:** Identifying visible evidence from RGB images rather than independently determining every underlying environmental or physiological cause.

## 4. Main Features

| Feature | Description |
|---|---|
| RGB Image Input | Capture or select a bell pepper plant image for analysis. |
| Image Quality Assessment | Check image suitability before analysis, where implemented. |
| Image Preprocessing | Prepare images for the AI model. |
| Stress Classification | Identify a supported plant-condition class. |
| Confidence Score | Display the model's prediction confidence. |
| Severity Assessment | Assess Mild, Moderate, or Severe conditions where a validated method is available. |
| Affected-Region Analysis | Estimate affected regions and affected-area percentage where segmentation is implemented. |
| Result Display | Present assessment results in the mobile application. |
| Result History | Save and review previous assessment results. |
| Follow-up Monitoring | Compare observations over time where implemented. |
| Multimodal Integration | Provide RGB findings to the wider research framework. |

The proposed five-class taxonomy represents the research target. The actual classes supported by a trained model depend on its training data, saved model files, and class mapping.

## 5. Target Plant-Condition Classes

| Class | Description |
|---|---|
| Healthy | Bell pepper plants without the target visible stress condition. |
| Water Deficit | Plants with verified evidence associated with insufficient water availability. |
| Nutrient Deficiency | Plants showing symptoms associated with nutrient deficiency. |
| Aphid | Plants showing verified aphid infestation evidence or associated damage. |
| Thrips | Plants showing verified thrips infestation evidence or associated damage. |

### Dataset Label Considerations

Original class labels and dataset source information should be preserved during dataset preparation.

Nutrient-specific labels such as nitrogen, phosphorus, potassium, magnesium, iron, and zinc deficiency may be mapped to the broader `Nutrient_Deficiency` class when supported by the original annotations.

Images showing overwatering must not automatically be labelled as water deficit. Uncertain symptoms should not be assigned a definite cause without supporting evidence.

Pest images originating from chilli or another crop should retain their original crop information because their suitability for bell pepper classification requires evaluation.

## 6. AI Model Approach

### 6.1 Image Classification

The recorded RGB model metadata identifies the following configuration:

| Item | Recorded Configuration |
|---|---|
| Model Version | `rgb-bellpepper-stress-v1` |
| Recorded Training Date | 26 September 2026 |
| Model Approach | Two-stage cascade |
| Backbone | EfficientNetB0 |
| Input Image Size | 256 × 256 pixels |
| AI Framework | TensorFlow / Keras |

The intended two-stage cascade approach separates classification into stages:

1. Identify whether an image is Healthy or Stressed.
2. Identify the supported stress category for images classified as Stressed.

The actual classes available for inference must match the saved model files and their class-index mapping.

**Model status note:** The recorded metadata lists `Healthy` in its flat-class list and `Aphid`, `Nutrient_Deficiency`, and `Thrips` for Stage 2. `Water_Deficit` is not listed in that metadata snapshot. Therefore, the recorded metadata does not establish that the current model supports all five target classes.

### 6.2 Image Preprocessing

The intended image-processing workflow includes:

1. Loading the submitted RGB image.
2. Checking image readability and suitability.
3. Resizing the image to the model's required input dimensions.
4. Applying the preprocessing and normalization expected by the model.
5. Passing the prepared image to the classification model.
6. Interpreting the output using the corresponding class mapping.

The preprocessing method used during inference must be consistent with the method used during model training.

### 6.3 Image Quality Assessment

Image quality can affect prediction reliability. The recorded inference-script configuration includes checks related to:

- Image blur using a Laplacian-variance threshold.
- Image brightness.
- Minimum foliage visibility.

These thresholds are implementation settings, not universal agricultural standards. Their suitability should be assessed using representative greenhouse images.

## 7. Affected-Region Segmentation and Severity

Classification identifies a predicted class, while segmentation aims to identify image regions associated with visible damage or symptoms.

A segmentation model such as U-Net may be evaluated if suitable pixel-level annotations are available.

### 7.1 Affected-Area Percentage

Where a validated segmentation method is available, affected-area percentage can be calculated as:

**Affected Area (%) = (Affected leaf pixels / Total valid leaf pixels) × 100**

Background pixels should be excluded, and the reference region should be clearly defined.

### 7.2 Severity Categories

The proposed severity categories are:

- Mild
- Moderate
- Severe

Severity should be determined using a defined and validated method. Affected-area percentage alone may not adequately represent severity across all stress classes.

Segmentation, affected-area estimation, and severity assessment should only be described as completed when supported by the actual implementation, annotations, and evaluation results.

## 8. RGB Analysis Workflow

The intended workflow is:

1. **Image Input:** A user captures or selects an RGB image of a bell pepper plant.
2. **Quality Assessment:** The image is checked for suitability.
3. **Preprocessing:** The image is prepared for AI inference.
4. **AI Classification:** The supported model predicts a plant-condition class.
5. **Result Interpretation:** The prediction and confidence are interpreted.
6. **Additional Assessment:** Severity and affected-region estimation are performed where implemented and validated.
7. **Result Presentation:** Available findings are displayed in the mobile application.
8. **Result Storage:** The assessment can be saved for later reference.
9. **Follow-up Comparison:** Observations may be compared over time where monitoring functionality is implemented.
10. **Multimodal Integration:** Structured RGB findings can support the Adaptive Recovery Decision Support System.

## 9. Mobile Application

The RGB component is designed to operate within the PepperCare AI mobile application.

### 9.1 Technologies Used

| Technology | Role |
|---|---|
| Flutter | Mobile application interface |
| Dart | Mobile application programming language |
| FastAPI | Backend API framework |
| Python | AI inference and image processing |
| TensorFlow / Keras | Recorded model implementation |
| OpenCV | Image processing and quality checks where implemented |
| Firebase Authentication | User authentication in the reviewed application |
| Cloud Firestore | Storage of RGB assessment results in the reviewed application |

### 9.2 Image Submission

The reviewed Flutter implementation communicates with the RGB prediction endpoint using:

- **HTTP Method:** `POST`
- **Endpoint:** `/rgb/predict`
- **Request Format:** `multipart/form-data`
- **Image Field:** `image`

The Flutter application and Python inference backend are separate parts of the system.

### 9.3 Result Storage

The reviewed mobile implementation provides a Save Result workflow that stores RGB results under:

`users/{uid}/rgb_results`

The available fields depend on the current result model and API response.

### 9.4 Follow-up Monitoring

The proposed monitoring approach compares observations associated with the same plant over time.

The intended follow-up statuses are:

- Improving
- Stable
- Worsening
- Recovered

These statuses require a defined comparison method and suitable historical observations. They should not be interpreted as validated recovery outcomes without supporting evidence.

## 10. Dataset Preparation

The proposed dataset organization is:

```text
RGB_BellPepper_Final_Dataset/
├── 01_Healthy/
│   └── raw/
├── 02_Water_Deficit/
│   └── raw/
├── 03_Nutrient_Deficiency/
│   └── raw/
├── 04_Aphid/
│   └── raw/
├── 05_Thrips/
│   └── raw/
├── metadata/
│   └── dataset_metadata.csv
└── evidence_screenshots/
```

### 10.1 Dataset Metadata

Each accepted image should retain information such as:

```text
filename
final_class
original_class
source
source_url
license
crop_or_species
notes
```

Dataset preparation should include checks for:

- Corrupted images.
- Duplicate files.
- Incorrect or uncertain labels.
- Class imbalance.
- Crop relevance.
- Source attribution and licence conditions.
- Suitability for the intended classification task.

Training, validation, and testing sets should be separated carefully to reduce data leakage from duplicate images, related image sequences, or images of the same plant.

### 10.2 Identified Dataset Sources

#### Healthy — PlantVillage Bell Pepper Healthy Subset

The Healthy subset should be associated with the exact repository from which the images were obtained. The source URL, applicable licence, and final usable image count should be recorded from the actual downloaded dataset.

#### Nutrient Deficiency — Pepper Nutrient Deficiency Dataset

**Source:** Mendeley Data

https://data.mendeley.com/datasets/dh5cpvn48j/1

The dataset describes *Capsicum annuum* under nutrient treatments including nitrogen (N), phosphorus (P), potassium (K), magnesium (Mg), iron (Fe), and zinc (Zn).

Original treatment labels and source attribution should be preserved.

#### Aphid — Wageningen University & Research

**Source record:**

https://research.wur.nl/en/datasets/data-underlying-the-project-lwv23041-detectie-en-behandeling-van/

Access conditions, reuse permissions, crop relevance, and the applicable licence should be confirmed before redistribution or training use.

#### Thrips — Red Chili Pepper Pests Dataset

**Source:** Kaggle

https://www.kaggle.com/datasets/indraagustian/red-chili-pepper-pests-dataset

This source is associated with a chilli/pepper domain. Original crop information should be retained, and suitability for bell pepper classification should be evaluated rather than assumed.

#### Water Deficit

A verified bell-pepper-specific RGB source with reliable water-deficit labels remains a dataset limitation in the recorded research notes.

Overwatering images or unverified wilting images should not be relabelled as water deficit merely to complete the target class list.

Actual dataset counts should be calculated from cleaned files. Placeholder metadata entries must not be treated as real training samples.

## 11. Model Evaluation

The model should be evaluated using data that were not used to train or select it.

### 11.1 Classification Metrics

| Metric | Purpose |
|---|---|
| Accuracy | Measures the proportion of correct predictions. |
| Precision | Measures how many predictions for a class are correct. |
| Recall | Measures how many reference examples of a class are identified. |
| F1-score | Combines precision and recall. |
| Macro-F1 | Gives equal weight to each class when averaging class-level F1 scores. |
| Confusion Matrix | Shows the relationship between actual and predicted classes. |

Per-class results are important because overall accuracy can hide poor performance for a minority class.

### 11.2 Segmentation Metrics

Where segmentation is implemented and reference masks are available, evaluation may include:

- Intersection over Union (IoU).
- Dice score.
- Affected-area estimation error.

Severity assessment should also be evaluated against independently labelled reference examples where suitable annotations are available.

No accuracy, Macro-F1, IoU, Dice, or severity-agreement value is claimed here without a supporting evaluation report.

## 12. Role in the Multimodal Research Framework

The RGB component provides information about visible plant conditions from ordinary images.

It complements the other research components:

| Component | Main Responsibility |
|---|---|
| RGB Stress Detection | Identifies visible stress evidence from RGB images. |
| Thermal Stress Detection | Analyses thermal evidence associated with plant stress. |
| Environmental Stress Prediction | Assesses environmental conditions and predicts future stress risk. |
| Adaptive Recovery DSS | Interprets available component outputs to support recovery decisions. |

The RGB component's intended contribution includes the predicted stress class, confidence, severity where validated, and affected-area information where available.

The RGB component does not independently determine every environmental cause or prescribe irrigation, fertilizer, or pesticide actions. Recovery recommendations belong to the Adaptive Recovery Decision Support System and require appropriate agricultural validation.

## 13. Limitations

- Similar visible symptoms can have different underlying causes.
- Public images may differ from greenhouse images in lighting, background, cultivar, and growth stage.
- Pest images from chilli may not generalize directly to bell pepper.
- A verified Water Deficit dataset is required to support the complete five-class objective.
- Model performance depends on data quality, class balance, and reliable labels.
- Severity and affected-area estimates require suitable definitions and validation.
- A model confidence score does not guarantee that a prediction is correct.
- RGB findings alone do not provide a complete assessment of plant physiology or environmental conditions.
- A prediction is not a definitive agricultural diagnosis.

## 14. Future Research Improvements

Potential improvements include:

- Expanding verified bell pepper RGB data for underrepresented classes.
- Improving representation of early or subtle symptoms.
- Evaluating model generalization on unseen greenhouse images.
- Comparing suitable classification architectures using reproducible experiments.
- Developing and validating affected-region segmentation where annotated masks are available.
- Improving severity assessment using independently labelled reference data.
- Evaluating follow-up observations across multiple time points.
- Assessing RGB output consistency when combined with thermal and environmental evidence.

## 15. Summary

The AI-Based RGB Bell Pepper Plant Stress Detection component investigates image-based identification of visible plant stress conditions in bell pepper cultivation.

Its research scope includes RGB image processing, classification, confidence reporting, severity assessment, and affected-region analysis where appropriate methods and evidence are available.

The proposed target classes are Healthy, Water Deficit, Nutrient Deficiency, Aphid, and Thrips. The actual classes supported by a trained model must be confirmed from its saved files and class mapping, particularly because the recorded model metadata does not list Water Deficit.

The component contributes visible plant-condition evidence to the broader multimodal research framework, supporting more informed greenhouse monitoring and adaptive recovery decision-making.
