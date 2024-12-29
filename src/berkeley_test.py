from os.path import join
from pathlib import Path

from gpt_structured import gen_structure_proof

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

def test_correct_solution(prob):
    with open (join(BERKELEY_DATA, prob, f"{prob}.md"), "r") as f:
        p = f.read()

    prob_text = extract_problem(prob)
    sol_text = p.find("## Solution") + len("## Solution")

    str_proof = gen_structure_proof(prob_text, p[sol_text:])

    if not Path(join(BERKELEY_DATA, prob)).exists():
        Path(join(BERKELEY_DATA, prob)).mkdir()
    with open(join(BERKELEY_DATA, prob, f"correct_str_{prob}.json"), "w") as f:
        f.write(str_proof)
    return str_proof

def save_str_proof(prob, sol_path):
    prob_text = extract_problem(prob)
    sol_text = extract_solution(prob, sol_path)
    print(prob_text)
    print(sol_text)

    structured_proof = gen_structure_proof(prob_text, sol_text)

    with open(join(BERKELEY_DATA, prob, sol_path), "w") as f:
        f.write(structured_proof)

    return structured_proof

if __name__ == "__main__":
    prob = "linalg_2_2"
    sol_path = prob + ".md" # In case of correct solution, sol_num = prob, else sol_num = "wrong_sol_{number}.md"
    #save_str_proof(prob, sol_path)
    test_correct_solution(prob)
    print("Done")
