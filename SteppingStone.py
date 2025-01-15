import numpy as np
from tabulate import tabulate
from tkinter import simpledialog, messagebox


# Étape 1: Génération des données aléatoires
def generate_data(nb_usines, nb_magasins, min_cost=1, max_cost=20, min_cap=10, max_cap=50):
    couts = np.random.randint(min_cost, max_cost, size=(nb_usines, nb_magasins))
    capacites = np.random.randint(min_cap, max_cap, size=nb_usines)
    demandes = np.random.randint(min_cap, max_cap, size=nb_magasins)

    total_capacite = sum(capacites)
    total_demande = sum(demandes)
    if total_capacite > total_demande:
        demandes[-1] += total_capacite - total_demande
    else:
        capacites[-1] += total_demande - total_capacite

    return couts, capacites, demandes

def executer_stepping_stone_via_interface(gui):
    try:
        # Demander les paramètres via `simpledialog`
        nb_usines = simpledialog.askinteger("Entrée", "Entrez le nombre d'usines :", parent=gui)
        nb_magasins = simpledialog.askinteger("Entrée", "Entrez le nombre de magasins :", parent=gui)
        
        if nb_usines is None or nb_magasins is None:
            messagebox.showinfo("Info", "Entrée annulée.")
            return

        # Générer les données
        couts, capacites, demandes = generate_data(nb_usines, nb_magasins)

        # Résolution avec Moindres Coûts (comme point de départ)
        allocation_moindre_cout = moindre_cout(couts, capacites.copy(), demandes.copy())

        # Optimisation avec Stepping Stone
        allocation_optimisee = stepping_stone(couts, allocation_moindre_cout)
        cout_optimise = calculer_cout_total(couts, allocation_optimisee)

        # Affichage des résultats
        result = f"Allocation Optimisée :\n{tabulate(allocation_optimisee, tablefmt='fancy_grid')}\n"
        result += f"Coût total optimisé : {cout_optimise}"
        messagebox.showinfo("Résultat", result)

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")


# Calculer le coût total pour une allocation donnée
def calculer_cout_total(couts, allocation):
    return np.sum(couts * allocation)


# Algorithme Nord-Ouest
def nord_ouest(capacites, demandes):
    allocation = np.zeros((len(capacites), len(demandes)), dtype=int)
    i, j = 0, 0
    while i < len(capacites) and j < len(demandes):
        alloc = min(capacites[i], demandes[j])
        allocation[i, j] = alloc
        capacites[i] -= alloc
        demandes[j] -= alloc
        if capacites[i] == 0:
            i += 1
        if demandes[j] == 0:
            j += 1
    return allocation


# Algorithme des moindres coûts
def moindre_cout(couts, capacites, demandes):
    allocation = np.zeros_like(couts, dtype=int)
    couts_temp = couts.astype(float)
    while np.any(capacites) and np.any(demandes):
        i, j = np.unravel_index(np.argmin(couts_temp, axis=None), couts_temp.shape)
        alloc = min(capacites[i], demandes[j])
        allocation[i, j] = alloc
        capacites[i] -= alloc
        demandes[j] -= alloc
        if capacites[i] == 0:
            couts_temp[i, :] = np.inf
        if demandes[j] == 0:
            couts_temp[:, j] = np.inf
    return allocation

def stepping_stone(couts, allocation):
    rows, cols = allocation.shape
    couts = couts.astype(float)  # S'assurer que les coûts sont en float
    while True:
        # Étape 1 : Identifier les cases non allouées
        empty_cells = [(i, j) for i in range(rows) for j in range(cols) if allocation[i, j] == 0]

        # Étape 2 : Tester chaque case vide pour des cycles d'amélioration
        best_improvement = 0
        best_allocation = allocation.copy()
        
        for cell in empty_cells:
            # Trouver un cycle fermé pour la case vide
            cycle, gain = find_cycle_and_gain(couts, allocation, cell)
            if cycle and gain < best_improvement:
                best_improvement = gain
                best_allocation = adjust_allocation(allocation, cycle)

        # Étape 3 : Appliquer la meilleure amélioration si possible
        if best_improvement >= 0:
            break  # Pas d'amélioration possible, la solution est optimale
        allocation = best_allocation

    return allocation


