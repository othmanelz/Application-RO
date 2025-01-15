import random
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import messagebox, simpledialog

def generate_random_graph(num_nodes):
    graph = {}
    for i in range(num_nodes):
        graph[i] = {}
        for j in range(num_nodes):
            if i != j and random.random() < 0.3:
                graph[i][j] = random.randint(1, 20)
    return graph

def bfs(graph, residual, source, sink, parent):
    visited = set()
    queue = deque([source])
    visited.add(source)
    while queue:
        current = queue.popleft()
        for neighbor, capacity in residual[current].items():
            if neighbor not in visited and capacity > 0:
                parent[neighbor] = current
                if neighbor == sink:
                    return True
                queue.append(neighbor)
                visited.add(neighbor)
    return False

def ford_fulkerson(graph, source, sink):
    residual = {u: {v: capacity for v, capacity in neighbors.items()} 
                for u, neighbors in graph.items()}
    max_flow = 0
    parent = {}
    
    while bfs(graph, residual, source, sink, parent):
        path_flow = float('Inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, residual[parent[s]][s])
            s = parent[s]
            
        max_flow += path_flow
        
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] = residual.get(v, {}).get(u, 0) + path_flow
            v = u
            
    return max_flow, residual

def draw_graph(graph, title="Graphe avec capacités", final_flow=None):
    plt.figure(figsize=(10, 8))
    g = nx.DiGraph()
    
    for u in graph:
        for v, capacity in graph[u].items():
            if final_flow:
                flow = capacity - final_flow[u].get(v, 0)
                label = f"{flow}/{capacity}"
            else:
                label = capacity
            g.add_edge(u, v, capacity=label)
    
    pos = nx.spring_layout(g)
    nx.draw(g, pos, with_labels=True, node_color="lightblue", 
            node_size=500, font_size=10, font_weight='bold')
    
    edge_labels = {(u, v): d['capacity'] for u, v, d in g.edges(data=True)}
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
    
    plt.title(title)
    plt.show()

def executer_ford_fulkerson_via_interface(window):
    # Demander le nombre de sommets
    num_nodes = simpledialog.askinteger("Input", 
        "Entrez le nombre de sommets:", minvalue=2)
    
    if num_nodes is None:
        return None
        
    # Générer le graphe
    graph = generate_random_graph(num_nodes)
    
    # Définir source et puits
    source = 0
    sink = num_nodes - 1
    
    # Afficher le graphe initial
    draw_graph(graph, "Graphe initial")
    
    try:
        # Calculer le flot maximum
        max_flow, residual = ford_fulkerson(graph, source, sink)
        
        # Afficher le résultat
        message = (f"Flot maximum du sommet {source} au sommet {sink}: {max_flow}\n\n"
                  f"Source: sommet {source}\n"
                  f"Puits: sommet {sink}")
        
        messagebox.showinfo("Résultat", message)
        
        # Afficher le graphe avec les flots
        draw_graph(graph, "Graphe avec flots maximums", residual)
        
        return graph, max_flow, residual
        
    except Exception as e:
        messagebox.showerror("Erreur", 
            f"Une erreur s'est produite: {str(e)}")
        return None