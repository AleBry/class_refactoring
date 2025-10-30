from graphviz import Digraph
import os
import json

def generate_class_hierarchy_by_parent(class_map, output_dir="class_hierarchy_by_parent"):
    os.makedirs(output_dir, exist_ok=True)  # crates output directory 
    
    parent_groups = {}
    for file, classes in class_map.items():
        for class_name, details in classes.items():
            for parent in details.get("parents", []):
                if parent not in parent_groups:
                    parent_groups[parent] = []
                parent_groups[parent].append((class_name, file))
    
    for parent, children in parent_groups.items():
        dot = Digraph(comment=f"Class Hierarchy for Parent {parent}", engine="dot")
        dot.attr(rankdir="TB", nodesep="1.0", ranksep="1.5")  # adjusts spacing, this default should be ok
        
        # Add the parent class as a node
        dot.node(parent, f"{parent}\n(Parent Class)", shape="box", style="filled", color="lightblue")
        
        edges = set()
        for child, file in children:
            # add child class as a node w/ file location, attributes, methods, etc
            dot.node(
                child,
                f"{child}\nFile: {file}\nMethods: {len(class_map[file][child].get('methods', []))}\nAttributes: {len(class_map[file][child].get('attributes', []))}",
                shape="ellipse"
            )
            if (parent, child) not in edges:
                dot.edge(parent, child)
                edges.add((parent, child))
        
        # Render the graph as an SVG
        sanitized_parent_name = parent.replace("/", "_").replace("\\", "_").replace(".", "_")
        output_file = os.path.join(output_dir, sanitized_parent_name)
        dot.render(output_file, format="svg", cleanup=True)
        print(f"Class hierarchy for parent {parent} saved as {output_file}.svg")

# example usage with class_details5.json, yes, no.5 b/c I forgot to change it but its the most up to data JSON file 
with open("class_details5.json", "r", encoding="utf-8") as f:
    class_map = json.load(f)

generate_class_hierarchy_by_parent(class_map)