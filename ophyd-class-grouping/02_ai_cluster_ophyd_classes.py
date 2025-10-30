import openai
import json
import numpy as np
import time

# config
openai_api_key = ""   # OpenAI API key here
embedding_model = "text-embedding-ada-002"
similarity_threshold = 0.85  # adjust for stricter/looser clustering
input_file = "ophyd_classes.json"
output_file = "ophyd_classes_ai_clusters.json"

openai.api_key = openai_api_key

def get_embedding(text, retry=3, sleep=1):
    for attempt in range(retry):
        try:
            response = openai.embeddings.create(
                input=text,
                model=embedding_model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Embedding error: {e}. Retrying...")
            time.sleep(sleep)
    return None

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))


with open(input_file, "r") as f:
    classes = json.load(f)

print(f"Getting embeddings for {len(classes)} classes...")
embeddings = []
for idx, cls in enumerate(classes):
    emb = get_embedding(cls['source'])
    embeddings.append(emb)
    print(f"Embedded class {idx+1}/{len(classes)}")

print("Comparing similarity and clustering...")
clusters = []
visited = set()
for i, emb_i in enumerate(embeddings):
    if emb_i is None or i in visited:
        continue
    cluster = [classes[i]]
    visited.add(i)
    for j, emb_j in enumerate(embeddings):
        if i == j or emb_j is None or j in visited:
            continue
        similarity = cosine_similarity(emb_i, emb_j)
        if similarity >= similarity_threshold:
            cluster.append(classes[j])
            visited.add(j)
    clusters.append(cluster)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(clusters, f, indent=2)

print(f"Clustered {len(classes)} classes into {len(clusters)} groups.")
print(f"See {output_file} for details.")
