import os
import ast
import json

ophyd_bases = {"Device", "EpicsSignal", "EpicsSignalRO", "Xspress3Detector", "Xspress3FileStore"}

def get_base_names(bases):
    names = []
    for base in bases:
        if isinstance(base, ast.Name):
            names.append(base.id)
        elif isinstance(base, ast.Attribute):
            names.append(base.attr)
        elif isinstance(base, ast.Subscript) and isinstance(base.value, ast.Name):
            names.append(base.value.id)
    return names

def extract_classes(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)
    results = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            bases = get_base_names(node.bases)
            if any(base in ophyd_bases for base in bases):
                src = ast.get_source_segment(open(filepath).read(), node)
                results.append({
                    "class_name": node.name,
                    "bases": bases,
                    "file": filepath,
                    "source": src
                })
    return results

def scan_repo(root_dir):
    all_classes = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                try:
                    classes = extract_classes(filepath)
                    all_classes.extend(classes)
                except Exception as e:
                    print(f"Error in {filepath}: {e}")
    return all_classes

if __name__ == "__main__":
    root = "profile-collections"  # has to profile-collection repo
    classes = scan_repo(root)
    with open("ophyd_classes.json", "w", encoding="utf-8") as f:
        json.dump(classes, f, indent=2)
    print(f"Extracted {len(classes)} ophyd classes.")
