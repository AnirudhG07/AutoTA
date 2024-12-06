import os

from flask import Flask, jsonify, render_template, request

# Import your existing functions
from gpt_structured import gen_structure_proof, solution_from_images

app = Flask(__name__)

# Ensure upload folder exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-images', methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return jsonify({"error": "No image files uploaded"}), 400
    
    uploaded_files = request.files.getlist('images')
    image_paths = []
    
    for file in uploaded_files:
        if file.filename == '':
            continue
        
        # Save the file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        image_paths.append(filepath)
    
    # Call your existing function to process images
    try:
        extracted_text = solution_from_images(image_paths)
        return jsonify({"extracted_text": extracted_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-structured-proof', methods=['POST'])
def generate_structured_proof():
    data = request.json
    theorem = data.get('theorem', '')
    proof = data.get('proof', '')
    
    if not theorem or not proof:
        return jsonify({"error": "Both theorem and proof are required"}), 400
    
    try:
        structured_proof = gen_structure_proof(theorem, proof)
        return jsonify({"structured_proof": structured_proof})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
