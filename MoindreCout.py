from tkinter import simpledialog, messagebox
import numpy as np
from tabulate import tabulate

def moindre_cout(capacites, demandes, couts):
    """
    Implémente la méthode de Moindre Coût pour résoudre le problème de transport.
    """
    allocation = np.zeros_like(couts, dtype=int)
    lignes, colonnes = len(capacites), len(demandes)
    
    # Créer une liste des indices triés par coût croissant
    indices = sorted(((i, j) for i in range(lignes) for j in range(colonnes)), key=lambda x: couts[x[0]][x[1]])
    
    for i, j in indices:
        if capacites[i] == 0 or demandes[j] == 0:
            continue
        valeur = min(capacites[i], demandes[j])
        allocation[i][j] = valeur
        capacites[i] -= valeur
        demandes[j] -= valeur

    return allocation

def calculer_cout_total(couts, allocation):
    """
    Calcule le coût total à partir de la matrice des coûts et de l'allocation.
    """
    return np.sum(couts * allocation)

def executer_moindre_cout_via_interface(gui):
    try:
        # Demander les dimensions
        nb_usines = simpledialog.askinteger("Entrée", "Entrez le nombre d'usines :", parent=gui)
        nb_magasins = simpledialog.askinteger("Entrée", "Entrez le nombre de magasins :", parent=gui)

        if nb_usines is None or nb_magasins is None:
            messagebox.showinfo("Info", "Entrée annulée.")
            return

        # Générer les coûts, capacités et demandes aléatoires
        couts = np.random.randint(1, 20, size=(nb_usines, nb_magasins))
        capacites = np.random.randint(20, 50, size=nb_usines)
        demandes = np.random.randint(20, 50, size=nb_magasins)

        # S'assurer que l'offre totale égale la demande totale
        total_offre = np.sum(capacites)
        total_demande = np.sum(demandes)
        difference = abs(total_offre - total_demande)

        if total_offre > total_demande:
            demandes[-1] += difference
        elif total_demande > total_offre:
            capacites[-1] += difference

        # Résolution par Moindre Coût
        allocation = moindre_cout(capacites.copy(), demandes.copy(), couts)
        cout_total = calculer_cout_total(couts, allocation)

        # Affichage des résultats
        result = f"Tableau des coûts :\n{tabulate(couts, tablefmt='fancy_grid')}\n"
        result += f"\nCapacités : {capacites}\nDemandes : {demandes}\n"
        result += f"\nAllocation :\n{tabulate(allocation, tablefmt='fancy_grid')}\n"
        result += f"\nCoût total : {cout_total}"
        messagebox.showinfo("Résultat", result)

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
