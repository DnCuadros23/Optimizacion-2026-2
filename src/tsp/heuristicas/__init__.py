"""Heurísticas (sección 3.2 del informe): vecino más cercano y 2-opt."""
from .dos_opt import dos_opt
from .vecino_cercano import vecino_mas_cercano

__all__ = ["vecino_mas_cercano", "dos_opt"]
