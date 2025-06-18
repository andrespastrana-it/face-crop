from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import numpy as np
import face_recognition
import cv2
import io
from fastapi.responses import StreamingResponse

app = FastAPI()

class ImageRequest(BaseModel):
    image_url: str

@app.post("/crop-face")
async def crop_face(request: ImageRequest):
    try:
        # Download the image
        response = requests.get(request.image_url)
        image_np = np.frombuffer(response.content, np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        # Detect face
        face_locations = face_recognition.face_locations(image)
        if not face_locations:
            raise HTTPException(status_code=404, detail="No face found.")

        padding = 100  # adjust as needed

        top, right, bottom, left = face_locations[0]

        top = max(0, top - (padding + 150))
        right = min(image.shape[1], right + padding)
        bottom = min(image.shape[0], bottom + padding - 80)
        left = max(0, left - padding)

        face_image = image[top:bottom, left:right]

        # Encode cropped face to WebP
        success, buffer = cv2.imencode(".webp", face_image)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to encode image to WebP.")

        return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/webp")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
