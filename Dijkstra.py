import networkx as nx
import matplotlib.pyplot as plt
import random
from tkinter import simpledialog, messagebox

def generer_graphe_aleatoire(nombre_sommets):
    graphe = nx.Graph()
    sommets = [f'x{i}' for i in range(nombre_sommets)]
    graphe.add_nodes_from(sommets)
    
    # Ajouter des arêtes avec des poids aléatoires
    for i in range(nombre_sommets):
        for j in range(i + 1, nombre_sommets):
            if random.choice([True, False]):  # Arête aléatoire
                poids = random.randint(1, 20)
                graphe.add_edge(sommets[i], sommets[j], weight=poids)
    
    return graphe

def afficher_graphe(graphe, chemin=None):
    pos = nx.spring_layout(graphe)
    nx.draw(graphe, pos, with_labels=True, node_color='skyblue', node_size=500, font_size=10, font_weight='bold')

    labels = nx.get_edge_attributes(graphe, 'weight')
    nx.draw_networkx_edge_labels(graphe, pos, edge_labels=labels)

    if chemin:
        chemin_edges = list(zip(chemin, chemin[1:]))
        nx.draw_networkx_edges(graphe, pos, edgelist=chemin_edges, edge_color='red', width=2)

    plt.show()

def executer_dijkstra_via_interface(parent):
    try:
        # Demander le nombre de sommets
        nombre_sommets = simpledialog.askinteger("Entrée", "Entrez le nombre de sommets :", parent=parent, minvalue=2)
        if nombre_sommets is None:
            return None, None, None  # Annulé par l'utilisateur
        
        # Générer un graphe aléatoire
        graphe = generer_graphe_aleatoire(nombre_sommets)

        sommets = list(graphe.nodes())

        # Demander le sommet source
        source = simpledialog.askstring("Source", f"Entrez le sommet de départ (choix : {', '.join(sommets)})", parent=parent)
        if source not in sommets:
            messagebox.showerror("Erreur", "Sommet source invalide.")
            return None, None, None

        # Demander le sommet cible
        cible = simpledialog.askstring("Cible", f"Entrez le sommet d'arrivée (choix : {', '.join(sommets)})", parent=parent)
        if cible not in sommets:
            messagebox.showerror("Erreur", "Sommet cible invalide.")
            return None, None, None

        # Calculer la distance et le chemin
        distance, chemin = nx.single_source_dijkstra(graphe, source, target=cible)
        return graphe, distance, chemin

    except nx.NetworkXNoPath:
        messagebox.showinfo("Résultat", "Aucun chemin trouvé entre les sommets.")
        return None, None, None

    except Exception as e:
        messagebox.showerror("Erreur", str(e))
        return None, None, None
