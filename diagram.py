from graphviz import Digraph

def create_workflow_diagram(steps):

    dot = Digraph()

    for i, step in enumerate(steps):
        dot.node(str(i), step)

    for i in range(len(steps) - 1):
        dot.edge(str(i), str(i + 1))

    return dot