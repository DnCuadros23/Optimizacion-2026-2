"""Heurísticas para el TSP: vecino más cercano (construye una ruta) y 2-opt (la mejora).

A diferencia de fuerza bruta y Held-Karp, no garantizan el óptimo, pero
corren en tiempo razonable sobre instancias grandes como berlin52.
"""
import numpy as np


def nearest_neighbor(D: np.ndarray, start: int = 0):
    """Construye una ruta greedy: desde la ciudad actual salta siempre a la más cercana sin visitar.

    Si hay un empate de distancia, gana la ciudad de menor índice (desempate determinista).
    """
    n = D.shape[0]
    visitada = [False] * n
    visitada[start] = True
    ruta = [start]
    actual = start

    for _ in range(n - 1):
        siguiente = min((c for c in range(n) if not visitada[c]), key=lambda c: D[actual, c])
        ruta.append(siguiente)
        visitada[siguiente] = True
        actual = siguiente

    return ruta


def two_opt(tour, D: np.ndarray):
    """Mejora local 2-opt con estrategia de primera mejora (first improvement).

    Para cada par de aristas (a,b) y (c,d) de la ruta, invertir el tramo entre
    ellas cambia el costo en Δ = d(a,c) + d(b,d) − d(a,b) − d(c,d). En cuanto
    se encuentra un Δ<0 se aplica de inmediato y se reinicia el barrido; el
    resultado es un óptimo local: ninguna de esas inversiones ya mejora la ruta.
    """
    ruta = list(tour)
    n = len(ruta)
    hay_mejora = True

    while hay_mejora:
        hay_mejora = False
        for i in range(n - 1):
            a, b = ruta[i], ruta[i + 1]
            for j in range(i + 2, n):
                c, d = ruta[j], ruta[(j + 1) % n]
                if d == a:
                    continue  # aristas adyacentes (comparten la ciudad a): no es un movimiento 2-opt válido
                delta = D[a, c] + D[b, d] - D[a, b] - D[c, d]
                if delta < 0:
                    ruta[i + 1:j + 1] = reversed(ruta[i + 1:j + 1])
                    hay_mejora = True
                    break  # primera mejora: se aplica el cambio y se reinicia el barrido
            if hay_mejora:
                break

    return ruta
