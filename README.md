# Face Crop API

A simple FastAPI-based service to detect and crop the first face from an image URL.  
Runs inside a Docker container for easy deployment.

---

## Features

- Accepts an image URL via POST request
- Detects faces using `face_recognition` (dlib-based)
- Crops and returns the first detected face as a JPEG image
- Returns 404 if no face is detected

---

## Requirements

- Docker
- (Optional) Python 3.10+ if running locally without Docker

---

## Quick Start

### 1. Build the Docker image

```bash
docker build -t face-crop-api .
```

### 2. Run the container

docker run -p 8000:8000 face-crop-api

## API Usage

{
"image_url": "https://example.com/image.jpg"
}

## Interactive API Docs

Visit http://localhost:8000/docs in your browser to test the API interactively.
