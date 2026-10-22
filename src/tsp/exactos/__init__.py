"""Métodos exactos (sección 3.1 del informe): fuerza bruta y Held-Karp. Solo para subconjuntos chicos."""
from .fuerza_bruta import fuerza_bruta
from .held_karp import held_karp

__all__ = ["fuerza_bruta", "held_karp"]
