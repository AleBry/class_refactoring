import json

input_file = "ophyd_classes_ai_clusters.json"
output_file = "all_clusters_mermaid.md"

with open(input_file, "r") as f:
    clusters = json.load(f)

lines = ["```mermaid", "classDiagram"]

for cluster in clusters:
    for cls in cluster:
        class_name = cls["class_name"]
        for base in cls.get("bases", []):
            lines.append(f"    {class_name} <|-- {base}")

lines.append("```")

with open(output_file, "w") as f:
    f.write("\n".join(lines))

print(f"Saved Mermaid diagram for ALL clusters to {output_file}")