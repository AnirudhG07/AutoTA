# Reviews of Data

Here is collated version of net reviews to be improved upon from below mention dataset.

> Dataset: UMA102 Finals 2023 Main
>
> Git Commits | Repo Name: 68afd8cb, d4214bd8, 14a9c27e | LeanAide

## Issues models need to improve upon

### Proof Model Improvements

1. **Obvious Proof Methods**:

- The model is considering "vice-versa" or symmetric solutions as incomplete. Here is a snippet from GPT generated proof:

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

- Another instance is where the model does not accept "counterexample" as a proof method. The model should be able to understand that a counterexample is a valid proof method(depending on the context).

**Possible Solution**: The model should be given `obvious proofs` methods as valid proof methods including above and more.

2. Do not write your own proofs when the student has not written anything, example of hallucination.

**Possible Solution**: We can introduce `end-of-source` to tell the model, evaluate the proof only till the `end-of-source` and do not generate any proof beyond that, only povide feedback.

3. **Well Structured Proof**: It has come to notice that for complicated proofs, the model is not able to generate a well-structured proof. It simply states the `statement` and its `type` without further details as expected for a unit json object.

4. **Descriptive Errors**: The model sometimes does not provide descriptive errors as to what is wrong. Here are some examples for the same:

```json
"errors": [
  "Depends on the previous incorrect assertions."
]
"errors": [
  "Conclusion relies on incorrect previous steps."
]
"errors": [
      {
        "type": "assert",
        "claim": "\\sum \\frac{(-1)^n (n+1)^{32}}{n!} converges absolutely"
      },
      {
        "type": "assert",
        "claim": "Absolute convergence implies conditional convergence"
      }
    ]

"errors": [
    "The proof does not correctly utilize the given conditions."
]
{
    "type": "assert",
    "claim": "\\{(\\int_0^1 (f(x))^n dx)^{1/n}\\}_{n \\in \\mathbb{N}} \\text{ is an increasing sequence}",
    "errors": [
        "Not proved"
    ]
},
"errors" : [
    "There are logical inconsistencies in the use of absolute values and inequalities."
]

```

**Possible Solution**: The model should be able to provide descriptive errors as to what is wrong with the proof, however in a controlled level.

5. **Missing Steps**: Some of the feedback can be fixed after second pass with `truly_missing`.

### OCR Model Improvements

1. When student marks equations with numbers or symbols, retain them in the proof since they are part of the proof.
2. If you wrongly detect a fraction at some point due to it being less clear, do not use the wrongly detected fraction for further steps ignoring that same fraction but well written. This makes the whole proof go wrong, instead of a typo in one step.

## Issues users needs to take care of

1. The pictures taken should not have cut/striked or similar text since the model is considering them as part of the proof.
2. Try not to have professor comments in the proof written, since the model might get clues as to what is wrong with the proof.

## Issues which possibly can't be resolved

- The model wrongly copies from markdown that `2<1` instead of `1<1` in below part of proof. These are rare instances and can't be permanently resolved.

## Overall results

- No problem was marked correct i.e. there is always some or the other `missing` or `errors` in the proof. However, many of the proofs can be marked correct after the second pass with `truly_missing`.

- When the proofs are actually correct, the model always finds something `missing`, but by observation these are mainly extra rigorous expectations of the model for justifying trivial steps or steps which can be assumed by the student(again resolved by `truly_missing`).

- Correct proofs sometimes have `errors` which are justifyable errors and not arbitrary, however they were overlooked by the professor.

- A couple of times it has been noticed that completely incorrect proofs were only given `missing` feedback and not `errors` feedback since there train of logic made sense(to the model) but assumptions taken and steps were incorrect.
