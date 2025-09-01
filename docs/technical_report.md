# Technical Report: Image Classification and Captioning Web App

**Author**: Aniket Nainwal
**Date**: September 1, 2025

## 1. Introduction

This document outlines the technical details of a full-stack web application designed to classify images and generate descriptive captions. The project leverages a deep learning model for image classification and a large language model (LLM) for captioning, served via a robust Python backend and accessed through a simple web interface. The entire application is containerized using Docker for portability and ease of deployment.

---

## 2. Project Architecture

The application follows a modern client-server architecture, consisting of three primary components:

* **Backend API**: A high-performance asynchronous API built with **FastAPI**. It handles image processing, model inference, and communication with the Google Generative AI service.
* **Frontend UI**: A clean, single-page user interface built with standard **HTML, CSS, and JavaScript**. It allows users to upload an image and displays the results without a page reload.
* **Containerization**: The entire application and its dependencies are packaged into a **Docker** container, ensuring a consistent and reproducible environment.



---

## 3. Backend Implementation

The backend is the core of the application, responsible for all the heavy lifting.

### 3.1. Framework and Server

* **Framework**: **FastAPI** was chosen for its high performance, asynchronous capabilities, and automatic interactive documentation.
* **Server**: The application is served by **Uvicorn**, an ASGI server compatible with FastAPI.

### 3.2. Machine Learning Models

Two models are used in this project:

1.  **Image Classification**: A pre-trained Convolutional Neural Network (CNN) model (`transfer_model_best.h5`), loaded using **TensorFlow/Keras**. It classifies an input image into one of six categories: buildings, forest, glacier, mountain, sea, or street.
2.  **Image Captioning**: Google's **Gemini 1.5 Flash** model, accessed via the `google-generativeai` library. It takes an image as input and generates a concise, human-readable description.

### 3.3. API Endpoints

The application exposes two main endpoints:

* **`GET /`**: This endpoint serves the static frontend files (`index.html`, `app.js`, `style.css`) using FastAPI's `StaticFiles` mounting feature.
* **`POST /predict`**: This is the primary inference endpoint.
    * **Input**: An image file (`UploadFile`) sent as `multipart/form-data`.
    * **Process**:
        1.  The image is read into an in-memory buffer to avoid file-locking issues.
        2.  The image is preprocessed (resized to 150x150) and fed into the Keras classification model.
        3.  A copy of the image is sent to the Gemini API for captioning.
        4.  Blocking I/O operations (model prediction and captioning) are run in a thread pool (`run_in_threadpool`) to keep the server responsive.
    * **Output**: A JSON object containing the classification and the caption.
        ```json
        {
          "prediction": "street",
          "description": "A bustling city street with cars and pedestrians."
        }
        ```

---

## 4. Frontend Implementation

The frontend is a single `index.html` file linked to `style.css` and `app.js`, providing a straightforward user experience.

* **Structure (`index.html`)**: Contains a file input and a button wrapped in a `<form>` element. Placeholders for status messages and results are included.
* **Styling (`style.css`)**: Provides a clean, centered layout with modern fonts and colors for a professional look.
* **Functionality (`app.js`)**:
    * Uses an event listener on the form's `submit` event to trigger the process.
    * Prevents the default form submission to avoid a page reload.
    * Uses the `fetch` API to send the image to the `/predict` backend endpoint with a `POST` request.
    * Dynamically updates the DOM to display status messages, the final prediction, and the description, or an error if one occurs.

---

## 5. Containerization with Docker

The application is containerized for portability and consistent deployment using a multi-stage `Dockerfile`.

* **Base Image**: `python:3.11-slim` is used for its small footprint.
* **Multi-Stage Build**:
    1.  A `builder` stage is used to install Python dependencies from `requirements.txt`. This keeps the final image clean of build tools and caches.
    2.  The final stage copies the installed packages from the builder, along with the `src`, `models`, and `frontend` directories.
* **Environment Variables**:
    * The `PYTHONPATH` is set to `/app` to ensure correct module imports.
    * The `GOOGLE_API_KEY` is passed in at runtime using the `docker run -e` flag to keep secrets out of the image.
* **Execution**: The container runs the application using the command `CMD ["python", "-m", "uvicorn", "src.api.main:app", ...]`, which is a robust way to start the server.

---

## 6. Conclusion

This project successfully integrates machine learning models into a full-stack web application. Key achievements include creating a non-blocking API, a responsive user interface, and a portable Docker container. Future improvements could include deploying the application to a cloud service, adding support for more image formats, or enhancing the user interface with image previews.