import json

input_file = "ophyd_classes_ai_clusters.json"

def mermaid_for_cluster(cluster_index):
    with open(input_file, "r") as f:
        clusters = json.load(f)

    if not (0 <= cluster_index < len(clusters)):
        print(f"Cluster index {cluster_index} out of range (0 to {len(clusters)-1})")
        return

    cluster = clusters[cluster_index]
    lines = ["```mermaid", "classDiagram"]
    for cls in cluster:
        class_name = cls["class_name"]
        for base in cls.get("bases", []):
            lines.append(f"    {class_name} <|-- {base}")
    lines.append("```")

    mermaid_syntax = "\n".join(lines)
    output_file = f"cluster_{cluster_index+1}_mermaid.md"
    with open(output_file, "w") as f:
        f.write(mermaid_syntax)
    print(f"Mermaid diagram for Cluster {cluster_index + 1} saved to {output_file}")
    return mermaid_syntax

if __name__ == "__main__":
    cluster_num = int(input("Enter cluster number (1-based): ").strip())
    mermaid_for_cluster(cluster_num - 1)