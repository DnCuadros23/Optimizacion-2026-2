"""Calibración de parámetros (fase 6, sección 5.1 del informe).

Para cada metaheurística se varía UN parámetro a la vez (bajo/medio/alto),
dejando el resto en su configuración base (la misma de la fase 4/5), con
10 semillas por nivel. Así se ve el efecto de cada parámetro por separado,
sin mezclarlo con el de los demás.
"""
import time

from tsp.heuristicas import vecino_mas_cercano
from tsp.metaheuristicas import genetico, hormigas, recocido_simulado

SEMILLAS = range(10)
NIVELES = ["bajo", "medio", "alto"]

# mismas configuraciones base usadas en la fase 4 y la fase 5
BASE_RECOCIDO = dict(alpha_cool=0.995, T_min=1e-3, L_iter=500)
BASE_GENETICO = dict(N=150, p_c=0.9, p_m=0.05, G_max=500, e=3)
BASE_HORMIGAS = dict(m=None, alpha=1, beta=3, rho=0.3, Q=100, t_max=100)


def _filas(instancia, optimo, metodo, parametro, corridas):
    """corridas: lista de (nivel, valor, semilla, costo, tiempo) -> filas para el CSV."""
    return [
        {
            "instance": instancia, "metodo": metodo, "parametro": parametro,
            "nivel": nivel, "valor": valor, "seed": semilla,
            "length": costo, "gap_pct": round((costo - optimo) / optimo * 100, 2),
            "time_s": round(tiempo, 4),
        }
        for nivel, valor, semilla, costo, tiempo in corridas
    ]


def calibrar_recocido_T0(D, instancia, optimo, valores_T0):
    """Varía T0 (temperatura inicial), con alpha_cool/T_min/L_iter fijos en la base."""
    ruta_inicial = vecino_mas_cercano(D, inicio=0)
    corridas = []
    for nivel, valor in zip(NIVELES, valores_T0):
        for semilla in SEMILLAS:
            t0 = time.perf_counter()
            _, costo, _ = recocido_simulado(ruta_inicial, D, T0=valor, semilla=semilla, **BASE_RECOCIDO)
            corridas.append((nivel, valor, semilla, costo, time.perf_counter() - t0))
    return _filas(instancia, optimo, "recocido_simulado", "T0", corridas)


def calibrar_recocido_alpha_cool(D, instancia, optimo, valores_alpha, T0_fijo):
    """Varía alpha_cool (velocidad de enfriamiento), con T0/T_min/L_iter fijos en la base."""
    ruta_inicial = vecino_mas_cercano(D, inicio=0)
    corridas = []
    for nivel, valor in zip(NIVELES, valores_alpha):
        params = {**BASE_RECOCIDO, "alpha_cool": valor}
        for semilla in SEMILLAS:
            t0 = time.perf_counter()
            _, costo, _ = recocido_simulado(ruta_inicial, D, T0=T0_fijo, semilla=semilla, **params)
            corridas.append((nivel, valor, semilla, costo, time.perf_counter() - t0))
    return _filas(instancia, optimo, "recocido_simulado", "alpha_cool", corridas)


def calibrar_genetico(n, D, instancia, optimo, parametro, valores):
    """Varía un parámetro del genético (N o p_m), con el resto fijo en la base."""
    corridas = []
    for nivel, valor in zip(NIVELES, valores):
        params = {**BASE_GENETICO, parametro: valor}
        for semilla in SEMILLAS:
            t0 = time.perf_counter()
            _, costo, _ = genetico(n, D, semilla=semilla, **params)
            corridas.append((nivel, valor, semilla, costo, time.perf_counter() - t0))
    return _filas(instancia, optimo, "genetico", parametro, corridas)


def calibrar_hormigas(n, D, instancia, optimo, parametro, valores):
    """Varía un parámetro de la colonia de hormigas (rho o beta), con el resto fijo en la base."""
    corridas = []
    for nivel, valor in zip(NIVELES, valores):
        params = {**BASE_HORMIGAS, parametro: valor}
        for semilla in SEMILLAS:
            t0 = time.perf_counter()
            _, costo, _ = hormigas(n, D, semilla=semilla, **params)
            corridas.append((nivel, valor, semilla, costo, time.perf_counter() - t0))
    return _filas(instancia, optimo, "hormigas", parametro, corridas)
