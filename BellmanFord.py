# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt
import random
import time
from tkinter import messagebox,simpledialog

def generer_graphe_aleatoire(nombre_sommets):
    graphe = nx.DiGraph()
    sommets = [f'x{i}' for i in range(nombre_sommets)]
    graphe.add_nodes_from(sommets)
    
    for i in range(nombre_sommets):
        for j in range(nombre_sommets):
            if i != j and random.choice([True, False]):
                poids = random.randint(1, 100)
                graphe.add_edge(sommets[i], sommets[j], weight=poids)
    
    return graphe

def afficher_graphe(graphe, chemin=None):
    plt.figure()  # Créer une nouvelle figure pour chaque graphe
    pos = nx.spring_layout(graphe)
    nx.draw(graphe, pos, with_labels=True, node_color='skyblue', 
            node_size=500, font_size=10, font_weight='bold', arrows=True)
    
    labels = nx.get_edge_attributes(graphe, 'weight')
    nx.draw_networkx_edge_labels(graphe, pos, edge_labels=labels)
    
    if chemin:
        chemin_edges = list(zip(chemin, chemin[1:]))
        nx.draw_networkx_edges(graphe, pos, edgelist=chemin_edges, 
                             edge_color='red', width=2, arrows=True)
    
    plt.show()

def executer_bellman_ford_via_interface(window):
    # Demander le nombre de sommets
    nombre_sommets = int(simpledialog.askstring("Input", "Entrez le nombre de sommets:"))

    # Générer le graphe aléatoire
    graphe = generer_graphe_aleatoire(nombre_sommets)
    
    # Afficher le graphe initial
    afficher_graphe(graphe)
    
    # Demander les sommets source et cible
    source = simpledialog.askstring("Input",
        "Entrez le sommet de départ (ex: x0):")
    cible = simpledialog.askstring("Input",
        "Entrez le sommet d'arrivée (ex: x1):")
    
    # Mesurer le temps d'exécution
    start_time = time.time()
    
    try:
        # Calculer la distance et le chemin
        distance, chemin = nx.single_source_bellman_ford(graphe, source, target=cible)
        end_time = time.time()
        
        # Créer le message de résultat
        message = (f"La plus courte distance de {source} à {cible} est {distance} Km.\n"
                  f"Chemin le plus court: {' -> '.join(chemin)}\n"
                  f"Temps d'exécution: {end_time - start_time:.4f} secondes.")
        
        # Afficher le résultat
        messagebox.showinfo("Résultat", message)
        
        # Afficher le graphe avec le chemin
        afficher_graphe(graphe, chemin)
        
        return graphe, distance, chemin
        
    except nx.NetworkXNoPath:
        messagebox.showerror("Erreur", 
            f"Aucun chemin n'existe entre {source} et {cible}.")
        return None, None, None