import json
import os
import sys
from pathlib import Path

import pyperclip
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from streamlit_sortables import sort_items

load_dotenv()

homedir = Path("..")
src_dir = os.path.join(homedir, "src")
sys.path.append(src_dir)
from gpt_structured import gen_structure_proof, solution_from_images

# Streamlit App
st.title("AutoTA")

provider_info = {
    "OPENAI": {
        "name": "OpenAI",
        "default_model": "gpt-4o",
        "default_api_key": os.getenv("OPENAI_API_KEY", ""),
    },
    "Gemini": {
        "name": "Gemini",
        "default_model": "gemini-1.5-pro",
        "default_api_key": os.getenv("GEMINI_API_KEY", ""),
    },
}

# API Credentials Section
with st.expander("Credentials"):
    # Provider selection
    provider = st.selectbox("Select Provider:", list(provider_info.keys()), index=0)

    # Dynamically update API Key and Model fields based on the provider
    selected_provider = provider_info[provider]

    if provider == "Gemini":
        # Warning if Gemini is selected
        st.warning("Gemini API is not yet supported. Please select OpenAI for now.")
    else:
        # API Key Input with masked display
        api_key_placeholder = f"{selected_provider['default_api_key'][:15]}{'*' * (len(selected_provider['default_api_key']) - 15)}" if selected_provider['default_api_key'] else ""
        api_key = st.text_input(
            "API Key:",
            value=api_key_placeholder,
            type="password",
            help="Hover to see the key, edit if needed."
        )

        # Model selection text boxes
        model_image_to_text = st.text_input(
            "Model for Image to Text:",
            value=selected_provider["default_model"],
            help="Specify the model for Image to Text. Check out list of OpenAI Models [↗](https://platform.openai.com/docs/models)"
        )
        model_json_generator = st.text_input(
            "Model for JSON Generator:",
            value=selected_provider["default_model"],
            help="Specify the model for JSON Generator. Check out list of OpenAI Models [↗](https://platform.openai.com/docs/models)"
        )
# Function to copy text to clipboard and show confirmation
def copy_to_clipboard(text):
    try:
        pyperclip.copy(text)
        st.toast("Copied to clipboard!", icon="✔️")
    except Exception as e:
        st.warning(f"Failed to copy: {e}")

# Function to trigger file download
# Create a temporary directory if it doesn't exist
temp_dir = "temp"
def download_file(file_content, file_name):
    st.download_button(label="Download File", data=file_content, file_name=file_name, mime="text/plain")

# Step 1: Upload images
st.header("Step 1: Upload Images for Proof")
uploaded_images = st.file_uploader("Upload multiple images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if "image_paths" not in st.session_state:
    st.session_state.image_paths = []
if "proof" not in st.session_state:
    st.session_state.proof = ""
if "structured_proof" not in st.session_state:
    st.session_state.structured_proof = ""

if uploaded_images:
    st.write("Images uploaded successfully. You can reorder them below:")
    
    os.makedirs(temp_dir, exist_ok=True)

    # Save uploaded images to the temporary directory
    for uploaded_file in uploaded_images:
        img = Image.open(uploaded_file)
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        img.save(temp_path)
        if temp_path not in st.session_state.image_paths:
            st.session_state.image_paths.append(temp_path)

    # Allow reordering of images using drag-and-drop functionality
    reordered_images = sort_items(
        items=[os.path.basename(path) for path in st.session_state.image_paths],  # Display only filenames
        direction="vertical",
    )
    st.session_state.image_paths = [
        os.path.join(temp_dir, filename) for filename in reordered_images
    ]

    if st.button("Generate Image to Text"):
        with st.spinner("Processing reordered images..."):
            try:
                st.session_state.proof = solution_from_images(st.session_state.image_paths)
            except Exception as e:
                st.warning(f"Failed to process images: {e}")

if st.session_state.proof:
    st.subheader("Generated Proof:")
    proof_box = st.text_area("Proof", st.session_state.proof, height=200, key="proof_text")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Copy to Clipboard", key="copy_proof"):
            copy_to_clipboard(st.session_state.proof)
    with col2:
        download_file(st.session_state.proof, "proof.txt")

# Step 2: Upload theorem
st.header("Step 2: Upload Theorem (Markdown File)")
uploaded_theorem = st.file_uploader("Upload a markdown file for the theorem", type="md")

if "theorem" not in st.session_state:
    st.session_state.theorem = ""

if uploaded_theorem:
    try:
        st.session_state.theorem = uploaded_theorem.read().decode("utf-8")
    except Exception as e:
        st.warning(f"Failed to read the theorem file: {e}")

if st.session_state.theorem:
    st.subheader("Theorem Content:")
    theorem_box = st.text_area("Theorem", st.session_state.theorem, height=200, key="theorem_text")
    if st.button("Copy to Clipboard", key="copy_theorem"):
        copy_to_clipboard(st.session_state.theorem)

# Step 3: Generate structured proof
if st.button("Generate Structured Proof"):
    if not st.session_state.image_paths or not st.session_state.theorem:
        st.warning("Please upload both images and a theorem file before generating the structured proof.")
    else:
        with st.spinner("Generating structured proof..."):
            try:
                st.session_state.structured_proof = gen_structure_proof(st.session_state.theorem, st.session_state.proof)
            except Exception as e:
                st.warning(f"Failed to generate structured proof: {e}")

if st.session_state.structured_proof:
    st.subheader("Structured Proof Output (JSON):")
    try:
        structured_proof_json = json.loads(st.session_state.structured_proof)
        json_str = json.dumps(structured_proof_json, indent=2)
        json_box = st.text_area("Structured Proof JSON", json_str, height=300, key="structured_proof_text")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Copy to Clipboard", key="copy_structured_proof"):
                copy_to_clipboard(json_str)
        with col2:
            download_file(json_str, "structured_proof.json")
    except Exception as e:
        st.warning(f"Failed to display structured proof: {e}")

# Delete temporary directory
if os.path.exists(temp_dir):
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)

# Footer
st.markdown("""
    <hr style="border: 0; border-top: 1px solid #ccc;" />
    <div style="text-align: center; color: #888; font-size: 0.9em;">
        Credits:
    </div>
""", unsafe_allow_html=True)
