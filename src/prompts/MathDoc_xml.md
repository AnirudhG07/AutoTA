- **AutoTA**: An evaluation of mathematical proof in a structured document with a predefined RUBRIC.
  - **rubric**: A rubric containing the criteria for scoring the proof for errors and missing proofs. The rubric is as follows:
    - **Score 1**: Minor Formal Errors.
      - **description**: Notation/terminology issues without affecting logic.
      - **Example**: Mislabeling variables, missing definitions, or minor imprecision.
    - **Score 2**: Incomplete Details.
      - **description**: Missing obvious steps or intermediate details.
      - **Example**: Skipping base cases, omitting domains, or straightforward simplifications.
    - **Score 3**: Logical Oversights.
      - **description**: Missing important considerations but proof is mostly valid.
      - **Example**: Ignoring edge cases, unproven minor lemmas, or weak case handling.
    - **Score 4**: Substantial Flaws.
      - **description**: Incorrect logic or invalid steps undermining the proof.
      - **Example**: Using wrong theorems, circular reasoning, or overlooking critical conditions.
    - **Score 5**: Critical Errors.
      - **description**: Flaws that fully invalidate the proof or its conclusion.
      - **Example**: Proving the wrong statement, misinterpreting the problem, or contradictory logic.
  - **math_document**: A structured math document in a custom XML format. Give a XML list, with each element of the list is a XML object with exactly one _key-value pair_, with the _key_ one of `let`, `some`, `assume`, `def`, `assert`, `theorem`, `problem`, `cases`, `induction`, `contradiction`, `calculate`, `conclude`, `remark`. The descriptions for the choices of _key_ and corresponding _value_ are as follows:
    - **let**: A statement introducing a new variable with given value, type and/or property. For saying that **some** value of the variable is as needed, use a 'some' statement. Give a XML object. The keys and corresponding values are as follows.
      - **variable**: The variable being defined (use `<anonymous>` if there is no name such as in `We have a group structure on S`) Give a XML string.
      - **value**: (OPTIONAL) The value of the variable being defined Give a XML string.
      - **kind**: (OPTIONAL) The type of the variable, such as `real number`, `function from S to T`, `element of G` etc. Give a XML string.
      - **properties**: (OPTIONAL) Specific properties of the variable beyond the type. Give a XML string.
    - **some**: A statement introducing a new variable and saying that **some** value of this variable is as required (i.e., an existence statement). This is possibly with given type and/or property. This corresponds to statements like 'for some integer `n` ...' or 'There exists an integer `n` ....'. Give a XML object. The keys and corresponding values are as follows.
      - **variable**: The variable being defined (use `<anonymous>` if there is no name such as in `We have a group structure on S`) Give a XML string.
      - **kind**: (OPTIONAL) The type of the variable, such as `real number`, `function from S to T`, `element of G` etc. Give a XML string.
      - **properties**: (OPTIONAL) Specific properties of the variable beyond the type. Give a XML string.
    - **assume**: A mathematical assumption being made. In case this is a variable or structure being introduced, use a 'let' statement. Give a XML string.
    - **def**: A mathematical term being defined. In case a definition is being used, use 'assert' or 'theorem' instead. Give a XML object. The keys and corresponding values are as follows.
      - **statement**: The mathematical definition. Give a XML string.
      - **term**: The term being defined. Give a XML string.
      - **name**: (OPTIONAL) The name of the theorem, lemma or claim. Give a XML string.
    - **assert**: A mathematical statement whose proof is a straightforward consequence of given and known results following some method. Give a XML object. The keys and corresponding values are as follows.
      - **claim**: The mathematical claim being asserted, NOT INCLUDING proofs, justifications or results used. The claim should be purely a logical statement which is the *consequence* obtained. Give a XML string.
      - **proof_method**: (OPTIONAL) The method used to prove the claim. This could be a direct proof, proof by contradiction, proof by induction, etc. this should be a single phrase or a fairly simple sentence; if a longer justification is needed break the step into smaller steps. If the method is deduction from a result, use the 'deduced_using' field. Give a XML string.
      - **deduced_from_results**: (OPTIONAL) A list of elements of type `deduced_from`. Each element of type `deduced_from` is as follows:.
        - **deduced_from**: A deduction of a mathematical result from assumptions or previously known results. Give a XML object. The keys and corresponding values are as follows.
          - **result_used**: An assumption or previously known results from which the deduction is made. If more than one result is used, list them in the 'deductions' field as separate `deduction` objects. If the result used needs justification, have a separate `assert` object earlier. Give a XML string.
          - **proved_earlier**: Whether the statement from which deduction has been proved earlier IN THIS DOCUMENT. Answer `true` or `false` (answer `false` if a result from the mathematical literature is being invoked). Give a XML boolean.
      - **calculate**: (OPTIONAL) An equation, inequality, short calculation etc. Give a XML object, with each element of the list is a XML object with exactly one _key-value pair_, with the _key_ one of `inline_calculation`, `calculation_sequence`.
        - **inline_calculation**: A simple calculation or computation written as a single line. Give a XML string.
        - **calculation_sequence**: A list of elements of type `calculation_step`. Each element of type `calculation_step` is as follows:.
          - **calculation_step**: A step, typically an equality or inequality, in a calculation or computation. Give a XML string.
      - **missing_proofs**: (OPTIONAL) A list of elements of type `missing`. Each element of type `missing` is as follows:.
        - **missing**: A  problem that need to be solved or results that need to be proved to complete the proof. Standard results/criteria may be omitted from the proof: include them in the 'deduced_from' field. Give a XML string.
        - **missing_level**: The severity of the missing statement in the proof, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
      - **errors**: (OPTIONAL) A list of elements of type `error`. Each element of type `error` is as follows:.
        - **error**: An error in a proof or calculation. Report only actual errors, with missing steps reported in the 'missing' field. Give a XML string.
        - **error_level**: The severity of the error, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
    - **theorem**: A mathematical theorem, with a list of hypotheses and a conclusion. Give a XML object. The keys and corresponding values are as follows.
      - **hypothesis**: a XML list of data and assumptions, i.e., **let** and **assume** statements. Give a XML list, with each element of the list is a XML object with exactly one _key-value pair_, with the _key_ one of `let`, `some`, `assume`.
      - **conclusion**: The conclusion of the theorem. Give a XML string.
      - **proved**: Whether the theorem has been proved, either here or earlier or by citing the literature. Give a XML boolean.
      - **overall_score**: The overall score (upto 1 decimal point) of the proof out of 10 based on the correctness of the proof. Give a XML number.
      - **name**: (OPTIONAL) The name of the theorem, lemma or claim. Give a XML string.
      - **proof**: (OPTIONAL) A proof of a lemma, theorem or claim, having the same structure as (the value for) a `math_document`. Give a XML list, with each element of the list is a XML object with exactly one _key-value pair_, with the _key_ one of `let`, `some`, `assume`, `def`, `assert`, `theorem`, `problem`, `cases`, `induction`, `contradiction`, `calculate`, `conclude`, `remark`.
      - **ref**: (OPTIONAL) A reference where the result has been previously proved. Give a XML string.
      - **cite**: (OPTIONAL) A citation of a result from the mathematical literature which gives the proof. Give a XML string.
      - **missing_proofs**: (OPTIONAL) A list of elements of type `missing`. Each element of type `missing` is as follows:.
        - **missing**: A  problem that need to be solved or results that need to be proved to complete the proof. Standard results/criteria may be omitted from the proof: include them in the 'deduced_from' field. Give a XML string.
        - **missing_level**: The severity of the missing statement in the proof, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
      - **errors**: (OPTIONAL) A list of elements of type `error`. Each element of type `error` is as follows:.
        - **error**: An error in a proof or calculation. Report only actual errors, with missing steps reported in the 'missing' field. Give a XML string.
        - **error_level**: The severity of the error, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
    - **problem**: A mathematical problem, with a statement and an answer. Give a XML object. The keys and corresponding values are as follows.
      - **statement**: The statement of the problem. Give a XML string.
      - **solved**: Whether the problem has been solved Give a XML boolean.
      - **answer**: (OPTIONAL) The answer to the problem. Give a XML string.
      - **proof**: (OPTIONAL) A proof of a lemma, theorem or claim, having the same structure as (the value for) a `math_document`. Give a XML list, with each element of the list is a XML object with exactly one _key-value pair_, with the _key_ one of `let`, `some`, `assume`, `def`, `assert`, `theorem`, `problem`, `cases`, `induction`, `contradiction`, `calculate`, `conclude`, `remark`.
      - **missing_proofs**: (OPTIONAL) A list of elements of type `missing`. Each element of type `missing` is as follows:.
        - **missing**: A  problem that need to be solved or results that need to be proved to complete the proof. Standard results/criteria may be omitted from the proof: include them in the 'deduced_from' field. Give a XML string.
        - **missing_level**: The severity of the missing statement in the proof, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
      - **errors**: (OPTIONAL) A list of elements of type `error`. Each element of type `error` is as follows:.
        - **error**: An error in a proof or calculation. Report only actual errors, with missing steps reported in the 'missing' field. Give a XML string.
        - **error_level**: The severity of the error, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
    - **cases**: A proof by cases or proof by induction, with a list of cases. Give a XML object. The keys and corresponding values are as follows.
      - **split_kind**: one of 'implication_direction' (for two sides of an 'iff' implication), 'match' (for pattern matching), 'condition' (if based on a condition being true or false) and 'groups' (for more complex cases)..
      - **on**: The variable or expression on which the cases are being done. Write 'implication direction' for an 'iff' statement. Give a XML string.
      - **proof_cases**: (OPTIONAL) A list of elements of type `case`. Each element of type `case` is as follows:.
        - **case**: A case in a proof by cases or proof by induction. Give a XML object. The keys and corresponding values are as follows.
          - **condition**: The case condition or pattern; for induction one of 'base' or 'induction-step'; for a side of an 'iff' statement write the claim being proved (i.e., the statement `P => Q` or `Q => P`). Give a XML string.
          - **proof**: (OPTIONAL) A proof of a lemma, theorem or claim, having the same structure as (the value for) a `math_document`. Give a XML list, with each element of the list is a XML object with exactly one _key-value pair_, with the _key_ one of `let`, `some`, `assume`, `def`, `assert`, `theorem`, `problem`, `cases`, `induction`, `contradiction`, `calculate`, `conclude`, `remark`.
          - **missing_proofs**: (OPTIONAL) A list of elements of type `missing`. Each element of type `missing` is as follows:.
            - **missing**: A  problem that need to be solved or results that need to be proved to complete the proof. Standard results/criteria may be omitted from the proof: include them in the 'deduced_from' field. Give a XML string.
            - **missing_level**: The severity of the missing statement in the proof, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
          - **errors**: (OPTIONAL) A list of elements of type `error`. Each element of type `error` is as follows:.
            - **error**: An error in a proof or calculation. Report only actual errors, with missing steps reported in the 'missing' field. Give a XML string.
            - **error_level**: The severity of the error, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
      - **exhaustiveness**: (OPTIONAL) Proof that the cases are exhaustive, similar to (the value for) 'math_document'. Give a XML list, with each element of the list is a XML object with exactly one _key-value pair_, with the _key_ one of `let`, `some`, `assume`, `def`, `assert`, `theorem`, `problem`, `cases`, `induction`, `contradiction`, `calculate`, `conclude`, `remark`.
      - **missing_proofs**: (OPTIONAL) A list of elements of type `missing`. Each element of type `missing` is as follows:.
        - **missing**: A  problem that need to be solved or results that need to be proved to complete the proof. Standard results/criteria may be omitted from the proof: include them in the 'deduced_from' field. Give a XML string.
        - **missing_level**: The severity of the missing statement in the proof, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
      - **errors**: (OPTIONAL) A list of elements of type `error`. Each element of type `error` is as follows:.
        - **error**: An error in a proof or calculation. Report only actual errors, with missing steps reported in the 'missing' field. Give a XML string.
        - **error_level**: The severity of the error, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
    - **induction**: The variable or expression on which induction is being done. Give a XML object. The keys and corresponding values are as follows.
      - **on**: The variable or expression on which induction is being done. Give a XML string.
      - **proof_cases**: (OPTIONAL) A list of elements of type `case`. Each element of type `case` is as follows:.
        - **case**: A case in a proof by cases or proof by induction. Give a XML object. The keys and corresponding values are as follows.
          - **condition**: The case condition or pattern; for induction one of 'base' or 'induction-step'; for a side of an 'iff' statement write the claim being proved (i.e., the statement `P => Q` or `Q => P`). Give a XML string.
          - **proof**: (OPTIONAL) A proof of a lemma, theorem or claim, having the same structure as (the value for) a `math_document`. Give a XML list, with each element of the list is a XML object with exactly one _key-value pair_, with the _key_ one of `let`, `some`, `assume`, `def`, `assert`, `theorem`, `problem`, `cases`, `induction`, `contradiction`, `calculate`, `conclude`, `remark`.
          - **missing_proofs**: (OPTIONAL) A list of elements of type `missing`. Each element of type `missing` is as follows:.
            - **missing**: A  problem that need to be solved or results that need to be proved to complete the proof. Standard results/criteria may be omitted from the proof: include them in the 'deduced_from' field. Give a XML string.
            - **missing_level**: The severity of the missing statement in the proof, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
          - **errors**: (OPTIONAL) A list of elements of type `error`. Each element of type `error` is as follows:.
            - **error**: An error in a proof or calculation. Report only actual errors, with missing steps reported in the 'missing' field. Give a XML string.
            - **error_level**: The severity of the error, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
    - **contradiction**: A proof by contradiction, with an assumption and a proof of the contradiction. Give a XML object. The keys and corresponding values are as follows.
      - **assumption**: The assumption being made for the contradiction. Give a XML string.
      - **proof**: The proof of the contradiction given the assumption. Give a XML list, with each element of the list is a XML object with exactly one _key-value pair_, with the _key_ one of `let`, `some`, `assume`, `def`, `assert`, `theorem`, `problem`, `cases`, `induction`, `contradiction`, `calculate`, `conclude`, `remark`.
      - **missing_proofs**: (OPTIONAL) A list of elements of type `missing`. Each element of type `missing` is as follows:.
        - **missing**: A  problem that need to be solved or results that need to be proved to complete the proof. Standard results/criteria may be omitted from the proof: include them in the 'deduced_from' field. Give a XML string.
        - **missing_level**: The severity of the missing statement in the proof, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
      - **errors**: (OPTIONAL) A list of elements of type `error`. Each element of type `error` is as follows:.
        - **error**: An error in a proof or calculation. Report only actual errors, with missing steps reported in the 'missing' field. Give a XML string.
        - **error_level**: The severity of the error, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
    - **calculate**: (OPTIONAL) An equation, inequality, short calculation etc. Give a XML object, with each element of the list is a XML object with exactly one _key-value pair_, with the _key_ one of `inline_calculation`, `calculation_sequence`.
      - **inline_calculation**: A simple calculation or computation written as a single line. Give a XML string.
      - **calculation_sequence**: A list of elements of type `calculation_step`. Each element of type `calculation_step` is as follows:.
        - **calculation_step**: A step, typically an equality or inequality, in a calculation or computation. Give a XML string.
    - **conclude**: conclude a claim obtained from the steps so far. this is typically the final statement of a proof giving the conclusion of the theorem. Give a XML object. The keys and corresponding values are as follows.
      - **claim**: The conclusion of the proof. Give a XML string.
      - **missing_proofs**: (OPTIONAL) A list of elements of type `missing`. Each element of type `missing` is as follows:.
        - **missing**: A  problem that need to be solved or results that need to be proved to complete the proof. Standard results/criteria may be omitted from the proof: include them in the 'deduced_from' field. Give a XML string.
        - **missing_level**: The severity of the missing statement in the proof, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
      - **errors**: (OPTIONAL) A list of elements of type `error`. Each element of type `error` is as follows:.
        - **error**: An error in a proof or calculation. Report only actual errors, with missing steps reported in the 'missing' field. Give a XML string.
        - **error_level**: The severity of the error, on a scale of 1 to 5, with 1 being the least severe and 5 being the most severe. Follow the RUBRIC mentioned previously. Give a XML number.
    - **remark**: A remark or comment that is NOT MATHEMATICAL, instead being for motivation, attention, sectioning etc. Give a XML string.