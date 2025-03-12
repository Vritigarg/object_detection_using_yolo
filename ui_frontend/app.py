from flask import Flask, render_template, request, redirect, url_for
import requests
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
AI_BACKEND_URL = "http://127.0.0.1:8000/detect"  # FastAPI AI Backend

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Send to FastAPI Backend for detection
        with open(filepath, "rb") as img_file:
            files = {"file": (filename, img_file, file.content_type)}
            response = requests.post(AI_BACKEND_URL, files=files)
            
            if response.status_code == 200:
                detection_results = response.json()
            else:
                detection_results = {"error": f"AI backend error: {response.status_code}"}
        
        # ✅ Pass `zip` explicitly to the template
        return render_template('result.html', image_url=filename, results=detection_results, zip=zip)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5000)
