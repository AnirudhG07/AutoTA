# AutoTA

AutoTA is a fun experiment assisting teaching assistants (TAs) in grading assignments and pointing out missinf and error statements using LLM's. It automate the grading process making more efficient and less time-consuming.

## Features

- Takes image file inputs(or directly text proofs) of Mathematics answer scripts and converts them to text with latex syntax for expressions.
- We create a structured proof of the answer script using our made `MathDoc.json` or `ProofShorter.json`.
- This contains the missing and error statements in the answer script with some marks awarded(which are based on clarity and correctness).
- A summary of all missing/error statements is provided at the end.

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

## Usage

## Notes

The project utilises the power of LLM's to convert math into OCR, generate structured proof along with comments. As the LLM's improve, the performance of this project will also improve. We have tested out with OpenAI and Gemini models, and results are reasonably great. The output may not be perfect, even at the OCR level since it's the LLM's job to understand the text and convert it to latex. We have tried our best to prompt, filter, reason about the outputs to make it as accurate as possible.

## Acknowledgements

This project was under Professor Siddhartha Gadgil, IISc Bengaluru.
