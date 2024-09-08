# Review of Feedback

Starting from a basic prompt `ProofJsonShorter1.md` to `ProofJsonShorter4.md` with various changes regarding outputs of structured proof and the quality of missing and error statements highlighted by GPT-4o.

## Expectation

We would like to get feedback on each solution presented by student based on -

1. Errors present in the solution
2. Statements or Theorems missed
3. Maintain acceptable levels of rigour

## Pass 01

The data was collected for pass01 for this problem, so no particular arguments can be presented but a general idea similar to other problems can be assumed.

The first pass of the results did not show any form of acceptable feedback with hardly any `error` and `missing` field present in the output. The model was considering the assertions and reasoning by the student to be correct for most problem, even though the solutions were wrong.

The structured proofs had "direct computation" used as proof methods without actually showing the math, thus considering even the wrong solutions correct.

Moreover, the models were halucinating and writing solutions from theorem and bits and pieces of the OCR generated wrong proof to write their own correct proof for the solution. This required specifications in the instructions to prevent any such acts.

## Pass 02

For this pass, the below changes were made to `ProofJsonShorter1.md` to clearly explain the math and prevent the halucination to allow the model to catch any missing and errors in the proofs.

```
**Calculation**: (optional) a JSON list of calculation steps, with each step either a JSON string (for an equality, inequality etc) or a JSON object with two fields, **step** (the step) and **justification** (the justification for the step).
```

This resulted in various solutions showing "errors" as someone would expect. However for this problem unlike others, we did not find "missing" fields in the output. We could only find this feedback for only a few problems. For example:

```
"error": "The proof incorrectly claims that the gradient is zero at (2/3, 0). The correct points are (1,0) and (-1,0)."
```

Human checking showed multiple errors unlike the generates ones, thus a more thorough feedback was much needed.
Morever, a common observation states all the `missing` or `error` fields to be at the end of the proof, thus not providing any feedback on steps in between thus leading to unclear feedback interpretations.

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

The proofs currently highlight the `missing` and `error` for each step wherever it is needed. The proofs are not marked incorrect, incomplete, etc. based on the final outcome and feedback. This time more error and missing field were generated, which shows a better feedback was generated in comparison to previous pass. For example -

```
# 14431_sol
"errors": [
      {
        "type": "remark",
        "statement": "The proof derives the condition for the gradient to be zero, but it does not directly prove that the gradient is actually zero at those points."
      }
```

```
# 14431_sol_gpt
"errors": [
      "The formulation of some of the steps appears incomplete or incorrect. For instance, steps are repetitive and the final conclusion step is not fully justified.",
      "The proof does not explicitly calculate the gradient components before setting them to zero."
    ]
```

```
# 14546_sol
{
    "type": "conclude",
    "statement": "$\\therefore \\nabla f = 0$ at $(1,0)$ & $(0,1)$",
    "errors": [
        {
        "type": "remark",
        "statement": "The conclusion is not justified since we only found a necessary condition for the gradient to be zero. Moreover, the point $(0,1)$ does not make the gradient zero even with the incorrect derivative, and the point $(-1,0)$ which does make the gradient zero is missed."
        }
        ]
    }
```

```
# 14546_sol_gpt

{
    "type": "conclude",
        "statement": "$\\nabla f$ is zero at $(1,0)$ and $(-1,0)$",
        "errors": [
        {
            "statement": "Misstatement in the problem: Incorrect function definition in step 2.",
            "detail": "Step 2 incorrectly defines $f(x, y)$ as $x^2 - 3xy + y^2$ instead of $x^3 - 3x + y^2$. Therefore, the gradient calculations and subsequent steps are incorrect."
        },
        {
            "statement": "Incorrect points: Erroneously concludes that $\\nabla f = 0$ at $(0,1)$ instead of $(-1,0)$",
            "detail": "The correct points where $\\nabla f = 0$ should be $(1,0)$ and $(-1,0)$"
        }
        ]
}
"missing": [
    {
        "type": "problem",
        "statement": "Correctly define the function f and recompute its gradient.",
        "solved": false
    }
  ]
```

