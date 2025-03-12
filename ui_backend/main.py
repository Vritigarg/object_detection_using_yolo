from fastapi import FastAPI, File, UploadFile
import requests

app = FastAPI()

AI_BACKEND_URL = "http://ai_backend:8000/detect"

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    files = {"file": (file.filename, await file.read(), file.content_type)}
    response = requests.post(AI_BACKEND_URL, files=files)
    
    # Save JSON response locally
    output_json_path = "output.json"
    with open(output_json_path, "w") as f:
        f.write(response.text)
    
    return response.json()
