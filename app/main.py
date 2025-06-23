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

        if image is None:
            raise HTTPException(status_code=400, detail="Failed to decode image.")

        # Detect face
        face_locations = face_recognition.face_locations(image)
        if not face_locations:
            raise HTTPException(status_code=404, detail="No face found.")

        # Get first face coordinates
        top, right, bottom, left = face_locations[0]

        # Calculate face center
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2

        # Define square box size with padding
        face_width = right - left
        face_height = bottom - top
        face_size = max(face_width, face_height)
        padding = int(face_size * 0.9)  # Add 60% padding

        half_size = (face_size + padding) // 2

        # Calculate square crop bounds
        crop_left = max(0, center_x - half_size)
        crop_top = max(0, center_y - half_size)
        crop_right = min(image.shape[1], center_x + half_size)
        crop_bottom = min(image.shape[0], center_y + half_size)

        # Ensure the crop is square
        crop_width = crop_right - crop_left
        crop_height = crop_bottom - crop_top
        square_size = min(crop_width, crop_height)

        # Recalculate crop box to be perfectly square
        crop_left = center_x - square_size // 2
        crop_top = center_y - square_size // 2
        crop_right = crop_left + square_size
        crop_bottom = crop_top + square_size

        # Clamp again to image bounds
        crop_left = max(0, crop_left)
        crop_top = max(0, crop_top)
        crop_right = min(image.shape[1], crop_right)
        crop_bottom = min(image.shape[0], crop_bottom)

        face_image = image[crop_top:crop_bottom, crop_left:crop_right]

        # Resize to 512x512
        resized_face = cv2.resize(face_image, (512, 512), interpolation=cv2.INTER_CUBIC)

        # Encode to WebP
        success, buffer = cv2.imencode(".webp", resized_face)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to encode image.")

        return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/webp")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
