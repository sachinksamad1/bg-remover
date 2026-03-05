# ✦ BG Remover — AI Background Removal Web App

A serverless background removal web application powered by the **U²-Net** deep learning model. Upload any image and get a clean, transparent PNG in seconds.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Cloud Run](https://img.shields.io/badge/Google%20Cloud%20Run-Deploy-orange)

---

## Features

- 🖼️ **Drag & drop** or click to upload images
- 🤖 **AI-powered** background removal using U²-Net
- 👀 **Side-by-side preview** — original vs. processed
- ⬇️ **One-click download** of transparent PNG
- 🎨 **Premium dark UI** with glassmorphism design
- 🐳 **Dockerized** for portable deployment
- ☁️ **Cloud Run ready** — zero-maintenance serverless hosting

---

## System Architecture

```
User Browser
     │
     ▼
Flask Web Server (Gunicorn)
     │
     ▼
Background Removal Service
(rembg + U²-Net model)
     │
     ▼
Processed Image (Transparent PNG)
```

---

## Tech Stack

| Component        | Technology         |
|------------------|--------------------|
| Backend          | Python 3.10        |
| Web Framework    | Flask              |
| Image Processing | rembg              |
| Model            | U²-Net             |
| Image Handling   | Pillow             |
| WSGI Server      | Gunicorn           |
| Containerization | Docker             |
| Cloud Platform   | Google Cloud Run   |
| Registry         | Artifact Registry  |

---

## Project Structure

```
bg-remover/
├── app.py              # Flask application & routes
├── requirements.txt    # Python dependencies
├── Dockerfile          # Production container config
├── .gitignore          # Git ignore rules
├── models/
│   └── u2net.pth       # U²-Net model weights
├── templates/
│   └── index.html      # Frontend UI
└── static/
    └── styles.css      # Premium dark theme styles
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- Docker *(optional, for containerized deployment)*

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd bg-remover
```

### 2. Download the U²-Net Model

Download `u2net.pth` and place it in the `models/` directory:

```bash
mkdir -p models
# Download from https://github.com/danielgatis/rembg#models
# Place downloaded model in the models/ directory
```

### 3. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

### 4. Run Locally

```bash
python app.py
```

Open **http://localhost:8080** in your browser.

---

## Docker

### Build

```bash
docker build -t bg-remover .
```

### Run

```bash
docker run -p 8080:8080 bg-remover
```

Open **http://localhost:8080**.

---

## Deploy to Google Cloud Run

### 1. Set Your Project

```bash
gcloud config set project YOUR_PROJECT_ID
```

### 2. Build & Push to Artifact Registry

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/bg-remover
```

### 3. Deploy

```bash
gcloud run deploy bg-remover \
  --image gcr.io/YOUR_PROJECT_ID/bg-remover \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 120
```

Cloud Run will provide a public URL for your app.

---

## API Endpoints

| Method | Endpoint     | Description                        |
|--------|--------------|------------------------------------|
| GET    | `/`          | Serves the web UI                  |
| POST   | `/remove-bg` | Accepts image upload, returns PNG  |
| GET    | `/health`    | Health check (for Cloud Run)       |

### `POST /remove-bg`

**Request:** `multipart/form-data` with field `image`

**Response:** `image/png` (transparent background)

**Constraints:**
- Accepted formats: PNG, JPG, JPEG, WEBP, BMP
- Max file size: 16 MB

---

## How It Works

1. User uploads an image via the web interface
2. Flask receives the image and opens it with **Pillow**
3. The image is passed to `rembg.remove()`, which runs the **U²-Net** model
4. U²-Net generates a saliency map to detect foreground objects
5. The background is removed and a transparent PNG is returned
6. The user can preview and download the result

---

## License

This project is for educational and personal use. The U²-Net model is licensed under [Apache 2.0](https://github.com/xuebinqin/U-2-Net/blob/master/LICENSE).