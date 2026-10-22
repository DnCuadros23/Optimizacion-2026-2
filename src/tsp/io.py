"""Lector de archivos TSPLIB (formato EUC_2D, NODE_COORD_SECTION).

Un archivo .tsp trae primero un encabezado con metadatos (NAME, DIMENSION,
EDGE_WEIGHT_TYPE) y después la sección NODE_COORD_SECTION, con una línea
"índice  x  y" por ciudad. Aquí solo se soporta EUC_2D (coordenadas en el
plano, distancia euclidiana), que es el tipo de berlin52 y eil51.
"""
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class Instancia:
    """Una instancia del TSP ya parseada: nombre, número de ciudades (n) y sus coordenadas (el conjunto V)."""
    nombre: str
    dimension: int  # n: cantidad de ciudades de la instancia
    coords: np.ndarray  # shape (n, 2); fila i = coordenadas (x, y) de la ciudad i, en el orden del archivo


def leer_tsp(ruta) -> Instancia:
    """Lee un archivo TSPLIB EUC_2D y devuelve su nombre, su dimensión (n) y sus coordenadas."""
    ruta = Path(ruta)
    nombre = None
    dimension = None
    tipo_peso = None
    coords: dict[int, tuple[float, float]] = {}
    en_coords = False  # True una vez que ya se pasó la línea NODE_COORD_SECTION

    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            if linea == "NODE_COORD_SECTION":
                en_coords = True
                continue
            if linea == "EOF":
                break
            if en_coords:
                # cada línea de esta sección trae: índice de la ciudad, x, y
                partes = linea.split()
                idx = int(partes[0])
                coords[idx] = (float(partes[1]), float(partes[2]))
                continue
            # antes de NODE_COORD_SECTION: líneas de metadatos tipo "CLAVE: valor"
            if ":" in linea:
                clave, valor = (p.strip() for p in linea.split(":", 1))
                if clave == "NAME":
                    nombre = valor
                elif clave == "DIMENSION":
                    dimension = int(valor)
                elif clave == "EDGE_WEIGHT_TYPE":
                    tipo_peso = valor

    if tipo_peso != "EUC_2D":
        raise ValueError(f"Tipo de distancia no soportado: {tipo_peso!r} (este parser solo lee EUC_2D)")
    if dimension is None or len(coords) != dimension:
        raise ValueError(
            f"DIMENSION ({dimension}) no coincide con el número de coordenadas leídas ({len(coords)}) en {ruta}"
        )

    # se ordena por índice de ciudad para que coords[i] corresponda siempre a la ciudad i
    ordenados = np.array([coords[i] for i in sorted(coords)], dtype=float)
    return Instancia(nombre=nombre, dimension=dimension, coords=ordenados)
