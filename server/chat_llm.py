import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

THIRD_PARTY_API_KEY = os.getenv("API_KEY")
THIRD_PARTY_API_URL = os.getenv("THIRD_PARTY_API_URL")


def call_model_api(message, model):
    # Create an OpenAI client with your deepinfra token and endpoint
    openai = OpenAI(
        api_key=THIRD_PARTY_API_KEY,
        base_url=THIRD_PARTY_API_URL,
    )

    chat_completion = openai.chat.completions.create(
        model=model,  ## MODEL NAME
        # more models at https://deepinfra.com/models/
        messages=message,
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return chat_completion.choices[0].message.content


@app.route("/chat", methods=["POST"])
def chat_completions():
    try:

        content_type = request.headers.get("Content-Type", "application/json")

        # Validate Content-Type
        if content_type != "application/json":
            return (
                jsonify({"error": "Invalid Content-Type. Use applications/json"}),
                400,
            )

        req_data = request.get_json()
        message = req_data["messages"]
        model = req_data["model"]

        model_response = call_model_api(message, model)

        return jsonify(model_response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
