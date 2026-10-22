"""Lector de archivos TSPLIB (formato EUC_2D, NODE_COORD_SECTION)."""
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class Instancia:
    """Instancia TSP: nombre, dimensión y coordenadas (x, y) de cada ciudad."""
    nombre: str
    dimension: int
    coords: np.ndarray  # shape (n, 2), ordenadas según el índice del archivo


def leer_tsp(ruta) -> Instancia:
    """Parsea un archivo TSPLIB EUC_2D y devuelve nombre, dimensión y coordenadas."""
    ruta = Path(ruta)
    nombre = None
    dimension = None
    tipo_peso = None
    coords: dict[int, tuple[float, float]] = {}
    en_coords = False

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
                partes = linea.split()
                idx = int(partes[0])
                coords[idx] = (float(partes[1]), float(partes[2]))
                continue
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

    ordenados = np.array([coords[i] for i in sorted(coords)], dtype=float)
    return Instancia(nombre=nombre, dimension=dimension, coords=ordenados)