```
# 14590_sol_gpt
{
    "type": "conclude",
    "statement": "$\\implies$ The points are $(1, 0)$, $(-1, 0)$",
    "error": "The proof incorrectly concludes that the gradient is zero at the points $(1,0)$ and $(-1,0)$ just because the partial derivatives are zero at those points. It needs to show that both partial derivatives are zero at those points *simultaneously*."
}
```

```
# 14679_sol
"error": "The proof incorrectly concludes that the gradient is zero only at (1, 0) and (-1, 0) by setting the gradient to zero and solving for x and y. This approach finds the critical points where the gradient is zero, but it doesn't prove that the gradient is zero only at those points."
```

```
# 14807_sol_gpt
"errors": [
    "The proof assumes without justification that $(1,0)$ and $(-1,0)$ are the only solutions. The conditions $3x^2 - 3 = 0$ and $2y = 0$ must be explicitly solved to show these are the only points where the gradient is zero."
],
"missing": [
{
    "type": "problem",
    "statement": "Solve $3x^2 - 3 = 0$ and $2y = 0$ to find all points where the gradient is zero.",
    "solved": false
}
]
```

Clearly we have now got a better and detailed feedback with thorough pointers to statements and calculations one would expect. We have various "errors" and "missing" fields generated for the proofs which were not present in the previous passes.
Some of the feedbacks are very impressive like as present in problem `14807_sol_gpt` regarding the mention of the given points being the only solution.
However, the solutions which are correct as well as correctly graded by professors are marked incomplete due to lack of theorem stating by the student. It is in a way, going "rigorous" such that no proof is marked "proved". Thus the level of rigorousness is very high despite the correct feedbacks.

```
# 14590_sol
{
    "type": "error",
    "statement": "The proof does not rigorously verify that these points result in a zero gradient."
}
```

```
# 14807_sol
"error": "The proof assumes the conclusion that the gradient is zero at the points, rather than independently deriving it."
```

Thus another pass is required to reduce the level of rigorousness to get a reasonable feedback.

## Pass 04

To obtain correct feedbacks, the `error` and `missing` should not ask for missing theorems that the student may be instructed to use freely in class, though not mentioned below. The below changes were done to get "less rigourous" results.

```
@@ -41,7 +43,7 @@
-    * **Errors**: (optional) a JSON list of errors in the proof.
+    * **Errors**: a list of errors in the proof. Report only actual errors, with missing steps reported in the **missing** field.

@@ -66,9 +68,10 @@
-    * **Error**: (optional) an error in the proof so that the conclusion is not justified.
+    * **Missing**: a JSON list of **problem** fields which are problems that need to be solved or results that need to be proved to complete the proof, if the status is "incomplete proof". Standard results/criteria may be omitted from the proof.
+    * **Errors**: (optional) an error in the proof so that the conclusion is not justified. Report only actual errors, with missing steps reported in the **missing** field.
```

Some errors fields obtained are same as obtained which is expected since they are critical errors made by students. The missing fields not involving the theorem statement requirements are also present thus confirming the changes made didn't reduce the quality of the feedbacks obtained.
The improvements are observable in case of "less rigourousness" i.e. the number of occurence has decreased, however there exist proofs where they are marked incomplete for the same reason. For example -

```
# 14590_sol_gpt
"errors": [
    {
      "type": "error",
      "statement": "The proof does not rigorously verify that these points result in a zero gradient."
    }
]
```

Now at this stage, where we have a good enough prompt to get a good feedback, we needed to go through a second pass for the proof to check if the missing field were based on theorems not stated but can be used by student. Thus `truly_missing` function was made which gave a check if the missing field was simply due to abovementioned reason.
