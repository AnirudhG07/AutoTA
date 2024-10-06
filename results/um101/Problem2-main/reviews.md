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
- `D`: Any other comments? (Leave empty if none)
```

> Noticable halucinations are the ones that are not present in the original proof and are not trivially derivable from the original proof.

## 22067 | Problem 2

- Yes
- No
- Yes

```json
      {
        "type": "assert",
        "claim": "$f(h) < \\delta$ when $|h| < \\delta$",
        "errors": [
          "Incorrect deduction from the previous statement"
        ]
      }
    ]
  },
  "missing": [
    {
      "type": "problem",
      "statement": "Justify why $\\lim_{h \\to 0} f(h)$ does not exist if $\\lim_{h \\to 0}|f(h)-f(-h)|=0$"
    }
```

## 22097 | Problem 2

- Yes
- Yes

Comments: There is no proof written by the student, yet we have some proof by the content. This is clear example of hallucination.
Suggestions: We should introduce `end_of_source` in the prompt, to tell model that this is the end of the proof and now do you think the proof is correct or not.

- No

<details><summary>Click to see the fully hallucinated proof</summary>

```json
{
        "type": "assert",
        "claim": "\\lim_{h \\rightarrow 0} f(-h) = L",
        "deduced_from": {
          "from_context": [
            "\\lim_{h \\rightarrow 0} f(h) = L"
          ]
        },
        "proof-method": "Since f is defined on (-1,1) and limits from both sides must equal for the limit to exist."
      },
      {
        "type": "assert",
        "claim": "\\lim_{h \\rightarrow 0} |f(h) - f(-h)| = |L - L| = 0",
        "deduced_from": {
          "from_context": [
            "\\lim_{h \\rightarrow 0} f(h) = L",
            "\\lim_{h \\rightarrow 0} f(-h) = L"
          ]
        },
        "proof-method": "Use the fact that both limits equal L."
      },
      {
        "type": "conclude",
        "statement": "\\lim_{h \\rightarrow 0} f(h) \\text{ does not exist}",
        "missing": [
          {
            "type": "problem",
            "statement": "Justify why the assumption \\lim_{h \\rightarrow 0} f(h) = L leads to a contradiction, considering that \\lim_{h \\rightarrow 0} |f(h) - f(-h)| = 0."
          }
        ]
      }
```

</details>

## 22120 | Problem 2

- No

Comments: The student had made a box and cut it, and new proof started below it. However the model read that boxed set of statements as a part of proof. Our proof pictures, should manually remove such issues.

- No
- Yes

```json
{
      "type": "assert",
      "claim": "2=|N+2-N| \\le |N+2-l + l-N| < 2",
      "errors": [
        "Incorrect inequality handling",
        "Validation of steps required"
      ]
    },
    {
      "type": "assert",
      "claim": "2<2, which is a contradiction"
    }
}
```

## 22172 | Problem 2

- Yes
- No
- No

Comments: The proof uses the triangle inequality correctly. Yet the model thinks that the student says its a "Misapplications" of the triangle inequality.

```json
            {
              "type": "assert",
              "claim": "$|(N+1) + L -L - (N - L)| \\leq 1$",
              "proof-method": "triangle inequality"
            },
            {
              "type": "assert",
              "claim": "$|N+1 + L|+|-L - N + L| < \\epsilon + \\epsilon$",
              "proof-method": "substitution"
            },

...

      {
        "type": "conclude",
        "statement": "$\\lim_{h \\rightarrow 0}f(h)$ does not exist.",
        "errors": [
          "Misapplication of the triangle inequality.",
          "Incorrect handling of the limit definition."
        ]
      }
```

Also, the model wrongly copies from markdown that `2<1` instead of `1<1` in below part of proof.

```json
{
  "type": "assert",
  "claim": "$2 < 1$",
  "proof-method": "simplification"
}
```

## 22183 | Problem 2

- Yes

Comments: The student had badly written the proof, thus model output contains vertical `...`.

- No
- Yes

```json
      {
        "type": "assert",
        "claim": "\\lim_{x \\to 0} f(1)-f(1) = 0 and \\lim_{h \\to 0} f(h) - \\lim_{h \\to 0} f(h) = 0",
        "errors": [
          "Irrelevant calculations unrelated to the theorem's conclusion."
        ]
      },
      {
        "type": "assert",
        "claim": "|f(h)-f(h)-0| < \\epsilon < \\epsilon'",
        "errors": [
          "Redundant and incorrect manipulation of terms."
        ]
      },
      {
        "type": "assert",
        "claim": "\\left|\\frac{|f(h)-0|}{\\delta/2} - \\frac{|f(h)-0|}{-\\delta/2}\\right| < \\delta",
        "errors": [
          "Incorrect and irrelevant calculation."
        ]
      }
    ]
  },
  "errors": [
    "The proof provided is incorrect and contains several logical and mathematical errors. The steps do not correctly follow from the given hypothesis to the conclusion."
  ]
```

## 22211 | Problem 2

- Yes
- No
- No

Comments: A counter example if enough to prove if a statement is wrong and you need not generalise for all examples as the model suggests.

```json
  "missing": [
    {
      "type": "problem",
      "statement": "Justify why the given function f satisfies the condition \\lim_{h \\to 0} |f(h) - f(-h)| = 0"
    }
  ],
  "errors": [
    {
      "type": "problem",
      "statement": "The proof uses an example function but does not generalize the result to all functions satisfying the hypothesis."
    }
```