def find_cycle_and_gain(couts, allocation, start_cell):
    rows, cols = allocation.shape
    visited = set()
    cycle = []

    def dfs(cell, path):
        if cell in visited:
            if cell == start_cell and len(path) >= 4:  # Cycle trouvé
                return path
            return None

        visited.add(cell)
        row, col = cell

        # Explorer les cases dans la même ligne et colonne
        for next_cell in [(row, c) for c in range(cols)] + [(r, col) for r in range(rows)]:
            if next_cell != cell and allocation[next_cell] > 0 or next_cell == start_cell:
                new_path = dfs(next_cell, path + [cell])
                if new_path:
                    return new_path

        visited.remove(cell)
        return None

    # Trouver un cycle en démarrant du point
    cycle = dfs(start_cell, [])

    if not cycle:
        return None, 0

    # Calculer le gain net du cycle
    gain = calculate_cycle_gain(couts, allocation, cycle)
    return cycle, gain


def calculate_cycle_gain(couts, allocation, cycle):
    gain = 0
    for k, (i, j) in enumerate(cycle):
        sign = 1 if k % 2 == 0 else -1  # Alterner entre + et -
        gain += sign * couts[i, j]
    return gain


def adjust_allocation(allocation, cycle):
    min_alloc = min(allocation[i, j] for k, (i, j) in enumerate(cycle) if k % 2 == 1)  # Trouver la plus petite allocation

    # Ajuster les allocations le long du cycle
    for k, (i, j) in enumerate(cycle):
        sign = 1 if k % 2 == 0 else -1
        allocation[i, j] += sign * min_alloc

    return allocation


# Optimisation Stepping Stone (déjà défini dans le précédent code)

# Fonction pour afficher un tableau formaté
def afficher_tableau(data, row_labels=None, col_labels=None, title=None):
    if row_labels is not None and col_labels is not None:
        table = tabulate(data, headers=col_labels, showindex=row_labels, tablefmt="fancy_grid")
    else:
        table = tabulate(data, tablefmt="fancy_grid")
    if title:
        print(f"\n{title}\n{'=' * len(title)}")
    print(table)


# Fonction principale
def main():
    nb_usines = int(input("Entrez le nombre d'usines: "))
    nb_magasins = int(input("Entrez le nombre de magasins: "))

    couts, capacites, demandes = generate_data(nb_usines, nb_magasins)

    afficher_tableau(couts, 
                     row_labels=[f"Usine {i+1}" for i in range(nb_usines)], 
                     col_labels=[f"Magasin {j+1}" for j in range(nb_magasins)], 
                     title="Coûts unitaires")

    print("\nCapacités des usines:", capacites)
    print("Demandes des magasins:", demandes)

    # Résolution avec Nord-Ouest
    allocation_nord_ouest = nord_ouest(capacites.copy(), demandes.copy())
    cout_nord_ouest = calculer_cout_total(couts, allocation_nord_ouest)
    afficher_tableau(allocation_nord_ouest, 
                     row_labels=[f"Usine {i+1}" for i in range(nb_usines)], 
                     col_labels=[f"Magasin {j+1}" for j in range(nb_magasins)], 
                     title="Allocation (Nord-Ouest)")
    print(f"Coût total (Nord-Ouest): {cout_nord_ouest}")

    # Résolution avec Moindres Coûts
    allocation_moindre_cout = moindre_cout(couts, capacites.copy(), demandes.copy())
    cout_moindre_cout = calculer_cout_total(couts, allocation_moindre_cout)
    afficher_tableau(allocation_moindre_cout, 
                     row_labels=[f"Usine {i+1}" for i in range(nb_usines)], 
                     col_labels=[f"Magasin {j+1}" for j in range(nb_magasins)], 
                     title="Allocation (Moindres Coûts)")
    print(f"Coût total (Moindres Coûts): {cout_moindre_cout}")

    # Optimisation avec Stepping Stone
    allocation_optimisee = stepping_stone(couts, allocation_moindre_cout)
    cout_optimise = calculer_cout_total(couts, allocation_optimisee)
    afficher_tableau(allocation_optimisee, 
                     row_labels=[f"Usine {i+1}" for i in range(nb_usines)], 
                     col_labels=[f"Magasin {j+1}" for j in range(nb_magasins)], 
                     title="Allocation Optimisée (Stepping Stone)")
    print(f"Coût total optimisé: {cout_optimise}")

if __name__ == "__main__":
 main()