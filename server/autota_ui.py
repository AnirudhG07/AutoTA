import json
import os
import shlex
import sys
from pathlib import Path

import pyperclip
import requests
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from streamlit_sortables import sort_items

load_dotenv()

homedir = str(Path(__file__).resolve().parent.parent)
src_dir = os.path.join(homedir, "src")
sys.path.insert(0, str(src_dir))
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

if "api_host" not in st.session_state:
    st.session_state.api_host = "localhost"
if "api_port" not in st.session_state:
    st.session_state.api_port = "7654"
# Host Information Section
with st.expander("Host Information"):
    localhost_serv = st.checkbox(
        "Your backend server is running on localhost", value=True, help="Check this if you want to call the backend API running on localhost.",
    )

    if not localhost_serv:
        api_host = st.text_input(
            "Backend API Host:",
            value="10.134.13.102",
            help="Specify the hostname or IP address where the proof server is running. Default is localhost.",
        )
        st.session_state.api_host = api_host
    api_port = st.text_input(
        "API Port:",
        value="7654",
        help="Specify the port number where the proof server is running. Default is 7654.",
    )
    st.session_state.api_port = api_port

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
        api_key_placeholder = (
            f"{selected_provider['default_api_key'][:15]}{'*' * (len(selected_provider['default_api_key']) - 15)}"
            if selected_provider["default_api_key"]
            else ""
        )
        api_key = st.text_input(
            "API Key:",
            value=api_key_placeholder,
            type="password",
            help="Hover to see the key, edit if needed.",
        )

        # Model selection text boxes
        model_image_to_text = st.text_input(
            "Model for Image to Text:",
            value=selected_provider["default_model"],
            help="Specify the model for Image to Text. Check out list of OpenAI Models [↗](https://platform.openai.com/docs/models)",
        )
        model_json_generator = st.text_input(
            "Model for JSON Generator:",
            value=selected_provider["default_model"],
            help="Specify the model for JSON Generator. Check out list of OpenAI Models [↗](https://platform.openai.com/docs/models)",
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
    st.download_button(
        label="Download File", data=file_content, file_name=file_name, mime="text/plain"
    )


# Step 1: Upload images
st.header("Upload Images for Proof")
uploaded_images = st.file_uploader(
    "Upload multiple images", type=["png", "jpg", "jpeg"], accept_multiple_files=True
)

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
        items=[
            os.path.basename(path) for path in st.session_state.image_paths
        ],  # Display only filenames
        direction="vertical",
    )
    st.session_state.image_paths = [
        os.path.join(temp_dir, filename) for filename in reordered_images
    ]

    if st.button("Generate Image to Text"):
        with st.spinner("Processing reordered images..."):
            try:
                st.session_state.proof = solution_from_images(
                    st.session_state.image_paths
                )
            except Exception as e:
                st.warning(f"Failed to process images: {e}")

if st.session_state.proof:
    st.subheader("Generated Proof:")
    proof_box = st.text_area(
        "Proof", st.session_state.proof, height=200, key="proof_text"
    )
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Copy to Clipboard", key="copy_proof"):
            copy_to_clipboard(st.session_state.proof)
    with col2:
        download_file(st.session_state.proof, "proof.txt")

# Step 2: Upload theorem
st.header("Upload Theorem (Markdown File)")
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
    theorem_box = st.text_area(
        "Theorem", st.session_state.theorem, height=200, key="theorem_text"
    )
    if st.button("Copy to Clipboard", key="copy_theorem"):
        copy_to_clipboard(st.session_state.theorem)

# Step 3: Generate structured proof
if st.button("Generate Structured Proof"):
    if not st.session_state.image_paths or not st.session_state.theorem:
        st.warning(
            "Please upload both images and a theorem file before generating the structured proof."
        )
    else:
        with st.spinner("Generating structured proof..."):
            try:
                st.session_state.structured_proof = gen_structure_proof(
                    st.session_state.theorem, st.session_state.proof
                )
            except Exception as e:
                st.warning(f"Failed to generate structured proof: {e}")

