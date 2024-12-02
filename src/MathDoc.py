class MathDocTree:
    def __init__(self,
                 name: str,
                 text: str = "",
                 child_list: list = [],
                 key_value_str: list = [],
                 optional: bool = False,
                 give_json: str = ""):
        """Initialise a node in the MathDocTree."""
        self.name = name
        self.desc = text
        self.children = []
        self.optional = optional
        self.give_json = give_json
        self.key_value_str = key_value_str
        for child in child_list:
            self.create_child(child)

    def create_child(self, name_or_node, text: str = ""):
        """Create a new child or assign an existing node as a child."""
        if isinstance(name_or_node, MathDocTree):
            # If the input is an existing node, add it as a child
            child = name_or_node
        else:
            # Otherwise, create a new node
            child = MathDocTree(name_or_node, text)
        self.children.append(child)
        return child

    def add_existing_child(self, existing_child):
        """Add an existing node as a child to this node."""
        self.children.append(existing_child)

    def get_child_names(self):
        """Return a list of names of all children of the current node."""
        return [child.name for child in self.children]


    def _to_markdown(self, depth=0):
        """Helper function to generate Markdown with proper indentation."""

        def key_value_pair_txt(keys: list) -> str:
            if keys == []:
                return ""
            return " with each element of the list is a JSON object with exactly one _key-value pair_, with the _key_ one of " + ", ".join([f"`{key}`" for key in keys])

        # Children are indented by 4 spaces * depth
        indent = "    " * depth
        optional_text = " (OPTIONAL)" if self.optional else ""
        give_json_text = f" Give a JSON {self.give_json}" if self.give_json else ""
        key_value_pair_str = key_value_pair_txt(self.key_value_str)
        punct = "," if key_value_pair_str != "" else "."
        # name is bolded
        line = f"{indent}- **{self.name}**:{optional_text} {self.desc}{give_json_text}{punct}{key_value_pair_str}"
        lines = [line]

        for child in self.children:
            lines.extend(child._to_markdown(depth + 1))
        return lines

    def to_markdown(self):
        """Generate Markdown representation of the tree."""
        return "\n".join(self._to_markdown())

def node_sequence_txt(node_name: str) -> str:
    return f"A list of elements of type `{node_name}`. Each element of type `{node_name}` is as follows:"

md_blobnames = ["let", "some", "assume", "def", "assert", "theorem", "problem", "cases", "induction", "contradiction", "calculate", "conclude", "remark"]

root_child = []

var = MathDocTree("variable", "The variable being defined (use `<anonymous>` if there is no name such as in `We have a group structure on S`)")
value = MathDocTree("value", "The value of the variable being defined")
kind = MathDocTree("kind", "The type of the variable, such as `real number`, `function from S to T`, `element of G` etc.")
properties = MathDocTree("properties", "Specific properties of the variable beyond the type.")

## Let 
let_children = [var, value, kind, properties]
let = MathDocTree("let", "A statement introducing a new variable with given value, type and/or property. For saying that **some** value of the variable is as needed, use a 'some' statement.", let_children)
root_child.append(let)

## Some
some = MathDocTree("some", "A statement introducing a new variable and saying that **some** value of this variable is as required (i.e., an existence statement). This is possibly with given type and/or property. This corresponds to statements like 'for some integer `n` ...' or 'There exists an integer `n` ....'.", [var, kind, properties])
root_child.append(some)

## Assume
assume = MathDocTree("assume", "A mathematical assumption being made. In case this is a variable or structure being introduced, use a 'let' statement.")
root_child.append(assume)

## Define
statement = MathDocTree("statement", "The mathematical definition.")
term = MathDocTree("term", "The term being defined.")
name_field = MathDocTree("name", "The name of the theorem, lemma or claim.", optional = True, give_json="string")

define = MathDocTree("def", "A mathematical term being defined. In case a definition is being used, use 'assert' or 'theorem' instead.", [statement, term, name_field])
root_child.append(define)

## Assert

