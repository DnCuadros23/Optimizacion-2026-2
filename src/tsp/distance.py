"""Matriz de distancias con redondeo TSPLIB y costo de una ruta L(π)."""
import numpy as np


def matriz_distancias(coords: np.ndarray) -> np.ndarray:
    """Matriz de distancias EUC_2D con redondeo TSPLIB: int(sqrt(dx**2+dy**2)+0.5)."""
    diff = coords[:, None, :] - coords[None, :, :]
    distancias = np.sqrt((diff ** 2).sum(axis=2))
    return (distancias + 0.5).astype(int)


def tour_length(tour, D: np.ndarray) -> int:
    """Costo L(π) de la ruta: suma de distancias consecutivas más el regreso al origen."""
    tour = np.asarray(tour)
    siguiente = np.roll(tour, -1)
    return int(D[tour, siguiente].sum())
