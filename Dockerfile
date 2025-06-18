FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for dlib, OpenCV, face_recognition
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  cmake \
  libboost-all-dev \
  libopenblas-dev \
  liblapack-dev \
  libx11-dev \
  libgtk-3-dev \
  libdlib-dev \
  ffmpeg \
  libgl1-mesa-glx \
  && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
COPY app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy source code
COPY app .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
