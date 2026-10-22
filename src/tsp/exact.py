"""Métodos exactos para el TSP: fuerza bruta y Held-Karp.

Ambos garantizan el óptimo, pero crecen muy rápido con n (fuerza bruta
prueba (n-1)! rutas; Held-Karp usa n^2 * 2^n). Por eso en este proyecto
solo se usan para validar subconjuntos chicos (hasta 12 ciudades), nunca
sobre berlin52 o eil51 completos.
"""
import itertools

import numpy as np


def fuerza_bruta(D: np.ndarray):
    """Revisa las (n-1)! rutas que fijan la ciudad 0 al inicio y devuelve la mejor (ruta, costo)."""
    n = D.shape[0]
    mejor_ruta = None
    mejor_costo = None

    for resto in itertools.permutations(range(1, n)):
        # costo de 0 -> resto[0] -> ... -> resto[-1] -> 0 (regreso al origen incluido)
        costo = D[0, resto[0]]
        for a, b in zip(resto, resto[1:]):
            costo += D[a, b]
        costo += D[resto[-1], 0]

        if mejor_costo is None or costo < mejor_costo:
            mejor_costo = costo
            mejor_ruta = (0,) + resto

    return list(mejor_ruta), int(mejor_costo)


def held_karp(D: np.ndarray):
    """Programación dinámica con bitmask: óptimo exacto en tiempo n^2 * 2^n. Devuelve (ruta, costo)."""
    n = D.shape[0]
    n_subconjuntos = 1 << n
    INF = float("inf")

    # dp[mascara][j] = costo mínimo para visitar exactamente las ciudades de "mascara"
    # (siempre incluye a la ciudad 0) terminando en la ciudad j
    dp = np.full((n_subconjuntos, n), INF)
    padre = np.full((n_subconjuntos, n), -1, dtype=int)
    dp[1][0] = 0.0  # mascara = {0}, terminar en 0, costo 0

    for mascara in range(n_subconjuntos):
        if not (mascara & 1):
            continue  # toda ruta parte de la ciudad 0, así que 0 siempre debe estar incluida
        for j in range(n):
            if not (mascara & (1 << j)) or dp[mascara][j] == INF:
                continue
            costo_hasta_j = dp[mascara][j]
            for k in range(n):
                if mascara & (1 << k):
                    continue  # k ya fue visitada en esta mascara
                nueva_mascara = mascara | (1 << k)
                nuevo_costo = costo_hasta_j + D[j, k]
                if nuevo_costo < dp[nueva_mascara][k]:
                    dp[nueva_mascara][k] = nuevo_costo
                    padre[nueva_mascara][k] = j

    mascara_completa = n_subconjuntos - 1
    mejor_costo = INF
    mejor_final = -1
    for j in range(1, n):
        costo = dp[mascara_completa][j] + D[j, 0]
        if costo < mejor_costo:
            mejor_costo = costo
            mejor_final = j

    # se reconstruye la ruta siguiendo los punteros "padre" desde la última ciudad hacia atrás
    ruta = []
    mascara, j = mascara_completa, mejor_final
    while j != -1:
        ruta.append(j)
        j_anterior = padre[mascara][j]
        mascara ^= (1 << j)
        j = j_anterior
    ruta.reverse()

    return ruta, int(mejor_costo)
