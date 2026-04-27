import javalang

def find_parent_method(path):
    for node in reversed(path):
        if isinstance(node, javalang.tree.MethodDeclaration):
            return node.name
    return None

def parse_project(files_dict):
    """
    files_dict: dict of {filename: sourceCODE}
    returns:
      relationships: list of dicts reflecting call graph edges
      class_stats: metadata about classes including their method list, approx dependencies
      method_line_ranges: metadata about method line ranges for dead code cleanup
    """
    relationships = []
    class_stats = {}
    method_line_ranges = {}
    
    for filename, code in files_dict.items():
        try:
            tree = javalang.parse.parse(code)
        except Exception:
            continue
            
        lines = code.splitlines()
        current_class = None
        
        # We process method declarations first to build ranges roughly
        methods_in_file = []
        for path, node in tree.filter(javalang.tree.MethodDeclaration):
            methods_in_file.append(node)
            
        for path, node in tree:
            if isinstance(node, javalang.tree.ClassDeclaration):
                current_class = node.name
                if current_class not in class_stats:
                    class_stats[current_class] = {
                        "methods": [],
                        "deps": set(),
                        "file": filename,
                        "line_start": node.position.line if node.position else 1,
                        "line_end": len(lines)
                    }
            
            if isinstance(node, javalang.tree.MethodDeclaration) and current_class:
                class_stats[current_class]["methods"].append(node.name)
                start_line = node.position.line if node.position else 1
                
                # Approximate end line by next method's start line or class end
                end_line = len(lines)
                for m in methods_in_file:
                    m_start = m.position.line if m.position else 1
                    if m_start > start_line and m_start < end_line:
                        end_line = m_start - 1
                        
                key = f"{current_class}.{node.name}"
                method_line_ranges[key] = {
                    "file": filename,
                    "start": start_line,
                    "end": end_line
                }
                
            if isinstance(node, javalang.tree.MethodInvocation) and current_class:
                caller_method = find_parent_method(path)
                relationships.append({
                    "caller_class": current_class,
                    "caller_method": caller_method,
                    "target_method": node.member,
                    "qualifier": node.qualifier
                })
                # simple heuristic: if qualifier is capitalized, might be a class dep
                if node.qualifier and isinstance(node.qualifier, str) and node.qualifier[0].isupper(): 
                    class_stats[current_class]["deps"].add(node.qualifier)
                    
    # Format deps to list
    for c in class_stats:
        class_stats[c]["deps"] = list(class_stats[c]["deps"])
        
    return relationships, class_stats, method_line_ranges

# Backwards compatibility
def extract_relationships(file_content):
    rels, _, _ = parse_project({"default.java": file_content})
    return [{"caller": r["caller_class"], "target_method": r["target_method"], "qualifier": r["qualifier"]} for r in rels]