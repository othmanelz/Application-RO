import random
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import messagebox, simpledialog

def generate_tasks(num_tasks):
    tasks = []
    for i in range(1, num_tasks + 1):
        duration = random.randint(1, 10)
        predecessors = []
        if i > 1:
            predecessors = random.sample(range(1, i), random.randint(0, i - 1))
        tasks.append((f"T{i}", duration, predecessors))
    return tasks

def create_pert_graph(tasks):
    graph = nx.DiGraph()
    for task, duration, predecessors in tasks:
        graph.add_node(task, duration=duration)
        for pred in predecessors:
            graph.add_edge(f"T{pred}", task)
    return graph

def compute_pert_schedule(graph):
    earliest_start = {}
    latest_start = {}
    critical_path = []
    
    # Calcul des dates au plus tôt (forward pass)
    for node in nx.topological_sort(graph):
        pred_durations = [earliest_start[pred] + graph.nodes[pred]['duration'] 
                         for pred in graph.predecessors(node)]
        earliest_start[node] = max(pred_durations, default=0)
    
    # Durée totale du projet
    project_duration = max(earliest_start[node] + graph.nodes[node]['duration'] 
                         for node in graph.nodes)
    
    # Calcul des dates au plus tard (backward pass)
    for node in reversed(list(nx.topological_sort(graph))):
        succ_durations = [latest_start[succ] for succ in graph.successors(node)]
        latest_start[node] = min(succ_durations, default=project_duration) - graph.nodes[node]['duration']
    
    # Identifier le chemin critique
    for node in graph.nodes:
        if earliest_start[node] == latest_start[node]:
            critical_path.append(node)
            
    return earliest_start, latest_start, critical_path, project_duration

def plot_potential_metra(graph, earliest_start, latest_start, critical_path):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    
    # Couleurs des nœuds
    node_colors = ["red" if node in critical_path else "lightblue" for node in graph.nodes]
    
    # Labels avec toutes les informations
    labels = {
        node: f"{node}\nDurée: {graph.nodes[node]['duration']}\nDébut tôt: {earliest_start[node]}\nDébut tard: {latest_start[node]}"
        for node in graph.nodes
    }
    
    # Dessiner le graphe
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=2500)
    nx.draw_networkx_edges(graph, pos, arrowstyle='->', arrowsize=15)
    nx.draw_networkx_labels(graph, pos, labels, font_size=8, font_color="black")
    
    plt.title("Diagramme de Potentiel MÉTRA (PERT)")
    plt.axis("off")
    plt.show()

def executer_pert_via_interface(window):
    # Demander le nombre de tâches
    num_tasks = simpledialog.askinteger("Input", 
        "Entrez le nombre de tâches:", minvalue=1)
    
    if num_tasks is None:
        return None
        
    try:
        # Générer les tâches
        tasks = generate_tasks(num_tasks)
        
        # Créer le message pour afficher les tâches générées
        tasks_message = "Tâches générées :\n"
        for task, duration, predecessors in tasks:
            tasks_message += f"{task} - Durée: {duration}, Antériorité: {predecessors}\n"
        
        messagebox.showinfo("Tâches générées", tasks_message)
        
        # Créer et calculer le graphe PERT
        pert_graph = create_pert_graph(tasks)
        earliest_start, latest_start, critical_path, project_duration = compute_pert_schedule(pert_graph)
        
        # Créer le message de résultat
        result_message = (
            f"Durée totale du projet : {project_duration} jours\n"
            f"Chemin critique : {' -> '.join(critical_path)}\n\n"
            "Dates au plus tôt :\n"
        )
        for task in earliest_start:
            result_message += f"{task}: {earliest_start[task]}\n"
        
        result_message += "\nDates au plus tard :\n"
        for task in latest_start:
            result_message += f"{task}: {latest_start[task]}\n"
            
        messagebox.showinfo("Résultats PERT", result_message)
        
        # Afficher le diagramme
        plot_potential_metra(pert_graph, earliest_start, latest_start, critical_path)
        
        return pert_graph, project_duration, critical_path
        
    except Exception as e:
        messagebox.showerror("Erreur", 
            f"Une erreur s'est produite: {str(e)}")
        return None