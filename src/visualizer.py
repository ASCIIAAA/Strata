import re

def sanitize(name):
    safe = re.sub(r'[^a-zA-Z0-9_]', '_', str(name))
    return safe[:40] 

def sanitize_label(name):
    s = str(name).replace('"', "'").replace("<", "").replace(">", "").strip()
    return s[:40]

def generate_mermaid_chart(relationships):
    mermaid_code = "graph TD\n"
    added = set()
    for rel in relationships:
        caller = rel['caller_class'] if rel['caller_class'] else "UnknownClass"
        target_class = rel['qualifier'] if rel['qualifier'] else "UnknownClass"
        
        caller_safe = sanitize(caller)
        target_safe = sanitize(target_class)
        
        label_caller = sanitize_label(caller)
        label_target = sanitize_label(target_class)
        
        edge = f'{caller_safe}["{label_caller}"] --> {target_safe}["{label_target}"]\n'
        if edge not in added:
            mermaid_code += edge
            added.add(edge)
            
    return mermaid_code

def generate_mermaid_sequence(relationships, max_lines=75):
    mermaid_code = "sequenceDiagram\n"
    participants = set()
    messages = []
    
    count = 0
    for rel in relationships:
        if count >= max_lines:
            break
        caller = rel['caller_class'] if rel['caller_class'] else "Unknown"
        target_class = rel['qualifier'] if rel['qualifier'] else "Unknown"
        method = rel['target_method']
        
        caller_safe = sanitize(caller)
        target_safe = sanitize(target_class)
        method_safe = sanitize_label(method)
        
        # Only meaningful calls
        if caller_safe and target_safe and str(target_class)[0].isupper():
            participants.add(caller_safe)
            participants.add(target_safe)
            messages.append(f"    {caller_safe}->>{target_safe}: {method_safe}()")
            count += 1
            
    # explicitly define participants first
    for p in sorted(participants):
        mermaid_code += f"    participant {p}\n"
        
    for m in messages:
        mermaid_code += f"{m}\n"
                
    return mermaid_code