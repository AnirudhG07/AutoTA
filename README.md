# AutoTA

## Running the server

To run the AutoTA server locally, simple follow the below instructions:

1. Clone the repository and navigate to the server directory

```bash
git clone https://github.com/AnirudhG07/AutoTA.git
cd AutoTA
cd server # To navigate to the server directory
```

3. Rename `.env.example` to `.env` and fill in the details.

4. (Recommended) Create a virtual environment and activate it

```bash
python3 -m venv venv
source .venv/bin/activate
```

3. Install the required packages

```bash
pip install -r requirements.txt
```

4. Run the server

```bash
streamlit run autota_ui.py
```

You can now access the server at `http://localhost:8501`(or any other port if specified).
