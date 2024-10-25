import base64
from os.path import join
from pathlib import Path

from openai import OpenAI

from .queries import ChatClient

homedir = Path("..")
data = join(homedir, "data")
results = join(homedir, "results")

ocr_rules = """
Follow the below rules while extracting text from the image:
1. Use `$` to enclose LaTeX formulas.
2. If equations are being referred with symbols or numbers, retain the symbols or numbers within the proof.
3. Do not use previously written fractions/expressions as references for upcoming steps for initial proof extraction. Interpret fractions/expressions at each step.
4. The generated proof will be used to CHECK the correctness of the original proof, so DO NOT make corrections or complete proofs, only clean up the language.
"""

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
client = OpenAI()

def solution_from_image(image_path: str):
    
    gpt_prompt = f"Extract text with LaTeX from the given mathematics solution. Also, rewrite the extracted text as a clean mathematical proof with full sentences, conjuctions etc. {ocr_rules}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": gpt_prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":  f"data:image/jpeg;base64,{image_path}"
                        },
                    },
                ],
            }
        ],

    )

    return response.choices[0]

def solution_from_images(image_paths):
    combined_text = ""
    for image_path in image_paths:
        response = solution_from_image(image_path)
        combined_text += response.message.content[0].content[0].value

    return combined_text

    

proof_json = open(join(data, "ProofJsonShorter.md")).read()

def structure_prompt(thm, pf):
    return f"{proof_json}\n---\n\n## Theorem: {thm}\n\n## Proof: {pf}\n"

def structure_prompt_with_knowns(thm, pf, knowns):
    return f"{proof_json}\n---\n\n## Theorem: {thm}\n\n## Proof: {pf}\n\n---\n\nThe following are known results that can be used without proof, even implicitly. DO NOT report the use of these results as errors or missing steps.\n\n## Known results: \n\n{knowns}\n"


chat_client = ChatClient()

def truly_missing(knowns, s):
    prompt = f"The following are known results that can be used without proof, even implicitly.  \n\n## Known results: \n\n{knowns}\n\n---\n\nThe following was reported as a missing step in a proof:\n {s}\n\nDoes this result follow from the above known results? Answer 'yes' or 'no'."
    response = chat_client.math(prompt)
    return response[0]
