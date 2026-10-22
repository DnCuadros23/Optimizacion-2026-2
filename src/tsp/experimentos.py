"""Corre varios algoritmos sobre una instancia y junta los resultados para compararlos.

Regla de presupuesto (hay que elegir una y documentarla; esta es la elegida):
NN y NN+2-opt son deterministicos, se corren una sola vez. Las tres
metaheuristicas se corren con el mismo orden de tiempo por corrida (unos
pocos segundos) fijando los mismos parametros de partida que se usaron y
validaron en la fase 4 (PARAMS_RECOCIDO/GENETICO/HORMIGAS); el tiempo real
de cada corrida queda en la columna time_s para poder comprobarlo.
"""
import time

import pandas as pd

from tsp.datos import longitud_ruta
from tsp.heuristicas import dos_opt, vecino_mas_cercano
from tsp.metaheuristicas import calcular_T0, genetico, hormigas, recocido_simulado

# mismos parametros de partida usados (y ya probados) en los ejecutables de la fase 4
PARAMS_RECOCIDO = dict(alpha_cool=0.995, T_min=1e-3, L_iter=500)
PARAMS_GENETICO = dict(N=150, p_c=0.9, p_m=0.05, G_max=500, e=3)
PARAMS_HORMIGAS = dict(m=None, alpha=1, beta=3, rho=0.3, Q=100, t_max=100)


def _corrida_nn(D):
    """Una corrida de vecino mas cercano. Devuelve (longitud, tiempo_s, historial=None: no aplica)."""
    t0 = time.perf_counter()
    ruta = vecino_mas_cercano(D, inicio=0)
    tiempo = time.perf_counter() - t0
    return longitud_ruta(ruta, D), tiempo, None


def _corrida_nn_2opt(D):
    """Una corrida de vecino mas cercano + 2-opt."""
    t0 = time.perf_counter()
    ruta = dos_opt(vecino_mas_cercano(D, inicio=0), D)
    tiempo = time.perf_counter() - t0
    return longitud_ruta(ruta, D), tiempo, None


def _corrida_recocido(D, semilla, params):
    """Una corrida de recocido simulado, partiendo de vecino mas cercano."""
    ruta_inicial = vecino_mas_cercano(D, inicio=0)
    T0 = calcular_T0(ruta_inicial, D, semilla=semilla)
    t0 = time.perf_counter()
    _, costo, historial = recocido_simulado(ruta_inicial, D, T0=T0, semilla=semilla, **params)
    tiempo = time.perf_counter() - t0
    return costo, tiempo, historial


def _corrida_genetico(n, D, semilla, params):
    """Una corrida del algoritmo genetico."""
    t0 = time.perf_counter()
    _, costo, historial = genetico(n, D, semilla=semilla, **params)
    tiempo = time.perf_counter() - t0
    return costo, tiempo, historial


def _corrida_hormigas(n, D, semilla, params):
    """Una corrida de la colonia de hormigas."""
    t0 = time.perf_counter()
    _, costo, historial = hormigas(n, D, semilla=semilla, **params)
    tiempo = time.perf_counter() - t0
    return costo, tiempo, historial


def ejecutar_experimentos(
    instancia, D, optimo, semillas=range(30),
    params_recocido=None, params_genetico=None, params_hormigas=None,
):
    """Corre NN y NN+2-opt una vez, y recocido/genetico/hormigas con cada semilla.

    Devuelve dos DataFrames: 'runs' (una fila por corrida, columnas instance,
    algo, config_id, seed, length, gap_pct, time_s) e 'historiales' (una fila
    por iteracion de cada corrida, para graficar la convergencia en la fase 8).
    """
    params_recocido = PARAMS_RECOCIDO if params_recocido is None else params_recocido
    params_genetico = PARAMS_GENETICO if params_genetico is None else params_genetico
    params_hormigas = PARAMS_HORMIGAS if params_hormigas is None else params_hormigas

    n = D.shape[0]
    filas, historiales = [], []

    def agregar(algo, semilla, costo, tiempo, historial):
        filas.append({
            "instance": instancia,
            "algo": algo,
            "config_id": "base",
            "seed": semilla,
            "length": costo,
            "gap_pct": round((costo - optimo) / optimo * 100, 2),
            "time_s": round(tiempo, 4),
        })
        if historial is not None:
            for iteracion, mejor_costo in enumerate(historial):
                historiales.append({
                    "instance": instancia, "algo": algo, "seed": semilla,
                    "iteracion": iteracion, "mejor_costo": mejor_costo,
                })

    costo, tiempo, _ = _corrida_nn(D)
    agregar("nearest_neighbor", None, costo, tiempo, None)

    costo, tiempo, _ = _corrida_nn_2opt(D)
    agregar("nearest_neighbor+2opt", None, costo, tiempo, None)

    for semilla in semillas:
        costo, tiempo, historial = _corrida_recocido(D, semilla, params_recocido)
        agregar("recocido_simulado", semilla, costo, tiempo, historial)

        costo, tiempo, historial = _corrida_genetico(n, D, semilla, params_genetico)
        agregar("genetico", semilla, costo, tiempo, historial)

        costo, tiempo, historial = _corrida_hormigas(n, D, semilla, params_hormigas)
        agregar("hormigas", semilla, costo, tiempo, historial)

    return pd.DataFrame(filas), pd.DataFrame(historiales)


def resumen_por_algoritmo(runs_df, optimo):
    """Por cada algoritmo: mejor longitud, media, desviación estándar y sus gaps contra el óptimo."""
    resumen = runs_df.groupby("algo")["length"].agg(mejor="min", media="mean", desviacion="std").reset_index()
    resumen["desviacion"] = resumen["desviacion"].fillna(0.0)  # NN y NN+2opt solo tienen 1 corrida
    resumen["gap_mejor_pct"] = round((resumen["mejor"] - optimo) / optimo * 100, 2)
    resumen["gap_medio_pct"] = round((resumen["media"] - optimo) / optimo * 100, 2)
    return resumen
