"""Vecino más cercano: construye una ruta rápido, pero sin garantía de ser la mejor."""
import numpy as np


def vecino_mas_cercano(D: np.ndarray, inicio: int = 0):
    """Desde la ciudad actual salta siempre a la más cercana sin visitar (empate -> menor índice)."""
    n = D.shape[0]
    visitada = [False] * n
    visitada[inicio] = True
    ruta = [inicio]
    actual = inicio

    for _ in range(n - 1):
        siguiente = min((c for c in range(n) if not visitada[c]), key=lambda c: D[actual, c])
        ruta.append(siguiente)
        visitada[siguiente] = True
        actual = siguiente

    return ruta
