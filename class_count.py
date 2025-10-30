import json

def analyze_class_collection(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        class_map = json.load(f)
    
    total_classes = 0
    total_methods = 0
    total_attributes = 0
    files_with_classes = []
    
    print("Class count")
    print("=" * 50)
    
    for file, classes in class_map.items():
        class_count = len(classes)
        if class_count > 0:
            files_with_classes.append((file, class_count))
            total_classes += class_count
            
            # count methods and attributes
            file_methods = sum(len(details.get("methods", [])) for details in classes.values())
            file_attributes = sum(len(details.get("attributes", [])) for details in classes.values())
            
            total_methods += file_methods
            total_attributes += file_attributes
    
    print(f"Total files processed: {len(class_map)}")
    print(f"Files with classes: {len(files_with_classes)}")
    print(f"Total classes found: {total_classes}")
    print(f"Total methods found: {total_methods}")
    print(f"Total attributes found: {total_attributes}")
    print(f"Average classes per file: {total_classes / len(files_with_classes):.2f}")
    print(f"Average methods per class: {total_methods / total_classes:.2f}")
    print(f"Average attributes per class: {total_attributes / total_classes:.2f}")
    
    # show files with most classes
    print("\nFiles with most classes:")
    print("-" * 30)
    sorted_files = sorted(files_with_classes, key=lambda x: x[1], reverse=True)
    for file, count in sorted_files[:10]:  # Top 10
        print(f"{count:3d} classes: {file}")
    
    return total_classes

analyze_class_collection("class_details5.json")