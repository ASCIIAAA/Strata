import networkx as nx

def build_code_graph(relationships):
    G = nx.DiGraph() # Directed Graph (A calls B)

    for rel in relationships:
        # We add an 'edge' (a line) between the caller class and the target
        G.add_edge(rel['caller'], rel['target_method'])
    
    return G

def find_god_objects(G):
    # A simple "God Object" metric is Out-Degree (how many things it talks to)
    # and In-Degree (how many things talk to it)
    report = {}
    for node in G.nodes():
        degree = G.degree(node)
        if degree > 10: # Threshold for 2nd-year demo
            report[node] = {"status": "God Object Candidate", "score": degree}
    return report