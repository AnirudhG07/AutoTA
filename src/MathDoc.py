class MathDocTree:
    def __init__(self, name: str, text: str = ""):
        self.name = name
        self.desc = text
        self.children = []

    def create_child(self, name: str, text: str = ""):
        """Create a new child and add it to the children list."""
        child = MathDocTree(name, text)
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

        # Children are indented by 4 spaces * depth
        indent = "    " * depth
        # name is bolded
        line = f"{indent}- **{self.name}** {self.desc}" 
        lines = [line]

        for child in self.children:
            lines.extend(child._to_markdown(depth + 1))
        return lines

    def to_markdown(self):
        """Generate Markdown representation of the tree."""
        return "\n".join(self._to_markdown())

# Example usage:
if __name__ == "__main__":
    root = MathDocTree("Root", "Top level")
    child1 = root.create_child("Child 1", "Level 1")
    child2 = root.create_child("Child 2", "Level 1")
    grandchild1 = child1.create_child("Grandchild 1", "Level 2")
    grandchild2 = child1.create_child("Grandchild 2", "Level 2")
    great_grandchild = grandchild1.create_child("Great Grandchild", "Level 3")

    # Add grandchild2 as a child of child2
    child2.add_existing_child(grandchild2)

    mathdoc = root.to_markdown()

    with open("./MathDoc.md", "w") as f:
        f.write(mathdoc)
    # Get names of children of root
    print("Children of Root:", root.get_child_names())

    # Get names of children of Child 1
    print("Children of Child 1:", child1.get_child_names())
