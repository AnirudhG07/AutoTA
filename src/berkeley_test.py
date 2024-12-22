from os.path import join
from pathlib import Path

from gpt_structured import gen_structure_proof

homedir = Path("..")
berekeley_data = join(homedir, "data", "berkeley")

def extract_problem(prob):
    with open (join(berekeley_data, prob, f"{prob}.md"), "r") as f:
        p = f.read()

    start = p.find("## Problem") + len("## Problem")
    end = p.find("## Solution") - 1

    return p[start:end]

def extract_wrong_solution(prob, sol_num):
    with open (join(berekeley_data, prob, f"wrong_sol_{sol_num}.md"), "r") as f:
        sol = f.read()

    start = sol.find("## Incorrect Proof:") + len("## Incorrect Proof:")
    end = sol.find("## Problems with") - 1

    return sol[start:end]

def test_correct_solution(prob):
    with open (join(berekeley_data, prob, f"{prob}.md"), "r") as f:
        p = f.read()

    prob_text = extract_problem(prob)
    sol_text = p.find("## Solution") + len("## Solution")

    str_proof = gen_structure_proof(prob_text, p[sol_text:])
    print(str_proof)
    return

def save_str_proof(prob, sol_num):
    prob_text = extract_problem(prob)
    sol_text = extract_wrong_solution(prob, sol_num)
    print(prob_text)
    print(sol_text)

    structured_proof = gen_structure_proof(prob_text, sol_text)

    with open(join(berekeley_data, prob, f"wrong_sol_{sol_num}_str.json"), "w") as f:
        f.write(structured_proof)

    return structured_proof

if __name__ == "__main__":
    prob = "alg_1"
    sol_num = 1
    #save_str_proof(prob, sol_num)
    test_correct_solution(prob)
    print("Done")