claim = MathDocTree("claim", "The mathematical claim being asserted, NOT INCLUDING proofs, justifications or results used. The claim should be purely a logical statement which is the *consequence* obtained.")
proof_method = MathDocTree("proof_method", "The method used to prove the claim. This could be a direct proof, proof by contradiction, proof by induction, etc. this should be a single phrase or a fairly simple sentence; if a longer justification is needed break the step into smaller steps. If the method is deduction from a result, use the 'deduced_using' field")


instantiation = MathDocTree("instantiation", "Specific numbers, functions etc to which a known result is applied. For example, if we apply uniqueness of prime factorisation to `42` write `{'result_used' : 'uniqueness of prime factorization', 'instantiation': '42'}`.")

### Deduced Using

result_used = MathDocTree("result_used", "An assumption or previously known results from which the deduction is made. If more than one result is used, list them in the 'deductions' field as separate `deduction` objects. If the result used needs justification, have a separate `assert` object earlier.")
in_context = MathDocTree("proved_earlier", "Whether the statement from which deduction has been proved earlier IN THIS DOCUMENT. Answer `true` or `false` (answer `false` if a result from the mathematical literature is being invoked).")

deduced_from= MathDocTree("deduced_from", "A deduction of a mathematical result from assumptions or previously known results.", [result_used, in_context])

deduced_from_results = MathDocTree("deduced_from_results", node_sequence_txt("deduced_from"), [deduced_from])

### Calculate

inline = MathDocTree("inline_calculation", "A simple calculation or computation written as a single line.")
calculation_step = MathDocTree("step", "A step, typically an equality or inequality, in a calculation or computation.")
calculation_sequence = MathDocTree("calculation_sequence", node_sequence_txt("calculation_step"), [calculation_step]) 

calculate = MathDocTree("calculate", "An equation, inequality, short calculation etc. Give a JSON object with exactly one _key-value pair_, with the _key_ one of `inline_calculation`, `calculation_sequence`", [inline, calculation_sequence])

### Missing Proofs
missing = MathDocTree("missing", "A  problem that need to be solved or results that need to be proved to complete the proof. Standard results/criteria may be omitted from the proof: include them in the 'deduced_from' field.")
missing_proofs = MathDocTree("missing_proofs", node_sequence_txt("missing"), [missing])

### Errors
errors = MathDocTree("errors", "An error in a proof or calculation. Report only actual errors, with missing steps reported in the 'missing' field.")
error = MathDocTree("error", node_sequence_txt("error"), [errors])


assert_children = [claim, proof_method, deduced_from_results, calculate, missing_proofs, errors]

assert_type = MathDocTree("assert", "A mathematical statement whose proof is a straightforward consequence of given and known results following some method.", assert_children) 
root_child.append(assert_type)

## Theorem

hypothesis = MathDocTree("hypothesis", "a JSON list of data and assumptions, i.e., **let** and **assume** statements.", give_json = "list", key_value_str=["let", "some", "assume"])

conclusion = MathDocTree("conclusion", "The conclusion of the theorem.", give_json="string")
proved = MathDocTree("proved", "Whether the theorem has been proved, either here or earlier or by citing the literature.", give_json="boolean")

proof = MathDocTree("proof", "A proof of a lemma, theorem or claim, having the same structure as (the value for) a `math_document`.", give_json="list", key_value_str = md_blobnames) 
ref = MathDocTree("ref", "A reference where the result has been previously proved.", optional = True, give_json="string")
cite = MathDocTree("cite", "A citation of a result from the mathematical literature which gives the proof.", optional= True, give_json="string")

theorem = MathDocTree("theorem", "A mathematical theorem, with a list of hypotheses and a conclusion.", child_list = [statement, hypothesis, conclusion, proved, proof, ref, cite, missing_proofs, errors])
root_child.append(theorem)


## Root 
# Tree initialisation from root.
root = MathDocTree("math_document", "A structured math document in a custom JSON format.", child_list=root_child)


if __name__ == "__main__":
    # Converting the tree to markdown (Always at the bottom)
    mathdoc = root.to_markdown()

    with open("./MathDoc.md", "w") as f:
        f.write(mathdoc)
