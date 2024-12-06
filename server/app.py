import os

from flask import Flask, jsonify, render_template, request

from gpt_structured import solution_from_images  # Import the new function

app = Flask(__name__)

# Directory for temporarily storing uploaded images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_images():
    if 'images[]' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400

    files = request.files.getlist('images[]')
    file_paths = []

    try:
        # Save the uploaded images temporarily
        for file in files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            file_paths.append(file_path)

        # Process the images using solution_from_images
        try:
            proof = solution_from_images(file_paths)
            print(f"Generated Proof: {proof}")  # Debugging: Print the proof in the terminal
        except Exception as e:
            print(f"Error generating proof: {str(e)}")
            return jsonify({'error': f"Error generating proof: {str(e)}"}), 500
        finally:
            # Clean up the saved files
            for path in file_paths:
                if os.path.exists(path):
                    os.remove(path)

        # Return the generated proof as a JSON response
        return jsonify({'output': proof})

    except Exception as e:
        # Log any unexpected errors
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
