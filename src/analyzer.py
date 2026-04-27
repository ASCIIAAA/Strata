import networkx as nx

try:
    from networkx.algorithms.community import louvain_communities
    HAS_LOUVAIN = True
except ImportError:
    HAS_LOUVAIN = False


def build_code_graph(relationships):
    G = nx.DiGraph() 

    for rel in relationships:
        if rel['caller_class'] and rel['qualifier']:
            # Graph between classes based on method calls (class-level graph)
            G.add_edge(rel['caller_class'], rel['qualifier'])
    
    return G

def build_method_graph(relationships):
    """ Builds a directed graph of specific method calls e.g., ClassA.method1 -> ClassB.method2 """
    G = nx.DiGraph()
    for rel in relationships:
        if rel['caller_method'] and rel['qualifier'] and rel['target_method']:
            u = f"{rel['caller_class']}.{rel['caller_method']}"
            v = f"{rel['qualifier']}.{rel['target_method']}"
            G.add_edge(u, v)
            
    return G

def find_god_objects(G, class_stats):
    report = {}
    for node in G.nodes():
        degree = G.degree(node)
        in_degree = G.in_degree(node)
        out_degree = G.out_degree(node)
        
        c_stats = class_stats.get(node, {})
        method_count = len(c_stats.get("methods", []))
        deps = len(c_stats.get("deps", []))
        
        # God Object heuristics
        if method_count > 20 or degree > 10 or deps > 5:
            # We flag it
            report[node] = {
                "status": "God Object Candidate",
                "score": degree,
                "methods": method_count,
                "in_degree": in_degree,
                "out_degree": out_degree,
                "responsibilities": deps
            }
    return report

def find_spaghetti_cycles(G):
    """ Detect cyclic dependencies amongst classes. Limits length to 5 for perf. """
    try:
        cycles = list(nx.simple_cycles(G))
    except Exception as e:
        cycles = []
    
    # Filter only meaningful cycles (A -> B -> A)
    spaghetti = [c for c in cycles if len(c) > 1 and len(c) <= 5]
    return spaghetti

def cluster_microservices(G):
    """ Returns a list of sets, where each set is a proposed microservice. """
    undirected_G = G.to_undirected()
    if HAS_LOUVAIN and len(undirected_G.nodes) > 0:
        communities = louvain_communities(undirected_G)
        return list(communities)
    else:
        # Fallback to connected components
        components = nx.connected_components(undirected_G)
        return list(components)

def find_dead_code(method_graph, class_stats):
    """
    Finds 'Ghost Code' (methods not accessible from entry points).
    Entry points are heuristically methods with in_degree == 0.
    """
    # 1. Identify all defined methods
    all_defined_methods = set()
    for c_name, stats in class_stats.items():
        for m_name in stats.get("methods", []):
            all_defined_methods.add(f"{c_name}.{m_name}")
            
    # 2. Add them to graph if not present
    for m in all_defined_methods:
        if m not in method_graph:
            method_graph.add_node(m)
            
    # 3. Find entry points (in_degree == 0)
    entry_points = [n for n in method_graph.nodes() if method_graph.in_degree(n) == 0]
    
    # 4. Find all reachable nodes from entry points
    reachable = set()
    for ep in entry_points:
        descendants = nx.descendants(method_graph, ep)
        reachable.add(ep)
        reachable.update(descendants)
        
    # 5. Dead code = all_defined - reachable
    dead_code = all_defined_methods - reachable
    return list(dead_code)