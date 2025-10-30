import json
import csv

with open("ophyd_classes_ai_clusters.json", "r") as f:
    clusters = json.load(f)

with open("clusters_summary.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Cluster Number", "Class Name", "File Path"])
    for idx, cluster in enumerate(clusters, 1):
        for cls in cluster:
            name = cls.get('class_name', 'UnknownClass')
            file = cls.get('file', 'UnknownFile')
            writer.writerow([idx, name, file])
print("CSV summary saved as clusters_summary.csv")
