import json
import os

import pyperclip
import streamlit as st
from PIL import Image
from streamlit_sortables import sort_items

from gpt_structured import gen_structure_proof, solution_from_images

# Streamlit App
st.title("Mathematical Proof Generator")

# Function to copy text to clipboard and show confirmation
def copy_to_clipboard(text):
    pyperclip.copy(text)
    st.success("Copied to clipboard!")

# Function to trigger file download
def download_file(file_content, file_name):
    st.download_button(label="Download File", data=file_content, file_name=file_name, mime="text/plain")

# Step 1: Upload images
st.header("Step 1: Upload Images for Proof")
uploaded_images = st.file_uploader("Upload multiple images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

image_paths, proof = [], ""
if uploaded_images:
    st.write("Images uploaded successfully. You can reorder them below:")
    
    # Create a temporary directory if it doesn't exist
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    # Save uploaded images to the temporary directory
    for uploaded_file in uploaded_images:
        img = Image.open(uploaded_file)
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        img.save(temp_path)
        image_paths.append(temp_path)

    # Allow reordering of images using drag-and-drop functionality
    reordered_images = sort_items(
        items=[os.path.basename(path) for path in image_paths],  # Display only filenames
        direction="vertical",
    )

    if st.button("Generate Image to Text"):
        with st.spinner("Processing reordered images..."):
            proof = solution_from_images([os.path.join(temp_dir, filename) for filename in reordered_images])
        st.subheader("Generated Proof:")
        proof_box = st.text_area("Proof", proof, height=200, key="proof_text")
        if st.button("Copy to Clipboard", key="copy_proof"):
            copy_to_clipboard(proof)
        download_file(proof, "proof.txt")

# Step 2: Upload theorem
st.header("Step 2: Upload Theorem (Markdown File)")
uploaded_theorem = st.file_uploader("Upload a markdown file for the theorem", type="md")

theorem = ""
if uploaded_theorem:
    theorem = uploaded_theorem.read().decode("utf-8")
    st.subheader("Theorem Content:")
    theorem_box = st.text_area("Theorem", theorem, height=200, key="theorem_text")
    if st.button("Copy to Clipboard", key="copy_theorem"):
        copy_to_clipboard(theorem)

# Step 3: Generate structured proof
if st.button("Generate Structured Proof"):
    if not image_paths or not uploaded_theorem:
        st.error("Please upload both images and a theorem file before generating the structured proof.")
    else:
        with st.spinner("Generating structured proof..."):
            structured_proof = gen_structure_proof(theorem, proof)
        st.subheader("Structured Proof Output (JSON):")
        structured_proof_json = json.loads(structured_proof)
        st.json(structured_proof_json, key="structured_proof_json")
        if st.button("Copy to Clipboard", key="copy_structured_proof"):
            copy_to_clipboard(json.dumps(structured_proof_json, indent=2))
        download_file(json.dumps(structured_proof_json, indent=2), "structured_proof.json")
