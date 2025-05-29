 Visualización de Algoritmos de Grafos en Python

 Descripción
--------------
Este proyecto es una herramienta educativa interactiva desarrollada en Python, que permite visualizar y comparar distintos algoritmos de grafos sobre una estructura generada a partir de una matriz de adyacencia. 
Se utilizan librerías como `networkx` y `matplotlib` para representar gráficamente los recorridos, rutas, árboles mínimos y coloraciones de nodos.

Requisitos del sistema
--------------------------
- Python 3.8 o superior
- Visual Studio Code (VS Code)
- Extensión de Python instalada en VS Code

 Instalación de librerías necesarias
--------------------------------------
Abre una terminal (o consola) en VS Code (usualmente powershell desde windows) y ejecuta los siguientes comandos para instalar las librerías requeridas:

    pip install networkx
    pip install matplotlib

Archivos principales
-----------------------
- main.py – Código fuente del proyecto
- grafo_todos_algoritmos.png – Imagen generada con los resultados (se crea al ejecutar el código)

Cómo ejecutar el proyecto en Visual Studio Code
---------------------------------------------------
1. Abre Visual Studio Code.
2. Crea una carpeta nueva o selecciona la que se encuentra aquí y guarda allí el archivo `main.py`.
3. Abre la carpeta desde Visual Studio Code.
4. Abre el archivo `main.py`.
5. Haz clic en el botón "Run Python File" o presiona F5 para ejecutar.
6. El programa te preguntara si el grafo es dirijido o no, y despues pedirá que ingreses una matriz de adyacencia:
   - Primero te preguntará cuántos nodos tendrá el grafo.
   - Luego ingresarás cada fila de la matriz, separando los valores con espacios.
7. Al finalizar, se generará una imagen llamada `grafo_todos_algoritmos.png` con los resultados de los algoritmos.

 Salida del programa
-----------------------
- Se mostrará una única ventana con 8 subgrafos.
- Cada uno corresponde a un algoritmo: Prim, Kruskal, Dijkstra, BFS, DFS, Hamiltoniano, Euleriano y coloración.
- En cada subgrafo se indicará el peso total de las aristas y los nodos tocados.


Anuncio
---------------

Este código puede tener errores debió a la falta de experiencia de este lenguaje
