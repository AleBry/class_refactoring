import json

with open('ophyd_classes.json', 'r') as f:
    classes = json.load(f)

print(f"Total number of classes: {len(classes)}")

# optional: show breakdown by base classes
from collections import Counter
base_counts = Counter()
for cls in classes:
    for base in cls['bases']:
        base_counts[base] += 1

print("\nBreakdown by base classes:")
for base, count in base_counts.most_common():
    print(f"  {base}: {count}")