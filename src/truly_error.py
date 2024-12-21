import json
from os.path import join
from pathlib import Path

from berkeley_test import extract_problem, extract_solution
from gpt_structured import gpt_response_gen

homedir = Path("..")
berekeley_data = join(homedir, "data", "berkeley")

def extract_error(str_proof_path: str):
    with open(str_proof_path, 'r') as file:
        proof_data = json.load(file)
    
    errors = []
    missing = []
    overall_score = proof_data["math_document"][0]["theorem"]["overall_score"]
    
    def extract_errors_from_step(step, claim_key):
        claim = step[claim_key]["claim"]
        if "errors" in step[claim_key]:
            for error in step[claim_key]["errors"]:
                errors.append({
                    "claim": claim,
                    "error": error["error"],
                    "score_e": error["score_e"]
                })
        elif "missing_proofs" in step[claim_key]:
            for miss in step[claim_key]["missing_proofs"]:
                missing.append({
                    "claim": claim,
                    "missing": miss["missing"],
                    "score_m": miss["score_m"]
                })
        else:
            pass

    err_kets = ["assert", "theorem", "problem", "cases", "case", "conclude", "contradiction"]
    for step in proof_data["math_document"][0]["theorem"]["proof"]:
        for key in err_kets:
            if key in step:
                extract_errors_from_step(step, key)
    
    result = {
        "overall_score": overall_score,
        "errors": errors
    }
    
    return result

def extract_everything(str_proof_path: str, prob_path: str, sol_path: str):
    def get_rubric():
        with open(join("prompts", "rubric.md"), "r") as f:
            rubric = f.read()
        return rubric

    errors = extract_error(str_proof_path)
    problem = extract_problem(prob_path)
    solution = extract_solution(prob_path, sol_path)
    rubric = get_rubric()

    return {
        "errors": errors,
        "rubric": rubric,
        "problem": problem,
        "solution": solution
    }

def check_errors(errors, rubric, solution, problem):
    pre_knowledge = "You can assume commonly known knowledge of the topic by the student if directly reason not stated."
    prompt = f"You are an expert mathematician. The following is a mathematical proof evaluated based on below rubric. ## RUBRIC\n{rubric}\n. Here are the list of errors/missing statemets produced reported for the solution. ## Problem Statement\n{problem} ##Solution:\n {solution}\n ##Review:\n{str(errors)}. {pre_knowledge} Your task is to check if the missing and error statements pointed out are valid or not. Produce a JSON document containing the `statement`, pointed out `error/missing` statement, boolean value for `is_valid` and an `explanation` of the reported error for each error/missing statement seperately IF valid. If the error claims that a detail is omitted when it is normal to omit such details in the mathematical literature, then report `is_valid` as False."

    response = gpt_response_gen(prompt, model = "o1-mini")
    return response


if __name__ == "__main__":
    prob = "alg_1"
    sol_path = prob + ".md"
    prob_path = prob
    str_proof_path = join(berekeley_data, prob, "correct_str_alg_1.json")

    elements = extract_everything(str_proof_path, prob_path, sol_path)
    print(check_errors(**elements))

