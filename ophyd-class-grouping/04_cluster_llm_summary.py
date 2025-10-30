import json
import openai

input_file = "ophyd_classes_ai_clusters.json"
sample_size = 3
model = "gpt-4o"  
api_key = "" # OpenAI API key here

client = openai.OpenAI(api_key=api_key)

def summarize_cluster(cluster_classes, cluster_idx):
    sample = cluster_classes[:sample_size]
    code_snippets = "\n\n".join(cls['source'] for cls in sample)
    prompt = (
        f"Summarize the following Python classes from the same cluster. "
        f"Describe their main purpose, commonalities, and any notable differences. "
        f"Suggest possible refactoring, improvements, or documentation ideas.\n\n{code_snippets}"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    summary = response.choices[0].message.content
    return summary

def main():
    with open(input_file, "r") as f:
        clusters = json.load(f)

    with open("cluster_summaries.md", "w") as md:
        md.write("# Cluster Summaries\n\n")
        for idx, cluster in enumerate(clusters, 1):
            print(f"Processing Cluster {idx} ({len(cluster)} classes)...")
            summary = summarize_cluster(cluster, idx)
            md.write(f"## Cluster {idx} ({len(cluster)} classes)\n")
            md.write(summary + "\n\n")
    print("Summaries saved to cluster_summaries.md")

if __name__ == "__main__":
    main()
