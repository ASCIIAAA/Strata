import sys
sys.path.append('src')
from parser_logic import parse_project
from visualizer import generate_mermaid_sequence, generate_mermaid_chart
import os
import glob

def test_mermaid():
    java_files = glob.glob('mock_project/**/*.java', recursive=True)
    if not java_files:
        print("No mock files")
        return
        
    files_dict = {}
    for f in java_files:
        with open(f, 'r', encoding='utf-8') as file:
            files_dict[f] = file.read()
            
    relationships, _, _ = parse_project(files_dict)
    
    seq = generate_mermaid_sequence(relationships, max_lines=75)
    print("=== SEQUENCE ===")
    print(seq)
    
    chart = generate_mermaid_chart(relationships)
    print("=== CHART (first 500 chars) ===")
    print(chart[:500])

if __name__ == "__main__":
    test_mermaid()
