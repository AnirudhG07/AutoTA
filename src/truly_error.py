import json
import xml.etree.ElementTree as ET
from os.path import join
from pathlib import Path

from berkeley_test import BERKELEY_DATA, extract_problem, extract_solution
from gpt_structured import gpt_response_gen

homedir = Path("..")

def extract_error_json(str_proof_path: str):
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
                    "error_level": error["error_level"]
                })
        elif "missing_proofs" in step[claim_key]:
            for miss in step[claim_key]["missing_proofs"]:
                missing.append({
                    "claim": claim,
                    "missing": miss["missing"],
                    "missing_level": miss["missing_level"]
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
        "errors": errors,
        "missing": missing
    }
    return result



def extract_error_xml(str_proof_path: str):
    tree = ET.parse(str_proof_path)
    root = tree.getroot()
    
    errors = []
    missing = []
    overall_score = root.find(".//overall_score")
    if overall_score is not None:
        overall_score = overall_score.text
    
    def extract_errors_from_step(step):
        claim = step.find("claim").text
        for error in step.findall(".//errors"):
            errors.append({
                "claim": claim,
                "error": error.find("error").text,
                "error_level": error.find("error_level").text if error.find("error_level") is not None else "N/A"
            })
        for miss in step.findall(".//missing_proofs"):
            missing.append({
                "claim": claim,
                "missing": miss.find("missing").text,
                "missing_level": miss.find("missing_level").text if miss.find("missing_level") is not None else "N/A"
            })
    
    for step in root.findall(".//proof/assert"):
        extract_errors_from_step(step)

    print(errors, missing)
    
    result = {
        "overall_score": overall_score,
        "errors": errors,
        "missing": missing
    }
    
    return result


def extract_everything(str_proof_path: str, prob_path: str, sol_path: str):
    def get_rubric():
        with open(join("prompts", "rubric.md"), "r") as f:
            rubric = f.read()
        return rubric

    # Extractor function
    if str_proof_path.endswith(".json"):
        extractor = extract_error_json
    else:
        extractor = extract_error_xml

    errors = extractor(str_proof_path)
    problem = extract_problem(prob_path)
    solution = extract_solution(prob_path, sol_path)
    rubric = get_rubric()

    return {
        "errors": errors,
        "rubric": rubric,
        "problem": problem,
        "solution": solution
    }

def check_errors(errors, rubric, solution: str, problem: str, format_type: str = "json"):
    pre_knowledge = "You can assume commonly known knowledge of the topic by the student if directly reason not stated."
    prompt = f"You are an expert mathematician. The following is a mathematical proof evaluated based on below rubric. ## RUBRIC\n{rubric}\n. Here are the list of errors/missing statemets produced reported for the solution. ## Problem Statement\n{problem} ##Solution:\n {solution}\n ##Review:\n{str(errors)}. {pre_knowledge} Your task is to check if the missing and error statements pointed out are valid or not. Produce a {format_type} document containing the `statement`, pointed out `error/missing` statement, boolean value for `is_valid` and compulsarily an `explanation` of the reported error for each error/missing statement seperately IF valid. If the error claims that a detail is omitted when it is normal to omit such details in the mathematical literature, then report `is_valid` as False."

    response = gpt_response_gen(prompt, model = "gpt-4o")
    return response


if __name__ == "__main__":

    prob = "linalg_1_1"
    sol_path = prob + ".md"
    prob_path = prob
    format = "xml"
    str_proof_path = join(BERKELEY_DATA, prob, f"correct_str_{prob}.{format.lower()}")

    elements = extract_everything(str_proof_path, prob_path, sol_path)
    # print(check_errors(**elements, format_type = format))
    # with open(join(BERKELEY_DATA, prob, f"truly_error_check.{format.lower()}"), "w") as f:
    #     json.dump(elements, f)
    #
