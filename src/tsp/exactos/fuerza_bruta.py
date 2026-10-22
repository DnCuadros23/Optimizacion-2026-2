"""Fuerza bruta: revisa TODAS las rutas posibles. Garantiza el óptimo, pero
crece como (n-1)! — por eso solo se usa aquí para validar subconjuntos muy
chicos (hasta 10 ciudades), nunca sobre berlin52 o eil51 completos.
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
