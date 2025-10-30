import ast
import os
import json

def extract_class_details(file_path):
    print(f"Processing file: {file_path}") 
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
    except SyntaxError as e:
        print(f"Syntax error in file {file_path}: {e}")  
        return {}
    classes = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            attributes = set()
            for n in ast.walk(node):
                if isinstance(n, ast.Assign):

                    # class level attributes
                    for target in n.targets:
                        if isinstance(target, ast.Name):
                            attributes.add(target.id)
                elif isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Store):

                    # instance level attributes (Ex: self.attr = value)
                    if isinstance(n.value, ast.Name) and n.value.id == "self":
                        attributes.add(n.attr)
            properties = [
                n.name
                for n in node.body
                if isinstance(n, ast.FunctionDef) and any(
                    isinstance(d, ast.Name) and d.id == "property"
                    for d in n.decorator_list
                )
            ]
            # extract parent classes and remove duplicates
            parent_classes = list(set(base.id for base in node.bases if isinstance(base, ast.Name)))
            classes[node.name] = {
                "methods": methods,
                "attributes": list(attributes),
                "properties": properties,
                "parents": parent_classes,
            }
    return classes

def extract_classes_from_directory(directory):
    class_map = {}
    for root, _, files in os.walk(directory):
        print(f"Scanning directory: {root}")  
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(f"Found Python file: {file_path}")  
                class_details = extract_class_details(file_path)
                if class_details:
                    class_map[file_path] = class_details
    return class_map

# this was originlly inside a cloned dir w/ all profile collections
profile_collections_dir = "."


class_map = extract_classes_from_directory(profile_collections_dir)


output_file = "class_details.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(class_map, f, indent=4)

print(f"Class details saved to {output_file}")