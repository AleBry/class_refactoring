import json
from difflib import SequenceMatcher

def compare_methods_and_attributes(class1, class2):
    def jaccard_similarity(set1, set2):
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union != 0 else 0

    method_similarity = jaccard_similarity(set(class1["methods"]), set(class2["methods"]))
    attribute_similarity = jaccard_similarity(set(class1["attributes"]), set(class2["attributes"]))

    return method_similarity, attribute_similarity

def analyze_parent_and_children(class_map, output_file="similarity_report.json", threshold=0.7):
    report = {}

    # group classes by parent
    parent_groups = {}
    for file, classes in class_map.items():
        for class_name, details in classes.items():
            for parent in details.get("parents", []):
                if parent not in parent_groups:
                    parent_groups[parent] = []
                parent_groups[parent].append((class_name, file, details))

    # analyze each parent and its children
    for parent, children in parent_groups.items():
        parent_report = []
        for i, (class1_name, file1, class1_details) in enumerate(children):
            for j, (class2_name, file2, class2_details) in enumerate(children):
                if i >= j:  # avoid duplicate comparisons
                    continue
                method_sim, attr_sim = compare_methods_and_attributes(class1_details, class2_details)
                if method_sim > threshold or attr_sim > threshold:
                    parent_report.append({
                        "class1": {"name": class1_name, "file": file1},
                        "class2": {"name": class2_name, "file": file2},
                        "method_similarity": method_sim,
                        "attribute_similarity": attr_sim
                    })
        if parent_report:
            report[parent] = parent_report

    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
    print(f"Similarity report saved to {output_file}")

# example usage with class_details5.json, yes, no.5 b/c I forgot to change it but its the most up to data JSON file 
with open("class_details5.json", "r", encoding="utf-8") as f:
    class_map = json.load(f)

analyze_parent_and_children(class_map)