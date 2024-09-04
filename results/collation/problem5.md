# Review of Feedback

Starting from a basic prompt `ProofJsonShorter1.md` to `ProofJsonShorter4.md` with various changes regarding outputs of structured proof and the quality of missing and error statements highlighted by GPT-4o.

## Expectation

We would like to get feedback on each solution presented by student based on -

1. Errors present in the solution
2. Statements or Theorems missed
3. Maintain acceptable levels of rigour

## Pass 01

The first pass of the results did not show any form of acceptable feedback with hardly any `error` and `missing` field present in the output. The model was considering the assertions and reasoning by the student to be correct for most problem, even though the solutions were wrong.

Here is an example of one missing field.

```
# 14546_sol
{
    "type": "missing",
    "Statement": [
                    {
                    "type": "problem",
                    "Statement": "Use Lagrange multipliers or another optimization technique to find the points on the ellipsoid  \\( x^{2}+2 y^{2}+3 z^{2}=1 \\) that maximize \\( f(x,y,z) = x^2 + y^2 + z^2 \\).\"
                }
        ]
}
```

The structured proofs had "direct computation" used as proof methods without actually showing the math, thus considering even the wrong solutions correct.
For example,

```
# 14679_sol
{
    "type": "assert",
    "claim": "$∇f = (2x, 4y, 6z)$ and $∇g = (2x, 2y, 2z)$",
    "proof-method": "Direct computation of the gradients."
},
```

Moreover, the models were halucinating and writing solutions from theorem and bits and pieces of the OCR generated wrong proof to write their own correct proof for the solution. This required specifications in the instructions to prevent any such acts.

## Pass 02

For this pass, the below changes were made to `ProofJsonShorter1.md` to clearly explain the math and prevent the halucination to allow the model to catch any missing and errors in the proofs.

```
**Calculation**: (optional) a JSON list of calculation steps, with each step either a JSON string (for an equality, inequality etc) or a JSON object with two fields, **step** (the step) and **justification** (the justification for the step).
```

This resulted in various solutions having "mssing" fields in the output, however most were based on proof incompleteness due to missing theorems not stated by the student. For example

```
# 14546_sol
{
    "type": "missing",
        "Problem": [
        {
            "type": "problem",
            "Statement": "Find the maximum of the function $g(x,y) = \\frac{1}{3} + \\frac{2}{3}x^2 + \\frac{1}{3}y^2$.",
            "Solved": false
          }
        ]
}
```

```
# 14546_sol_json

{
    "type": "missing",
        "problems": [
        {
            "type": "problem",
            "statement": "Complete the proof by showing that these points indeed have the largest distance from the origin using the given assumptions."
        }
        ]
}
```

Note that the solutions of 14546 Serial number were actually wrong and badly written, thus it was easily detected in both the passes above. Thus missing fields were present for this student's unlike other student's solutions.

However, a common observation states all the `missing` or `error` fields to be at the end of the proof, thus not providing any feedback on steps in between thus leading to unclear feedback interpretations.

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

The proofs currently highlight the `missing` and `error` for each step wherever it is needed. The proofs are not makred incorrect, incomplete, etc. based on the final outcome and feedback. For example -

```
# 14431_sol
"Status": "incomplete proof",
"Missing": [
    {
      "type": "problem",
      "Statement": "Prove that the function $f = \\sqrt{x^2 + y^2 + z^2}$ subject to the constraint $x^2 + 2y^2 + 3z^2 = 1$ has a maximum.",
      "Solved": false
    },
    {
      "type": "problem",
      "Statement": "Show rigorously that finding points where $\\nabla f = 0$ gives all possible maxima and minima of $f$ subject to the constraint.",
      "Solved": false
    }
],
...
{
    "type": "conclude",
    "Statement": "Since $1 > 1/\\sqrt{2}$, the points $(1, 0, 0)$ and $(-1, 0, 0)$ have a larger distance from the origin than the point $(0, 1/\\sqrt{2}, 0)$ on the ellipsoid. Therefore, $(1, 0, 0)$ and $(-1, 0, 0)$ are the points on the ellipsoid farthest from the origin.",
    "Error": "This argument only shows that (1,0,0) and (-1,0,0) are local maxima. To show they are global maxima, we need to compare their distance to the distance of all other points on the ellipsoid, not just one specific point."
}
```

However, the solutions which are correct as well as correctly graded by professors are marked incomplete due to lack of theorem stating by the student. It is in a way, going "rigorous" such that no proof is marked "proved". Thus the level of rigorousness is very high despite the correct feedbacks.

```
{example}
```

## Pass 04

To obtain correct feedbacks, the `error` and `missing` should not ask for missing theorems that the student may be instructed to use freely in class, though not mentioned below.

```
@@ -41,7 +43,7 @@
-    * **Errors**: (optional) a JSON list of errors in the proof.
+    * **Errors**: a list of errors in the proof. Report only actual errors, with missing steps reported in the **missing** field.

@@ -66,9 +68,10 @@
-    * **Error**: (optional) an error in the proof so that the conclusion is not justified.
+    * **Missing**: a JSON list of **problem** fields which are problems that need to be solved or results that need to be proved to complete the proof, if the status is "incomplete proof". Standard results/criteria may be omitted from the proof.
+    * **Errors**: (optional) an error in the proof so that the conclusion is not justified. Report only actual errors, with missing steps reported in the **missing** field.
```

The above changes were done to get "less rigourous" results. The improvements are observable however the proofs are still marked incomplete for the same reason. For example -

```
{codes}
```

Now at this stage, where we have a good enough prompt to get a good feedback, we needed to go through a second pass for the proof to check if the missing field were based on theorems not stated but can be used by student. Thus `truly_missing` function was made which gave a check if the missing field was simply due to abovementioned reason.

```
{truly_missing_code}
```

Now the proofs were marked correctly and the feedback was acceptable. For example -

```
{codes}
```
