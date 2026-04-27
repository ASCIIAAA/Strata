def generate_mermaid_chart(relationships):
    # 'graph TD' means Top-Down
    mermaid_code = "graph TD\n"
    for rel in relationships:
        caller = rel['caller'] if rel['caller'] else "UnknownClass"
        target = rel['target_method']
        # Wrapping names in brackets [] or using quotes "" helps Mermaid render better
        mermaid_code += f'    {caller}["{caller}"] --> {target}["{target}"]\n'
    return mermaid_code