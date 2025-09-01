# Image Classification & Captioning API

This project is a full-stack web application that classifies uploaded images into one of several categories and generates a descriptive caption using a large language model. It features a Python backend built with FastAPI and a simple, interactive frontend. The entire application is containerized with Docker for easy deployment and portability.



## ✨ Features

* **Image Upload**: Simple web interface to upload JPG or PNG images.
* **Multi-Class Classification**: Classifies images into one of six categories (buildings, forest, glacier, mountain, sea, street) using a pre-trained TensorFlow model.
* **AI-Powered Captioning**: Generates a human-like description for the uploaded image using the Google Gemini 1.5 Flash model.
* **Asynchronous API**: Built with FastAPI for high-performance, non-blocking request handling.
* **Containerized**: Fully containerized with Docker for a consistent and reproducible environment.

---

## 🛠️ Tech Stack

* **Backend**: Python, FastAPI, Uvicorn
* **Machine Learning**: TensorFlow (Keras), Google Generative AI (Gemini)
* **Frontend**: HTML, CSS, JavaScript (Fetch API)
* **Containerization**: Docker

---

## 📂 Project Structure

```
assignment/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── models/
│   └── transfer_model_best.h5
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── model/
│       ├── __init__.py
│       └── llm_image_caption.py
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

You can run this project either locally with a Python environment or as a Docker container.

### Prerequisites

* Python 3.9+
* Docker Desktop
* A Google Generative AI API Key

### 1. Local Setup

**a. Clone the repository:**
```bash
git clone <your-repository-url>
cd assignment
```

**b. Create and activate a virtual environment:**
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

**c. Install dependencies:**
```bash
pip install -r requirements.txt
```

**d. Set the environment variable:**
You must set your Google API key for the captioning feature to work.

```powershell
# In PowerShell
$env:GOOGLE_API_KEY = "your_api_key_here"

# In bash (macOS/Linux)
export GOOGLE_API_KEY="your_api_key_here"
```

**e. Run the application:**
```bash
python src/main.py
```
The application will be available at **`http://localhost:8000`**.

### 2. Docker Setup

**a. Build the Docker image:**
From the project's root directory (`assignment/`), run:
```bash
docker build -t image-classifier-app .
```

**b. Run the Docker container:**
This command runs the container, maps the port, and securely passes your API key as an environment variable.
```bash
docker run -p 8000:8000 -e "GOOGLE_API_KEY=your_api_key_here" image-classifier-app
```
The application will be available at **`http://localhost:8000`**.