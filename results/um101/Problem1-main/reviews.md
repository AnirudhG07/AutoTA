# Reviews of Generations

This is style of reviews for the generated structured proofs pipeline. Please mention the Dataset Name and all Git Commit of Dataset Run(to keep track of updates).

Dataset: UMA102 Finals 2023 Main

Git Commits | Repo Name: 68afd8cb, d4214bd8, 14a9c27e | LeanAide

For each problem, the review contains the following information with Yes/No and any comments below it.

```markdown
## {Student ID} | Problem {ID}

- `A`: Is the Latex generation correct and clean?
- `B`: Does the structured proof generation contain noticable halucinations?
- `C`: Are the missing and error statements correctly identified?
```

> Noticable halucinations are the ones that are not present in the original proof and are not trivially derivable from the original proof.

## 22067 | Problem 1

- Yes
- No
- No

The model is considering "vice-versa" or symmetric solutions as incomplete. Here is a snippet from GPT generated proof:

```json
      {
        "type": "assert",
        "claim": "This argument can be repeated by switching $A$ and $B$.",
        "proof-method": "symmetry"
      },
      {
        "type": "conclude",
        "statement": "$\\sup (A \\cup B) = \\max \\{ \\sup A, \\sup B \\}$."
      }
    ]
  },
  "missing": [
    {
      "type": "problem",
      "statement": "Complete the proof that $\\max \\{ \\sup A, \\sup B \\}$ is the supremum of $A \\cup B$.",
      "solved": false
    }

```

## 22097 | Problem 1

- Yes
- No
- Yes

`Comments`: In the OCR, you should not have professor comments else they also get counted as part of the proof. However the model considered the proof wrong, as it should.

## 22120 | Problem 1

- Yes
- No
- No, some useless missing statements are there, however it should be taken care of in `truly_missing` pass.

```json
"missing": [
    {
      "type": "problem",
      "statement": "Prove that the union of two non-empty bounded sets is non-empty."
    }
```

## 22172 | Problem 1

- The picture contains boxes here there, so order is messed up.

Comments: The picture should not have small boxes at sides for any (\*) pointers. Have a clear order.

## 22183 | Problem 1

- Yes
- Yes

```json
      {
        "type": "assert",
        "claim": "$\\exists M_A \\in \\mathbb{R}$ such that $\\forall x \\in A$, $x \\leq M_A$",
        "proof-method": "A is bounded above"
      },
      {
        "type": "assert",
        "claim": "$\\exists M_B \\in \\mathbb{R}$ such that $\\forall x \\in B$, $x \\leq M_B$",
        "proof-method": "B is bounded above"
      },
```

The proof does not contain definition of M_a and M_b, yet the model is defining it.

- Yes

```json
  },
  "missing": [
    {
      "type": "problem",
      "statement": "Formal proof that $M = \\max \\{\\sup A, \\sup B\\}$ and $\\sup (A \\cup B) = M$"
    }
  ],
  "errors": [
    {
      "type": "error",
      "statement": "Missing formal justification for $\\sup (A \\cup B) = M$"
    }
  ]
```

## 22211 | Problem 1

- Yes

Comments: The model is not marking equation named as `(1)`, `(*)`, etc. and instead in the cleaned up proof. Thus, wherever the student has marked `- by (1)`, the model is writing the full `(1)` statement, which makes reading better, however redundant.

```markdown
## Student's Marking

Without loss of generality, let sup A ≥ sup B. <!-- This is (1) -->

## Model's Usage

Similarly, ∀y ∈ B, y ≤ sup(B) ≤ sup(A), as sup(B) is an upper bound of B and `sup B ≤ sup A`.

<!-- The highlighted is (1) by student-->
```

- No
- No

The model is not considering "exchange" argument presented by student. This is similar to symmetric proof for two cases where `A` and `B` can be exchanged.

```json
      {
        "type": "conclude",
        "statement": "$\\sup(A \\cup B) = \\max \\{\\sup A, \\sup B\\}$",
        "missing": [
          {
            "type": "problem",
            "statement": "Proper justification of the exchange argument."
          }
        ]
      }
    ]
  },
  "missing": [
    {
      "type": "problem",
      "statement": "Proof of $\\sup(A \\cup B) = \\sup B$ when $\\sup B \\ge \\sup A$"
    }
```
