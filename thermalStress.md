## AI-Based Thermal Bell Pepper Plant Stress Detection

 ## 1. Project Overview

This component is part of the research project **"Development of a Multimodal AI Framework for Early Bell Pepper Stress Detection and Adaptive Recovery in Greenhouse Environments."**

The purpose of this component is to analyze thermal images of bell pepper plants and classify their stress status using a Convolutional Neural Network (CNN). It also extracts image-based intensity features to provide additional supporting information for downstream analysis.

The component is designed to integrate with the overall multimodal framework, where thermal predictions can be combined with RGB image analysis and environmental data. The combined information can then be used by the Adaptive Recovery Decision Support System (DSS).

## 2. Objectives

- Classify thermal images into the four configured classes.
- Identify whether a plant is classified as healthy or stressed.
- Extract image-based intensity statistics as supporting features.
- Assess basic thermal image quality before inference.
- Provide predictions through a REST API.
- Supply thermal detection outputs to the wider multimodal framework.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| TensorFlow / Keras | CNN development and inference |
| EfficientNetB0 | Pretrained CNN backbone |
| OpenCV | Image processing and feature extraction |
| NumPy and Pandas | Numerical operations and data processing |
| Scikit-learn | Evaluation metrics and machine-learning utilities |
| FastAPI | REST API development |
| Uvicorn | Running the API server |
| Matplotlib | Visualization, including Grad-CAM outputs |

## 4. System Architecture

The component follows this general workflow:

1. Receive a thermal image.
2. Check image quality.
3. Preprocess the image into the required input format.
4. Pass the image through the trained CNN.
5. Generate the predicted class and associated confidence.
6. Calculate supporting image-based intensity features.
7. Apply the configured severity mapping and confound checks.
8. Return a structured JSON response through the API.
9. Pass the thermal evidence to the wider multimodal framework.

## 5. Project Structure

The main Python files and their responsibilities are listed below.

| File | Description |
|---|---|
| `config.py` | Stores model, training, preprocessing and threshold settings. |
| `data_pipeline.py` | Discovers images, prepares datasets, splits data and applies preprocessing and augmentation. |
| `model.py` | Defines the CNN architecture using transfer learning. |
| `train.py` | Trains the classification model and saves model artifacts. |
| `evaluate.py` | Evaluates classification performance and generates evaluation reports. |
| `feature_extraction.py` | Extracts pixel-intensity proxy features and supports the separate Track B classifier. |
| `gradcam.py` | Generates Grad-CAM visualizations to inspect image regions influencing CNN predictions. |
| `app.py` | Implements the FastAPI inference service. |

## 6. Model Development

The primary classification model uses transfer learning with an EfficientNetB0 backbone pretrained on ImageNet.

Training is performed in two stages:

1. **Classification head training:** The pretrained backbone is frozen while the newly added classification head is trained.
2. **Fine-tuning:** Selected later layers of the pretrained backbone are unfrozen and trained using a smaller learning rate.

The training process uses validation monitoring, early stopping and learning-rate reduction to help control overfitting.

The configured training settings include a batch size of 16, up to 15 head-training epochs and up to 30 fine-tuning epochs. The best saved model and associated metadata are used for inference.

## 7. Dataset and Preprocessing

The data pipeline discovers thermal images organized into class folders and prepares them for model development.

The preprocessing workflow includes:

- Loading thermal images.
- Resizing images to the configured dimensions of 240 × 320 pixels.
- Converting image data into the required numerical format.
- Normalizing pixel values.
- Splitting data into training, validation and test sets.
- Applying data augmentation during training.

The configured split proportions are 70% training, 15% validation and 15% testing.

Dataset quality, class balance, duplicate images and the independence of training and testing samples should be considered when interpreting evaluation results.

## 8. Model Evaluation

The evaluation module assesses classification performance using metrics such as:

- Accuracy
- Precision
- Recall
- Macro-F1 score
- Confusion matrix
- Expected Calibration Error (ECE)

Five-fold stratified cross-validation is also configured to examine performance across different data splits.

Grad-CAM visualizations provide an additional qualitative check of which image regions influence the model's predictions. These visualizations do not independently establish prediction correctness.

Evaluation reports are saved by the relevant scripts under the configured reports directory.

## 9. API Endpoints

The FastAPI application provides the following main endpoints.

### Health Check

**Endpoint:** `GET /health`

Checks whether the inference service is running and whether the required model artifacts have loaded.

### Thermal Image Prediction

**Endpoint:** `POST /predict`

Accepts a thermal image through the `thermal_image` upload field. An optional `plant_id` can be included.

The endpoint performs image-quality checks, preprocessing, CNN inference and supporting feature extraction.

The response includes fields such as:

- Predicted class
- Plant status
- Stress type, where applicable
- Prediction confidence
- Heuristic severity
- Pixel-intensity proxy statistics
- Possible environmental/background confound information

The exact response structure is defined by the implementation in `app.py`.

## 10. Installation and Setup

### Prerequisites

- Python version compatible with the project's installed dependencies.
- Visual Studio Code or another Python development environment.
- The required Python packages.
- The trained model artifacts and metadata required by the inference service.

### Install Dependencies

If the repository includes a `requirements.txt` file, create and activate a virtual environment, then install the dependencies.

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If no dependency file exists, install the packages specified by the project's actual imports and tested environment. The required package versions should be documented for reproducibility.

## 11. Training the Model

Ensure that the dataset is arranged in the directory structure expected by `data_pipeline.py` and that the paths in `config.py` are correct.

Run the training script from the project root:

```bash
python train.py
```

The script prepares the datasets, builds the model, performs the training stages and saves the trained model artifacts and metadata in the configured locations.

Check the training logs and generated files to confirm that training completed successfully.

## 12. Running the API

Ensure that the trained model and metadata files exist at the paths expected by `app.py`.

Start the FastAPI service using Uvicorn:

```bash
uvicorn app:app --reload
```

The API should start on the default local address and port used by Uvicorn unless otherwise configured.

Open the interactive API documentation at:

`http://127.0.0.1:8000/docs`

Use the documentation to inspect the endpoints and submit a thermal image for prediction.

## 13. Limitations

- The current intensity statistics are pixel-intensity proxies, not calibrated temperature measurements in degrees Celsius.
- Prediction confidence is not equivalent to the biological severity of plant stress.
- Thermal images alone may not reliably identify the underlying physiological cause of stress.
- Image quality and foreground-background checks are heuristic checks and require appropriate validation.
- Model performance depends on the quality, diversity and representativeness of the training dataset.
- Grad-CAM provides qualitative interpretation and does not prove that the model is correct.
- Real-world greenhouse use requires further validation under different environmental and imaging conditions.

## 14. Integration with the Multimodal Framework

This component provides thermal stress classification and supporting image-based evidence to the overall multimodal system.

Its outputs can be combined with RGB-based plant analysis and environmental information. The Adaptive Recovery DSS uses the integrated evidence and relevant agronomic knowledge to support recovery recommendations.

This component does not independently prescribe irrigation, fertilizer application or other recovery actions.

## 15. Research Context

This implementation is developed as the thermal stress detection component of a final-year undergraduate research project focused on multimodal AI for early bell pepper stress detection and adaptive recovery in greenhouse environments.

The component is intended to contribute thermal evidence to the wider framework while supporting model evaluation, explainability and integration with other AI components.
