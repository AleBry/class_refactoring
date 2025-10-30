import json

with open("ophyd_classes_ai_clusters.json", "r") as f:
    clusters = json.load(f)

for idx, cluster in enumerate(clusters, 1):
    print(f"\nCluster {idx} ({len(cluster)} classes):")
    for cls in cluster:
        name = cls.get('class_name', 'UnknownClass')
        file = cls.get('file', 'UnknownFile')
        print(f"  - {name} ({file})")