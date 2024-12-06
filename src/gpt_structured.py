import base64
import json
import os
from itertools import groupby
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

PROOF_JSON_SHORTER_PROMPT = open(join(homedir, "src", "ProofJsonShorter.md")).read()
JSON_PROOF_INSTRUCTIONS = open(join(homedir, "src", "MathDoc.md")).read()

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

client = OpenAI(
    api_key  = OPENAI_API_KEY,
)

def image_solution(image_path: str, model: str = "gpt-4o"):
    image_path = encode_image(image_path)
    
    gpt_prompt = "Extract text with LaTeX from the given mathematics solution. GIVE ONLY THE PROOF within Latex code block."

    response = client.chat.completions.create(
        model=model,
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

def gpt_response_gen(prompt:str, task:str = "", model:str ="gpt-4o"):

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

    return response.choices[0].message.content


def solution_from_images(image_paths):
    combined_text = ""
    for image_path in image_paths:
        response = image_solution(image_path)
        combined_text += str(response)

    task =f"You are proficient in extracting Mathematical text from images. Your task is to rewrite the extracted text as a clean mathematical proof with full sentences, conjuctions etc. \n {ocr_rules}"
    prompt = f"Proof is: {combined_text}"

    return str(gpt_response_gen(task, prompt))

def save_proof(path:str , text_proof:str, structured_proof, pid:str, thm:str, model:str = "gpt-4o"):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(join(path, f"{pid}_sol.md"), "w") as f:
        f.write(f"## Theorem:\n {thm}\n\n## Proof:\n{text_proof}")

    with open(join(path, f"{pid}_gpt_sol.json"), "w") as f:
        f.write(structured_proof)
    
def structure_prompt_proofshorterjson(thm, pf):
    return f"{PROOF_JSON_SHORTER_PROMPT}\n---\n\n## Theorem: {thm}\n\n## Proof: {pf}\n"

def structure_prompt_mathdoc(thm, pf):
    alert = "Note that the proof may not be complete and may have some errors, which you should note in the appropriate fields."
    return f"The following is a custom JSON format, which we call `mathDocJSON`, for mathematical documents. Note that a document is translated to a JSON object with a single key 'math_document' and a corresponding value.\n\n {JSON_PROOF_INSTRUCTIONS}\n---\n\nWrite the following theorem and proof into `MathDocJSON` format. {alert} Output JSON only. The theorem and proof are as follows:\n\n## Theorem:\n {thm}\n\n## Proof:\n {pf}\n"

def gen_structure_proof(thm: str, pf: str):
    response = gpt_response_gen(structure_prompt_mathdoc(thm, pf))
    print(response)
    if response is None:
        return "No response from model while generating structured proof"
    response_cleaned = response.strip("```json").strip("```")
    
    return json.dumps(json.loads(response_cleaned), indent=2)

def structure_prompt_with_knowns(thm, pf, knowns):
    return f"{PROOF_JSON_SHORTER_PROMPT}\n---\n\n## Theorem: {thm}\n\n## Proof: {pf}\n\n---\n\nThe following are known results that can be used without proof, even implicitly. DO NOT report the use of these results as errors or missing steps.\n\n## Known results: \n\n{knowns}\n"

def truly_missing(knowns, s):
    prompt = f"The following are known results that can be used without proof, even implicitly.  \n\n## Known results: \n\n{knowns}\n\n---\n\nThe following was reported as a missing step in a proof:\n {s}\n\nDoes this result follow from the above known results? Answer 'yes' or 'no'."
    return gpt_response_gen(prompt)

def gen_proof_from_dir(image_path, model: str = "gpt-4o"):
    for problem_dir in os.listdir(image_path):  # problem_dir is Problem1_main

        files = os.listdir(join(image_path, problem_dir))
        grouped_files = {k: list(v) for k, v in groupby(sorted(files), key=lambda x: x.split("_")[0])}

        prob_thm = open(join(image_path, problem_dir, "theorem.md")).read()

        for st, pf_imgs in grouped_files.items():
            if st == "theorem.md":
                pass
            else:
                pf_imgs = [join(image_path, problem_dir, img) for img in pf_imgs]
                try:
                    text_proof = solution_from_images(pf_imgs)
                    print(text_proof)
                except Exception as e:
                    text_proof = ""
                    print("Error in extracting text from images", e)
                print("*************")

                try:
                    structured_proof = gen_structure_proof(prob_thm, text_proof)
                except Exception as e:
                    structured_proof = ""
                    print("Error in structuring proof", e)
                save_proof(join(results, "uma101_23_main", "selected_problems", problem_dir), text_proof, structured_proof, st, prob_thm, model)

    # Temporarily breaking the loop after the first problem
            break
        break
 
if __name__ == "__main__":
    model = "gpt-4o"
    image_path = join(data, "uma101_23_main", "selected_problems")
    gen_proof_from_dir(image_path, model)
