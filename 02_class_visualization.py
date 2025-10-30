import json
from graphviz import Digraph
from torch import dot

def generate_class_hierarchy(class_map, output_file="class_hierarchy"):

    # create a Digraph with 'dot' engine
    dot = Digraph(comment="Class Hierarchy", engine="dot")
    
    # set layout direction to top-to-bottom and adjust spacing
    dot.attr(rankdir="TB", nodesep="1.0", ranksep="3.0")
    
    # track edges to avoid duplicates
    edges = set()
    
    for file, classes in class_map.items():
        for class_name, details in classes.items():

            # check if the class is a parent (has children)
            if any(class_name in child_details.get("parents", []) for _, child_details in class_map.items() for child_details in child_details.values()):
                # add the parent class as a node with a single color
                dot.node(
                    class_name,
                    f"{class_name}\nFile: {file}\nMethods: {len(details.get('methods', []))}\nAttributes: {len(details.get('attributes', []))}",
                    style="filled",
                    color="lightblue"
                )
            else:
                # add the child class as a node without color
                dot.node(
                    class_name,
                    f"{class_name}\nFile: {file}\nMethods: {len(details.get('methods', []))}\nAttributes: {len(details.get('attributes', []))}"
                )
            # add edges for parent classes
            for parent in details.get("parents", []):
                if (parent, class_name) not in edges:
                    dot.edge(parent, class_name)
                    edges.add((parent, class_name))
    
    # render the graph as an SVG
    dot.render(output_file, format="svg", cleanup=True)
    print(f"Class hierarchy diagram saved as {output_file}.svg")


with open("class_details5.json", "r", encoding="utf-8") as f:
    class_map = json.load(f)

generate_class_hierarchy(class_map)