if st.session_state.structured_proof:
    st.subheader("Structured Proof Output (JSON):")
    try:
        structured_proof_json = json.loads(st.session_state.structured_proof)
        json_str = json.dumps(structured_proof_json, indent=2)
        json_box = st.text_area(
            "Structured Proof JSON", json_str, height=300, key="structured_proof_text"
        )
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Copy to Clipboard", key="copy_structured_proof"):
                copy_to_clipboard(json_str)
        with col2:
            download_file(json_str, "structured_proof.json")
    except Exception as e:
        st.warning(f"Failed to display structured proof: {e}")


# Output the summary and missing errors properly.
# TODO:
if st.session_state.proof:
    st.subheader("Response Summary: TODO")

# Lean Checker Tasks
tasks = {
    "echo": {"input": {"data": "Json"}, "output": {"data": "Json"}},
    "translate_thm": {
        "input": {"text": "String"},
        "output": {"theorem": "String"},
        "parameters": {
            "greedy": "Bool (default: true)",
            "fallback": "Bool (default: true)",
        },
    },
    "translate_def": {
        "input": {"text": "String"},
        "output": {"definition": "String"},
        "parameters": {"fallback": "Bool (default: true)"},
    },
    "theorem_doc": {
        "input": {"name": "String", "command": "String"},
        "output": {"doc": "String"},
    },
    "def_doc": {
        "input": {"name": "String", "command": "String"},
        "output": {"doc": "String"},
    },
    "theorem_name": {"input": {"text": "String"}, "output": {"name": "String"}},
    "prove": {"input": {"theorem": "String"}, "output": {"proof": "String"}},
    "structured_json_proof": {
        "input": {"theorem": "String", "proof": "String"},
        "output": {"json_structured": "Json"},
    },
    "lean_from_json_structured": {
        "input": {"json_structured": "String"},
        "output": {
            "lean_code": "String",
            "declarations": "List String",
            "top_code": "String",
        },
    },
    "elaborate": {
        "input": {"lean_code": "String", "declarations": "List Name"},
        "output": {"logs": "List String", "sorries": "List Json"},
        "parameters": {
            "top_code": 'String (default: "")',
            "describe_sorries": "Bool (default: false)",
        },
    },
}


def parse_curl(curl_cmd):
    args = shlex.split(curl_cmd)
    out = {"method": "POST", "url_ip": "", "port": "", "headers": {}, "data": {}}
    i = 0
    while i < len(args):
        match args[i]:
            case "curl":
                i += 1
            case "-X":
                out["method"] = args[i + 1]
                i += 2
            case "-H":
                k, v = args[i + 1].split(":", 1)
                out["headers"][k.strip()] = v.strip()
                i += 2
            case "--data" | "-d":
                try:
                    out["data"] = json.loads(args[i + 1])
                except Exception:
                    out["data"] = args[i + 1]
                i += 2
            case x if x.startswith("http"):
                x = x.split("://", 1)[1].split(":", 1)
                out["url_ip"] = x[0]
                out["port"] = x[1]
                i += 1
            case _:
                i += 1
    return out

def button_clicked(button_arg):
    def protector():
        """This function does not allow value to become True until the button is clicked."""
        st.session_state[button_arg] = True
    return protector

st.header("Server Request: Sparrow")

# cURL Request Section
st.subheader("Paste cURL Request")
curl_input = st.text_area(
    "Paste your cURL request here:",
    height=150,
    placeholder="Paste cURL command starting with curl -X POST...",
)

## Initialize session state variables
for key in ["parsed_curl", "manual_selection", "curl_selection", "sel_inputs", "sel_params", "selected_tasks", "result"]:
    if key not in st.session_state:
        st.session_state[key] = None
for key in ["curl_botton", "request_button"]:
    if key not in st.session_state:
        st.session_state[key] = False
