# Review of Feedback

Starting from a basic prompt `ProofJsonShorter1.md` to `ProofJsonShorter4.md` with various changes regarding outputs of structured proof and the quality of missing and error statements highlighted by GPT-4o.

## Expectation

We would like to get feedback on each solution presented by student based on -

1. Errors present in the solution
2. Statements or Theorems missed
3. Maintain acceptable levels of rigour

## Pass 01

The first pass of the results did not show any form of acceptable feedback with hardly any `error` and `missing` field present in the output. The model was considering the assertions and reasoning by the student to be correct for most problem, even though the solutions were wrong.

```json
{
    "type": "remark",
    "Statement": "Since \\(\\epsilon > 0\\) was arbitrary, we can choose \\(\\epsilon < \\frac{1}{2}\\). This means we have found \\((x,y)\\) such that \\( \\|(x, y) - (0, 0)\\| < \\delta \\) but \\(|f(x, y) - f(0, 0)| \\geq \\epsilon \\), contradicting our assumption that \\(f\\) is continuous at \\((0,0)\\)."
    },
    {
    "type": "conclude",
    "Statement": "Therefore, the function \\(f\\) is not continuous at \\((0, 0)\\)."
}
```

The structured proofs had "direct computation" used as proof methods without actually showing the math, thus considering even the wrong solutions correct.
For example,

```json
{
    "type": "assert",
    "Claim": "\\( \\|(x, y) - (0, 0)\\| = \\sqrt{\\left(\\frac{\\delta}{2}\\right)^2 + \\left(\\frac{\\delta}{2}\\right)^2} = \\frac{\\delta}{\\sqrt{2}} < \\delta \\)",
    "Proof-method": "direct computation"
    },
    {
    "type": "assert",
    "Claim": "\\( |f(x, y) - f(0, 0)| = \\left|\\frac{\\left(\\frac{\\delta}{2}\\right)\\left(\\frac{\\delta}{2}\\right)}{\\left(\\frac{\\delta}{2}\\right)^2 + \\left(\\frac{\\delta}{2}\\right)^2}\\right| = \\frac{1}{2} \\)",
    "Proof-method": "direct computation"
},
```

Moreover, the models were halucinating and writing solutions from theorem and bits and pieces of the OCR generated wrong proof to write their own correct proof for the solution. This required specifications in the instructions to prevent any such acts.

## Pass 02

For this pass, the below changes were made to `ProofJsonShorter1.md` to clearly explain the math and prevent the halucination to allow the model to catch any missing and errors in the proofs.

```markdown
**Calculation**: (optional) a JSON list of calculation steps, with each step either a JSON string (for an equality, inequality etc) or a JSON object with two fields, **step** (the step) and **justification** (the justification for the step).
```

This resulted in various solutions having "mssing" and some "error" fields in the output, however most were based on proof incompleteness due to missing theorems not stated by the student. For example,

```json
{
"type": "assert",
"claim": "\\( ||(x, y)|| < \\delta \\implies ||f(x) - f(0)|| < \\epsilon \\)",
"missing": [
    {
    "type": "problem",
    "statement": "Need to rigorously prove this implication, considering both cases of the definition of f(x)."
    }
]
},
```

However, a common observation states all the `missing` or `error` fields to be at the end of the proof, thus not providing any feedback on steps in between thus leading to unclear feedback interpretations. Also most proofs still were marked with status "proved" even though a detailed analysis could have been given.

## Pass 03

To resolve the abovementioned issue, the below changes were made to `ProofJsonShorter2.md` to increase the frequency of missing and error fields in the output. The proofs were now asked to be divided in various levels of completeness, thus segregating the proofs into cleaner final results.

```
+    * **Missing**: (optional) a JSON list of **problem** fields which are problems that need to be solved or results that need to be proved to complete the proof. Standard results/criteria may be omitted from the proof: include them in the **deduced_from** field.
+    * **Errors**: (optional) a JSON list of errors in the proof.

-    * **Status**: one of "stated", "recalled", "proved earlier", "proved", "proved later".
+    * **Status**: one of "stated", "recalled", "proved earlier", "proved", "proved later", "wrong statement", "wrong proof" and "incomplete proof".

+    * **Missing**: (optional) a JSON list of **problem** fields which are problems that need to be solved or results that need to be proved to complete the proof. Standard results/criteria may be omitted from the proof.
+    * **Errors**: (optional) a JSON list of errors in the proof.
```

The proofs for this problem mostly show the status to be "proved" however the same missing field was present as before, but with a more accurate position.

```json
{
    "type": "assert",
    "claim": "\\( ||(x, y)|| < \\delta \\implies ||f(x) - f(0)|| < \\epsilon \\)",
    "missing": [
      {
        "type": "problem",
        "statement": "Need to rigorously prove this implication, considering both cases of the definition of f(x)."
      }
    ]
},
```

## Pass 04

To obtain better feedbacks, the `error` and `missing` should not ask for missing theorems that the student may be instructed to use freely in class, though not mentioned below.

```
@@ -41,7 +43,7 @@
-    * **Errors**: (optional) a JSON list of errors in the proof.
+    * **Errors**: a list of errors in the proof. Report only actual errors, with missing steps reported in the **missing** field.

@@ -66,9 +68,10 @@
-    * **Error**: (optional) an error in the proof so that the conclusion is not justified.
+    * **Missing**: a JSON list of **problem** fields which are problems that need to be solved or results that need to be proved to complete the proof, if the status is "incomplete proof". Standard results/criteria may be omitted from the proof.
+    * **Errors**: (optional) an error in the proof so that the conclusion is not justified. Report only actual errors, with missing steps reported in the **missing** field.
```

The above changes were done to get "less rigourous" results. Since for this problem being easier and small, the feedback was good enough in the previous pass, not much changes are observed.

Now at this stage, where we have a good enough prompt to get a good feedback, we needed to go through a second pass for the proof to check if the missing field were based on theorems not stated but can be used by student. Thus `truly_missing` function was made which gave a check if the missing field was simply due to abovementioned reason.

<!-- TODO: add truly_missing based hypo and more-->
