import base64
import os
from os.path import join
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

homedir = Path("..")
data = join(homedir, "data")
results = join(homedir, "results")

ocr_rules = """
Follow the below rules while extracting text from the image:
1. Use `$` to enclose LaTeX formulas.
2. If equations are being referred with symbols or numbers, retain the symbols or numbers within the proof.
3. Do not use previously written fractions/expressions as references for upcoming steps for initial proof extraction. Interpret fractions/expressions at each step.
4. The generated proof will be used to CHECK the correctness of the original proof, so DO NOT make corrections, add unmentioned reasonings complete proofs, only clean up the language.
"""

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

client = OpenAI(
    api_key  = OPENAI_API_KEY,
)

def image_solution(image_path: str):
    image_path = encode_image(image_path)
    
    gpt_prompt = "Extract text with LaTeX from the given mathematics solution."

    response = client.chat.completions.create(
        model="gpt-4o",
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

    return response.choices[0].message.content

def gpt_text_gen(prompt:str, task:str = "", model:str ="gpt-4o"):

    messages = []
    if task != "":
        messages.append({"role": "system", "content": task})
    messages.append({
        "role": "user",
        "content": prompt,
    })

    response = client.chat.completions.create(
            model=model,
            messages=messages,
        )

    return str(response.choices[0].message)


def solution_from_images(image_paths):
    combined_text = ""
    for image_path in image_paths:
        response = image_solution(image_path)
        combined_text += str(response)

    task =f"Your task is to rewrite the extracted text as a clean mathematical proof with full sentences, conjuctions etc. \n {ocr_rules}"
    prompt = f"Proof is: {combined_text}"

    return gpt_text_gen(task, prompt)

def save_proof(path:str , text_proof:str, structured_proof, pid:str):
    with open(join(path, f"{pid}.md"), "w") as f:
        f.write(text_proof)
    with open(join(path, f"{pid}.json"), "w") as f:
        f.write(structured_proof)
    
proof_json = open(join(homedir, "src", "ProofJsonShorter.md")).read()

def structure_prompt(thm, pf):
    return f"{proof_json}\n---\n\n## Theorem: {thm}\n\n## Proof: {pf}\n"

def structure_prompt_with_knowns(thm, pf, knowns):
    return f"{proof_json}\n---\n\n## Theorem: {thm}\n\n## Proof: {pf}\n\n---\n\nThe following are known results that can be used without proof, even implicitly. DO NOT report the use of these results as errors or missing steps.\n\n## Known results: \n\n{knowns}\n"

def truly_missing(knowns, s):
    prompt = f"The following are known results that can be used without proof, even implicitly.  \n\n## Known results: \n\n{knowns}\n\n---\n\nThe following was reported as a missing step in a proof:\n {s}\n\nDoes this result follow from the above known results? Answer 'yes' or 'no'."
    return gpt_text_gen(prompt)

def gen_proof_from_dir(image_path):
    for problem_dir in os.listdir(image_path):
        previous_pid = ""
        for prob in os.listdir(join(image_path, problem_dir)):

            if prob == "theorem.md":
                thm = open(join(image_path, problem_dir, prob)).read()

            elif prob.endswith(".png"):
                cur_pid = prob.split(".")[0].split("_")[0]

                if previous_pid != cur_pid:
                    previous_pid = cur_pid
                    image_paths = [join(image_path, prob)]

                else:
                    previous_pid = cur_pid

            else:
                # Probably some other cache file or something
                pass
