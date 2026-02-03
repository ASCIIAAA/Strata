import javalang

def analyze_java_file(file_path):
    with open(file_path, 'r') as f:
        tree = javalang.parse.parse(f.read())

    stats = {
        "classes": [],
        "methods": []
    }

    # Extract Class Names
    for path, node in tree.filter(javalang.tree.ClassDeclaration):
        stats["classes"].append(node.name)

    for path, node in tree.filter(javalang.tree.MethodDeclaration):
        stats["methods"].append(node.name)

    return stats

# Quick Test
if __name__ == "__main__":
    test_file = "data\sample.java" 
    try:
        results = analyze_java_file(test_file)
        print(f"Found Classes: {results['classes']}")
        print(f"Found Methods: {results['methods']}")
    except Exception as e:
        print(f"Error: {e}. Make sure you have a valid .java file in the data folder.")