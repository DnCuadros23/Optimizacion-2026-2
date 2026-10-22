"""Matriz de distancias (d_ij) con redondeo TSPLIB y costo L(π) de una ruta."""
import numpy as np


def matriz_distancias(coords: np.ndarray) -> np.ndarray:
    """Construye d_ij: distancia euclidiana entre cada par de ciudades, redondeada como en TSPLIB."""
    # diff[i, j] = coords[i] - coords[j], para las dos coordenadas (x, y) a la vez
    diff = coords[:, None, :] - coords[None, :, :]
    distancias = np.sqrt((diff ** 2).sum(axis=2))
    # TSPLIB redondea al entero más cercano (no trunca): int(dist + 0.5)
    return (distancias + 0.5).astype(int)


def longitud_ruta(ruta, D: np.ndarray) -> int:
    """Calcula L(π): la distancia total de la ruta, incluyendo el regreso a la primera ciudad."""
    ruta = np.asarray(ruta)
    # "siguiente" recorre la ruta desplazada una posición, así la última ciudad
    # queda emparejada con la primera y el regreso al origen entra en la suma
    siguiente = np.roll(ruta, -1)
    return int(D[ruta, siguiente].sum())
