from tkinter import *
from tkinter import simpledialog, messagebox
from WelshPowell import welsh_powell
from Kruskal import kruskal
from Dijkstra import executer_dijkstra_via_interface, afficher_graphe
from BellmanFord import executer_bellman_ford_via_interface
from FordFulkerson import executer_ford_fulkerson_via_interface
from PotentielMetra import executer_pert_via_interface
from SteppingStone import executer_stepping_stone_via_interface
from NordOuest import executer_nord_ouest_via_interface
from MoindreCout import executer_moindre_cout_via_interface

# Création de la fenêtre principale
gui = Tk()
gui.geometry("1000x500")
gui.title("Recherches Opérationnelles")

# Couleurs principales
bg_color = "#ADD8E6"  # Bleu Alice pour l'arrière-plan
button_hover_color = "#8B0000"  # Vert moyen pour les boutons au survol
button_color = "#E6E6FA"  # Lavande pour le cadre principal
title_color = "#4682B4"  # Bleu acier pour le titre principal
output_text_color = "#2F4F4F"  # Gris ardoise foncé pour le texte de sortie

# Arrière-plan principal
gui.config(bg=bg_color)

# Label de titre
title_label = Label(gui, text="Interface Graphique Tkinter", font=("Arial", 18, "bold"), fg="black", bg="#E6E6FA")
title_label.pack(pady=10)

# Cadre principal
main_frame = Frame(gui, relief="solid", bd=3, padx=20, pady=20, bg=button_color)
main_frame.pack(pady=30)

# Titre secondaire
algo_label = Label(main_frame, text="Algorithme de Recherche Opérationnelle", font=("Arial", 12, "bold"),
                   bg=button_color, fg="black")
algo_label.pack(pady=10)


# Fonction pour appliquer le style des boutons
def style_button(button, bg, hover_bg, fg="black"):
    button.config(bg=bg, fg=fg, font=("Arial", 10, "bold"), bd=3, activebackground=hover_bg, relief="raised")


# Fonction pour ouvrir une nouvelle fenêtre
def algorithme():
    guiA = Toplevel(gui)
    guiA.geometry("1000x500")
    guiA.config(bg=bg_color)

    # Label de sortie pour afficher les résultats
    output_label = Label(guiA, text="", font=("Arial", 12), fg=output_text_color, wraplength=900, bg=bg_color)
    output_label.place(x=50, y=300)

    # Fonction pour exécuter Welsh Powell
    def run_welsh_powell():
        try:
            output_label.config(text="Exécution de l'algorithme Welsh-Powell...")
            welsh_powell(guiA, output_label)
        except Exception as e:
            output_label.config(text=f"Erreur : {str(e)}")

    # Fonction pour exécuter Kruskal
    def run_kruskal():
        try:
            output_label.config(text="Exécution de l'algorithme Kruskal...")
            kruskal(guiA, output_label)
        except Exception as e:
            output_label.config(text=f"Erreur : {str(e)}")

    # Fonction pour exécuter Dijkstra
    def run_dijkstra():
        try:
            graphe, distance, chemin = executer_dijkstra_via_interface(guiA)
            if graphe and chemin:
                chemin_str = " -> ".join(chemin)
                messagebox.showinfo("Résultat", f"Distance : {distance}\nChemin : {chemin_str}")
                afficher_graphe(graphe, chemin)  # Afficher le graphe avec le chemin en rouge
        except Exception as e:
            output_label.config(text=f"Erreur : {str(e)}")

    # Fonction pour Bellman-Ford
    def run_bellman_ford():
        try:
            graphe, distance, chemin = executer_bellman_ford_via_interface(guiA)
            if graphe and chemin:
                output_label.config(text="Algorithme de Bellman-Ford exécuté avec succès.")
        except Exception as e:
            output_label.config(text=f"Erreur : {str(e)}")

    # Fonction pour Ford-Fulkerson
    def run_ford_fulkerson():
        try:
            result = executer_ford_fulkerson_via_interface(guiA)
            if result:
                output_label.config(text="Algorithme de Ford-Fulkerson exécuté avec succès.")
        except Exception as e:
            output_label.config(text=f"Erreur : {str(e)}")

    # Fonction pour PERT/MÉTRA
    def run_pert():
        try:
            result = executer_pert_via_interface(guiA)
            if result:
                output_label.config(text="Analyse Potentiel Metra exécutée avec succès.")
        except Exception as e:
            output_label.config(text=f"Erreur : {str(e)}")

    def run_stepping_stone():
        try:
            executer_stepping_stone_via_interface(guiA)
        except Exception as e:
            output_label.config(text=f"Erreur : {str(e)}")

    # Création des boutons
    welsh_powell_button = Button(guiA, text="Welsh Powell", command=run_welsh_powell)
    style_button(welsh_powell_button, button_color, button_hover_color)
    welsh_powell_button.place(x=70, y=120, width=120, height=50)

    kruskal_button = Button(guiA, text="Kruskal", command=run_kruskal)
    style_button(kruskal_button, button_color, button_hover_color)
    kruskal_button.place(x=300, y=120, width=120, height=50)

    dijkstra_button = Button(guiA, text="Dijkstra", command=run_dijkstra)
    style_button(dijkstra_button, button_color, button_hover_color)
    dijkstra_button.place(x=530, y=120, width=120, height=50)

    bellman_ford_button = Button(guiA, text="Bellman-Ford", command=run_bellman_ford)
    style_button(bellman_ford_button, button_color, button_hover_color)
    bellman_ford_button.place(x=760, y=120, width=120, height=50)

    ford_fulkerson_button = Button(guiA, text="Ford-Fulkerson", command=run_ford_fulkerson)
    style_button(ford_fulkerson_button, button_color, button_hover_color)
    ford_fulkerson_button.place(x=70, y=200, width=120, height=50)

    pert_button = Button(guiA, text="PERT/MÉTRA", command=run_pert)
    style_button(pert_button, button_color, button_hover_color)
    pert_button.place(x=300, y=200, width=120, height=50)

    stepping_stone_button = Button(guiA, text="Stepping Stone", command=run_stepping_stone)
    style_button(stepping_stone_button, button_color, button_hover_color)
    stepping_stone_button.place(x=530, y=200, width=120, height=50)

    nord_ouest_button = Button(guiA, text="Nord-Ouest", command=lambda: executer_nord_ouest_via_interface(guiA))
    style_button(nord_ouest_button, button_color, button_hover_color)
    nord_ouest_button.place(x=760, y=200, width=120, height=50)

    moindre_cout_button = Button(guiA, text="Moindre Coût", command=lambda: executer_moindre_cout_via_interface(guiA))
    style_button(moindre_cout_button, button_color, button_hover_color)
    moindre_cout_button.place(x=70, y=280, width=120, height=50)

    btnquit = Button(guiA, text="Quitter", command=guiA.destroy)
    style_button(btnquit, button_color, button_hover_color)
    btnquit.place(x=550, y=300, width=100, height=50)


# Boutons de la fenêtre principale
btn1 = Button(gui, text="Entrer", command=algorithme)
style_button(btn1, button_color, button_hover_color)
btn1.place(x=350, y=250, width=100, height=50)

btn2 = Button(gui, text="Quitter", command=gui.destroy)
style_button(btn2, button_color, button_hover_color)
btn2.place(x=550, y=250, width=100, height=50)

gui.mainloop()