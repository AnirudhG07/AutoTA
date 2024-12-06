import os

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

from gpt_structured import solution_from_images  # Import your function

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Home Page
@app.route("/")
def index():
    return render_template("index.html")


# Upload Endpoint
@app.route("/upload", methods=["POST"])
def upload_images():
    uploaded_files = request.files.getlist("images[]")
    file_paths = []

    for file in uploaded_files:
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            file_paths.append(file_path)

    return jsonify({"message": "Files uploaded successfully", "files": file_paths})


# Generate Endpoint
@app.route("/generate", methods=["POST"])
def generate_text():
    data = request.json
    image_paths = data.get("files", [])
    if not image_paths:
        return jsonify({"error": "No images provided"}), 400

    result = solution_from_images(image_paths)
    return jsonify({"output": result})


if __name__ == "__main__":
    app.run(debug=True)
