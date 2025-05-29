import networkx as nx
import matplotlib.pyplot as plt
import random

def nodo_letra(i):
    return chr(ord('A') + i)

def es_dirigido():
    opcion = input("¿El grafo es dirigido? (s/n): ").strip().lower()
    return opcion == 's'

def pedir_matriz():
    n = int(input("¿Cuántos nodos tiene el grafo? "))
    print("Introduce la matriz de adyacencia (una fila por línea, separados por espacio):")
    matriz = []
    for _ in range(n):
        fila = list(map(int, input().split()))
        matriz.append(fila)
    return matriz, n

def crear_grafo(matriz, n, dirigido=False):
    G = nx.DiGraph() if dirigido else nx.Graph()
    for i in range(n):
        rango_j = range(n) if dirigido else range(i + 1, n)
        for j in rango_j:
            if matriz[i][j] != 0:
                peso = random.randint(1, 10)
                G.add_edge(nodo_letra(i), nodo_letra(j), weight=peso)
    return G

def verificar_euler(G):
    if isinstance(G, nx.DiGraph):
        if nx.is_eulerian(G):
            print("El grafo dirigido **es Euleriano**.")
            return True, "Euleriano"
        elif nx.has_eulerian_path(G):
            print("ℹEl grafo dirigido **es semi-Euleriano** (tiene camino pero no ciclo).")
            return False, "Semi-Euleriano"
    else:
        if nx.is_eulerian(G):
            print("El grafo no dirigido **es Euleriano**.")
            return True, "Euleriano"
        elif nx.has_eulerian_path(G):
            print("ℹEl grafo no dirigido **es semi-Euleriano** (tiene camino pero no ciclo).")
            return False, "Semi-Euleriano"
    print("El grafo **no es Euleriano**.")
    return False, "No Euleriano"

def seleccionar_destino(G, origen='A'):
    nodos = list(G.nodes())
    if origen not in nodos:
        origen = nodos[0]
    destino = random.choice(nodos)
    while destino == origen:
        destino = random.choice(nodos)
    print(f"Origen fijo: {origen}")
    print(f"Destino aleatorio para Dijkstra: {destino}")
    return origen, destino

def obtener_aristas_por_algoritmo(G, algoritmo, origen='A', destino=None):
    if algoritmo == "prim":
        if isinstance(G, nx.DiGraph):
            return []
        return list(nx.minimum_spanning_edges(G, algorithm="prim", data=False))
    
    elif algoritmo == "kruskal":
        if isinstance(G, nx.DiGraph):
            return []
        return list(nx.minimum_spanning_edges(G, algorithm="kruskal", data=False))
    
    elif algoritmo == "dijkstra":
        if destino is None:
            return []
        try:
            camino = nx.shortest_path(G, source=origen, target=destino, weight='weight')
            return list(zip(camino[:-1], camino[1:]))
        except nx.NetworkXNoPath:
            return []

    elif algoritmo == "bfs":
        return list(nx.bfs_edges(G, source=origen))
    
    elif algoritmo == "dfs":
        return list(nx.dfs_edges(G, source=origen))
    
    elif algoritmo == "hamilton":
        def buscar(camino):
            if len(camino) == len(G):
                return camino
            for vecino in G[camino[-1]]:
                if vecino not in camino:
                    resultado = buscar(camino + [vecino])
                    if resultado:
                        return resultado
            return None
        for inicio in sorted(G.nodes()):
            camino = buscar([inicio])
            if camino:
                return list(zip(camino[:-1], camino[1:]))
        return []

    elif algoritmo == "euleriano":
        if nx.is_eulerian(G):
            return [(u, v) for u, v in nx.eulerian_circuit(G)]
        return []

    return []

