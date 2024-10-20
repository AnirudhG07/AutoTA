import json
import os
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("API_KEY")

def model_chat(prompt: str, model: str):
    # Create an OpenAI client with your deepinfra token and endpoint
    openai = OpenAI(
        api_key=API_KEY,
        base_url="https://api.deepinfra.com/v1/openai",
    )

    chat_completion = openai.chat.completions.create(
        model=model,  ## MODEL NAME
        # more models at https://deepinfra.com/models/
        messages=[
            {
                "role": "system",
                "content": "TO BE ADDED.",
            },
            {
                "role": "user",
                "content": f"TO BE ADDED. {prompt} ",
            },
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    prompt = "someprompt"
    model = "meta-llama/Meta-Llama-3-70B-Instruct"
    print(model_chat(prompt, model))
