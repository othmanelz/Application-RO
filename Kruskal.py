# Kruskal.py
import networkx as nx
import random
import string
import matplotlib.pyplot as plt
from itertools import combinations
from tkinter import simpledialog,messagebox

def generer_graphe_pondere_gui(gui):
    while True:
        try:
            n = simpledialog.askinteger(
                "Entrée",
                "Entrez le nombre de sommets (max {}): ".format(len(string.ascii_uppercase) * (len(string.ascii_uppercase) - 1) // 2),
                parent=gui,
                minvalue=1
            )
            if n is None:  # Si l'utilisateur annule
                return None
            break
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre entier.")
    
    sommets = [''.join(comb) for comb in combinations(string.ascii_uppercase, 2)][:n]
    G = nx.Graph()
    G.add_nodes_from(sommets)
    
    for i in range(n):
        for j in range(i + 1, n):
            poids = random.randint(1, 100)
            G.add_edge(sommets[i], sommets[j], weight=poids)
    
    return G

def kruskal(gui, output_label):
    # Générer d'abord le graphe
    G = generer_graphe_pondere_gui(gui)
    if G is None:
        return
    
    # Dessiner le graphe initial
    plt.figure(1)
    dessiner_graphe_gui(G)
    
    # Exécuter l'algorithme de Kruskal
    edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
    parent = {node: node for node in G.nodes()}
    rank = {node: 0 for node in G.nodes()}
    
    def find(v):
        if parent[v] != v:
            parent[v] = find(parent[v])
        return parent[v]
    
    def union(u, v):
        root_u = find(u)
        root_v = find(v)
        
        if root_u != root_v:
            if rank[root_u] > rank[root_v]:
                parent[root_v] = root_u
            elif rank[root_u] < rank[root_v]:
                parent[root_u] = root_v
            else:
                parent[root_v] = root_u
                rank[root_u] += 1
    
    mst_edges = []
    total_cost = 0
    
    for u, v, data in edges:
        if find(u) != find(v):
            union(u, v)
            mst_edges.append((u, v, data['weight']))
            total_cost += data['weight']
    
    # Afficher les résultats dans l'interface graphique
    output = f"Coût total de l'arbre couvrant : {total_cost}\n"
    output += "Les arêtes de l'arbre couvrant avec leurs poids :\n"
    
    messagebox.showinfo(
    "Résultat de Kruskal",
    f"Coût total de l'arbre couvrant : {total_cost}\n\n"
    + "\n".join([f"({u}, {v}) avec poids {weight}" for u, v, weight in mst_edges])
)

    for u, v, weight in mst_edges:
        output += f"({u}, {v}) avec poids {weight}\n"
    
    output_label.config(text=output)
    
    # Dessiner le graphe avec l'arbre couvrant minimal
    plt.figure(2)
    dessiner_graphe_gui(G, mst_edges)

def dessiner_graphe_gui(G, mst_edges=None):
    pos = nx.spring_layout(G)
    plt.clf()
    
    # Dessiner le graphe normal
    nx.draw(G, pos, with_labels=True, node_color='skyblue', 
            edge_color='gray', node_size=2000, font_size=10, 
            font_weight='bold')
    
    # Si des arêtes d'arbre couvrant sont fournies, les dessiner
    if mst_edges is not None:
        mst_graph = nx.Graph()
        mst_graph.add_weighted_edges_from(mst_edges)
        nx.draw_networkx_edges(mst_graph, pos, edge_color='red', width=2)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.title("Graphe Pondéré" + (" et Arbre Couvrant (MST)" if mst_edges else ""))
    plt.show(block=False)
