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

        top, right, bottom, left = face_locations[0]
        face_image = image[top:bottom, left:right]

        # Encode cropped face to JPEG
        _, buffer = cv2.imencode(".jpg", face_image)
        return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
