"""Lectura de instancias TSPLIB y cálculo de distancias (sección 5.2 del informe: función de costo)."""
from .distancias import longitud_ruta, matriz_distancias
from .lector_tsp import Instancia, leer_tsp

__all__ = ["Instancia", "leer_tsp", "matriz_distancias", "longitud_ruta"]
