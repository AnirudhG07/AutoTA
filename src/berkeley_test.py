import json
from os.path import join
from pathlib import Path

import xmltodict

from gpt_structured import gen_structure_proof as gen_json
from gpt_structured_xml import gen_structure_proof as gen_xml

homedir = Path("..")

BERKELEY_DATA = join(homedir, "data/berkeley/berkeley_errorsIncluded/")
def extract_problem(prob):
    with open (join(BERKELEY_DATA, prob, f"{prob}.md"), "r") as f:
        p = f.read()

    start = p.find("## Problem") + len("## Problem")
    end = p.find("## Solution") - 1

    return p[start:end]

def extract_solution(prob, sol_path):
    # sol_path may be same as prob, for correct solution case
    with open (join(BERKELEY_DATA, prob, sol_path), "r") as f:
        sol = f.read()

    start = sol.find("## Solution") + len("## Solution")

    # For correct solution, except block will give end
    try:
        end = sol.find("## Problems with") - 1
    except Exception as _:
        end = -1

    return sol[start:end]

def test_correct_solution(prob, xml: bool = False):
    with open (join(BERKELEY_DATA, prob, f"{prob}.md"), "r") as f:
        p = f.read()

    gen_func = gen_xml if xml else gen_json

    prob_text = extract_problem(prob)
    sol_text = p.find("## Solution") + len("## Solution")

    str_proof = gen_func(prob_text, p[sol_text:])

    if not Path(join(BERKELEY_DATA, prob)).exists():
        Path(join(BERKELEY_DATA, prob)).mkdir()

    format_type = "xml" if xml else "json"
    with open(join(BERKELEY_DATA, prob, f"correct_str_{prob}.{format_type}"), "w") as f:
        f.write(str_proof)

    if xml:
        with open(join(BERKELEY_DATA, prob, f"correct_str_{prob}.json"), "w") as f:
            f.write(json.dumps(xmltodict.parse(str_proof), indent=2))
    return str_proof

def save_str_proof(prob, sol_path, xml: bool = False):
    prob_text = extract_problem(prob)
    sol_text = extract_solution(prob, sol_path)
    print(prob_text)
    print(sol_text)

    gen_func = gen_xml if xml else gen_json
    structured_proof = gen_func(prob_text, sol_text)

    with open(join(BERKELEY_DATA, prob, sol_path), "w") as f:
        f.write(structured_proof)

    return structured_proof

if __name__ == "__main__":
    prob = "linalg_1_1"
    sol_path = prob + ".md" # In case of correct solution, sol_num = prob, else sol_num = "wrong_sol_{number}.md"
    #save_str_proof(prob, sol_path)
    test_correct_solution(prob, xml=True)
    print("Done")