def graficar_todos_los_algoritmos(G, posiciones, euler_tipo, origen, destino):
    algoritmos = [
        ("Prim", "prim", "#e74c3c"),
        ("Kruskal", "kruskal", "#e67e22"),
        ("Dijkstra", "dijkstra", "#2980b9"),
        ("BFS", "bfs", "#8e44ad"),
        ("DFS", "dfs", "#16a085"),
        ("Hamilton", "hamilton", "#f39c12"),
        ("Euleriano", "euleriano", "#1abc9c"),
        ("Coloración", "color", "#7f8c8d")
    ]

    filas = 2
    columnas = 4
    fig, axes = plt.subplots(filas, columnas, figsize=(22, 11))
    axes = axes.flatten()

    for i, (titulo, clave, color) in enumerate(algoritmos):
        ax = axes[i]

        if clave == "color":
            colores = nx.coloring.greedy_color(G, strategy="largest_first")
            lista_colores = [colores[nodo] for nodo in G.nodes()]
            cmap = plt.cm.get_cmap("Set3", max(lista_colores) + 1)
            nx.draw_networkx_nodes(G, posiciones, ax=ax, node_color=lista_colores, cmap=cmap,
                                   edgecolors='black', linewidths=1.2, node_size=750)
            nx.draw_networkx_edges(G, posiciones, ax=ax, edge_color="#BDC3C7", width=1.2)
            nx.draw_networkx_labels(G, posiciones, ax=ax, font_size=12, font_weight='bold')
            ax.set_title("Coloración", fontsize=14, color="#2C3E50")
            ax.axis('off')
            continue

        if clave == "dijkstra":
            aristas = obtener_aristas_por_algoritmo(G, clave, origen, destino)
        else:
            aristas = obtener_aristas_por_algoritmo(G, clave, origen)

        H = nx.Graph() if not isinstance(G, nx.DiGraph) else nx.DiGraph()
        peso_total = 0
        ruta_nodos = []

        for u, v in aristas:
            if G.has_edge(u, v):
                peso = G[u][v]['weight']
                H.add_edge(u, v, weight=peso)
                peso_total += peso
                if u not in ruta_nodos:
                    ruta_nodos.append(u)
                if v not in ruta_nodos:
                    ruta_nodos.append(v)

        pesos = nx.get_edge_attributes(H, 'weight')

        nx.draw_networkx_nodes(G, posiciones, ax=ax, node_color="#D6EAF8",
                               edgecolors="#1B4F72", linewidths=1.5, node_size=700)
        nx.draw_networkx_edges(G, posiciones, ax=ax, edge_color="#D0D3D4", width=1, style='dashed')
        nx.draw_networkx_labels(G, posiciones, ax=ax, font_size=12, font_family='sans-serif', font_weight='bold')

        nx.draw_networkx_edges(H, posiciones, ax=ax, edge_color=color, width=2.5,
                               arrows=isinstance(G, nx.DiGraph))
        if clave not in ["bfs", "dfs"]:
            nx.draw_networkx_edge_labels(H, posiciones, edge_labels=pesos, ax=ax, font_size=10)

        if clave == "euleriano":
            titulo_completo = f"{titulo} ({euler_tipo})"
        elif clave == "dijkstra" and aristas:
            titulo_completo = f"{titulo} (A → {destino})\nPeso Total: {peso_total}, Ruta: {' → '.join(ruta_nodos)}"
        elif aristas:
            titulo_completo = f"{titulo}\nPeso Total: {peso_total}, Ruta: {' → '.join(ruta_nodos)}"
        else:
            titulo_completo = f"{titulo}\n(No aplica o no encontrado)"

        ax.set_title(titulo_completo, fontsize=11, color=color)
        ax.axis('off')

    plt.tight_layout()
    plt.savefig("grafo_todos_algoritmos.png", dpi=300)
    plt.show()
    print("Imagen combinada guardada como grafo_todos_algoritmos.png")

def main():
    dirigido = es_dirigido()
    matriz, n = pedir_matriz()
    G = crear_grafo(matriz, n, dirigido)
    posiciones = nx.spring_layout(G, seed=42)
    es_euler, euler_tipo = verificar_euler(G)
    origen, destino = seleccionar_destino(G)
    graficar_todos_los_algoritmos(G, posiciones, euler_tipo, origen, destino)

main()