#
if st.button("Process cURL Request", on_click = button_clicked("curl_botton")) or st.session_state.curl_botton:
    try:
        # Extract JSON payload from curl
        st.session_state.parsed_curl = parsed_curl = parse_curl(curl_input)
        # Update session state with host and port if they exist in the curl
        if "url_ip" in parsed_curl and parsed_curl["url_ip"]:
            st.session_state.api_host = parsed_curl.get(
                "url_ip", st.session_state.get("api_host", "localhost")
            )
        if "port" in parsed_curl and parsed_curl["port"]:
            st.session_state.api_port = parsed_curl.get(
                "port", st.session_state.get("api_port", "7654")
            )

        st.success("cURL parsed successfully!")
        st.json(parsed_curl)
        # Update session states
        st.session_state.curl_selection = True
        st.session_state.selected_tasks = list(parsed_curl.get("data", {})["tasks"]) if "data" in parsed_curl else []
    except Exception as e:
        st.session_state.selected_tasks = []
        st.error(f"Error parsing curl: {e}")

if st.checkbox(
    "Fill request manually. This will ignore any cURL request pasted above.",
    value=False,
):
    st.session_state.manual_selection = True
    st.subheader("Step 1: Select Input Tasks")
    selected_inputs = st.multiselect("Select Input Tasks:", list(tasks.keys()))

    sel_inputs = {}
    sel_params = {}
    if st.button("Give Input"):
        for task in selected_inputs:
            sel_inputs[task] = {}
            for key, value in tasks[task].get("input", {}).items():
                sel_inputs[task][key] = st.text_input(
                    f"{task.capitalize()} - {key} ({value}):"
                )
            for param, param_type in tasks[task].get("parameters", {}).items():
                sel_params[param] = st.checkbox(f"{task} - {param} ({param_type})")

    st.subheader("Step 2: Select Processing Tasks")
    selected_tasks = [task for task in tasks.keys() if task not in selected_inputs]
    selected_tasks = st.multiselect("Select Processing Tasks:", selected_tasks)

    # update to session state
    st.session_state.selected_tasks = selected_tasks
    st.session_state.sel_inputs = sel_inputs
    st.session_state.sel_params = sel_params


# Submit Request Section. Common to Curl and Manual Selection
if st.button("Submit Request", on_click= button_clicked("request_button")) or st.session_state.request_button:
    if not st.session_state.curl_selection and not st.session_state.manual_selection:
        st.warning("Please either paste a cURL request or select tasks manually.")
        st.stop()
    if st.session_state.manual_selection: # Makes the request payload from manual selection
        request_payload = {"tasks": st.session_state.selected_tasks, **st.session_state.sel_inputs, **st.session_state.sel_params}
    else: # Makes the request payload from cURL
        request_payload = st.session_state.parsed_curl.get("data", {})
        print(f"Request Payload: {request_payload}")
        if not request_payload:
            st.warning(
                "No data found in the cURL request. Please check the cURL command."
            )
            st.stop()
    with st.spinner("Request sent. Please wait for a short while..."):
        response = requests.post(
            f"http://{st.session_state.api_host}:{st.session_state.api_port}", json=request_payload
        )

    if response.status_code == 200:
        # Get the result
        st.success("Response received successfully!")
        st.session_state.result = response.json()
        print(f"Selected Tasks: {st.session_state.selected_tasks}")
        print(f"Response: {st.session_state.result}")
  
        # Handle the output for each task
        for task in st.session_state.selected_tasks:
            st.subheader(task.capitalize() + " Output", divider =True)
            for key, value in tasks[task]["output"].items():
                if "json" in value.lower().split():
                    st.write(f"{key.capitalize()} ({value}):")
                    st.json(st.session_state.result.get(key, "No data available."))
                else:
                    st.write(f"{key.capitalize()} ({value}):")
                    st.code(
                        st.session_state.result.get(key, "No data available."), language="plaintext"
                    )
    else:
        st.error(f"Error: {response.status_code}, {response.text}")


if os.path.exists(temp_dir):
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)
