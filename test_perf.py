import os
import time

from src.parser_logic import parse_project
from src.analyzer import build_code_graph, build_method_graph, find_god_objects, find_spaghetti_cycles, cluster_microservices, find_dead_code

def run_test():
    base_dir = "mock_project"
    files_dict = {}
    
    total_lines = 0
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".java"):
                path = os.path.join(root, f)
                with open(path, "r") as fp:
                    content = fp.read()
                    files_dict[f] = content
                    total_lines += len(content.splitlines())
                    
    print(f"Loaded {len(files_dict)} files with {total_lines} total lines.")
    print("Starting pipeline test...")
    start_time = time.time()
    
    print("Parsing...")
    rels, class_stats, lines_info = parse_project(files_dict)
    
    print("Building Graphs...")
    G_class = build_code_graph(rels)
    G_method = build_method_graph(rels)
    
    print("Finding God Objects...")
    god_objects = find_god_objects(G_class, class_stats)
    
    print("Finding Spaghetti Cycles...")
    spaghetti = find_spaghetti_cycles(G_class)
    
    print("Clustering microservices...")
    microservices = cluster_microservices(G_class)
    
    print("Finding Dead Code...")
    dead_code = find_dead_code(G_method, class_stats)
    
    end_time = time.time()
    
    print("-----------------------------------------")
    print(f"Done in {end_time - start_time:.2f} seconds!")
    print(f"Goal: < 300 seconds (5 mins)")
    print(f"God Objects: {len(god_objects)}")
    print(f"Cycles: {len(spaghetti)}")
    print(f"Microservices: {len(microservices)}")
    print(f"Dead Code Methods: {len(dead_code)}")

if __name__ == '__main__':
    run_test()
