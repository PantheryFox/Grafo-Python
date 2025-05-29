import networkx as nx
import matplotlib.pyplot as plt
import random


#  Funciones generales ( para pedir la matriz y generar los grafos)


def nodo_letra(i):
    return chr(ord('A') + i)

def pedir_matriz():
    n = int(input("¿Cuántos nodos tiene el grafo? "))
    print("Introduce la matriz de adyacencia (una fila por línea, separados por espacio):")
    matriz = []
    for _ in range(n):
        fila = list(map(int, input().split()))
        matriz.append(fila)
    return matriz, n

def crear_grafo(matriz, n):
    G = nx.Graph()
    for i in range(n):
        for j in range(i + 1, n):
            if matriz[i][j] != 0:
                peso = random.randint(1, 10)
                G.add_edge(nodo_letra(i), nodo_letra(j), weight=peso)
    return G

def obtener_aristas_por_algoritmo(G, algoritmo, origen='A'):
    if algoritmo == "prim":
        return list(nx.minimum_spanning_edges(G, algorithm="prim", data=False))
    elif algoritmo == "kruskal":
        return list(nx.minimum_spanning_edges(G, algorithm="kruskal", data=False))
    elif algoritmo == "dijkstra":
        caminos = nx.single_source_dijkstra_path(G, origen)
        aristas = []
        for camino in caminos.values():
            aristas += list(zip(camino[:-1], camino[1:]))
        return aristas
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

def graficar_todos_los_algoritmos(G, posiciones):
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
            # Parte en donde se genera el grafo de color
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

        # Parte para generar los siguientes grafos
        aristas = obtener_aristas_por_algoritmo(G, clave)
        H = nx.Graph()
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

        nx.draw_networkx_edges(H, posiciones, ax=ax, edge_color=color, width=2.5)
        nx.draw_networkx_edge_labels(H, posiciones, edge_labels=pesos, ax=ax, font_size=10)

        if aristas:
            titulo_completo = f"{titulo}\nPeso Total: {peso_total}, Ruta: {' → '.join(ruta_nodos)}"
        else:
            titulo_completo = f"{titulo}\n(No aplica o no encontrado)"

        ax.set_title(titulo_completo, fontsize=11, color=color)
        ax.axis('off')

    plt.tight_layout()
    plt.savefig("grafo_todos_algoritmos.png", dpi=300)
    plt.show()
    print("Imagen combinada guardada como grafo_todos_algoritmos.png")



#  Coloración de nodos


def coloracion_nodos(G, posiciones):
    colores = nx.coloring.greedy_color(G, strategy="largest_first")
    lista_colores = [colores[nodo] for nodo in G.nodes()]
    cmap = plt.cm.get_cmap("Set3", max(lista_colores) + 1)

    plt.figure(figsize=(7, 6))
    nx.draw_networkx_nodes(G, posiciones, node_color=lista_colores, cmap=cmap, node_size=750,
                           edgecolors='black', linewidths=1.2)
    nx.draw_networkx_edges(G, posiciones, edge_color="#BDC3C7", width=1.2)
    nx.draw_networkx_labels(G, posiciones, font_size=12, font_weight='bold')
    plt.title("Coloración de Nodos", fontsize=16, color="#2C3E50")
    plt.axis('off')
    plt.savefig("grafo_coloracion.png", dpi=300)
    plt.show()
    print("Grafo de coloración guardado como grafo_coloracion.png")



 #  Programa principal (En donde se mostraran todos los grafos)

def main():
    matriz, n = pedir_matriz()
    G = crear_grafo(matriz, n)
    posiciones = nx.spring_layout(G, seed=42)
    graficar_todos_los_algoritmos(G, posiciones)

main()
