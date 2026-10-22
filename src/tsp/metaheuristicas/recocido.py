"""Recocido simulado (Simulated Annealing) con vecindad 2-opt.

Idea del algoritmo: a diferencia de 2-opt (que solo acepta movimientos que
mejoran), el recocido también acepta movimientos que empeoran, con una
probabilidad que depende de la temperatura T. Al principio T es alta y casi
cualquier empeoramiento se acepta (para no quedarse atascado en un óptimo
local); a medida que T baja, el algoritmo se vuelve cada vez más exigente,
hasta terminar pareciéndose a 2-opt puro.

Parámetros (nombres del informe):
    T0          temperatura inicial.
    alpha_cool  factor de enfriamiento: en cada paso, T <- alpha_cool * T.
    T_min       temperatura a la que se detiene la búsqueda.
    L_iter      cuántos movimientos se intentan en cada nivel de temperatura.
"""
import math
import random

from tsp.datos import longitud_ruta


def _movimiento_aleatorio(ruta, D, rng):
    """Elige al azar dos aristas de la ruta y calcula Δ de invertir el tramo entre ellas.

    Es el mismo movimiento de 2-opt (src/tsp/heuristicas/dos_opt.py), solo que
    aquí se elige una pareja de aristas al azar en vez de buscar la mejor.
    """
    n = len(ruta)
    while True:
        i, j = sorted(rng.sample(range(n), 2))
        if i == 0 and j == n - 1:
            continue  # aristas adyacentes por el cierre del ciclo: no es un movimiento válido
        break

    a, b = ruta[i], ruta[i + 1]
    c, d = ruta[j], ruta[(j + 1) % n]
    delta = D[a, c] + D[b, d] - D[a, b] - D[c, d]
    return i, j, int(delta)


def calcular_T0(ruta_inicial, D, fraccion_aceptada=0.8, muestras=200, semilla=0):
    """Calcula T0 para que, al empezar, se acepte en promedio 'fraccion_aceptada' de los movimientos que empeoran.

    Se muestrean movimientos aleatorios desde la ruta inicial, se promedia el
    Δ de los que empeoran (Δ>0), y se despeja T0 de exp(-Δ_prom / T0) = fraccion_aceptada.
    """
    rng = random.Random(semilla)
    ruta = list(ruta_inicial)
    deltas_que_empeoran = []

    while len(deltas_que_empeoran) < muestras:
        _, _, delta = _movimiento_aleatorio(ruta, D, rng)
        if delta > 0:
            deltas_que_empeoran.append(delta)

    delta_promedio = sum(deltas_que_empeoran) / len(deltas_que_empeoran)
    return -delta_promedio / math.log(fraccion_aceptada)


def recocido_simulado(ruta_inicial, D, T0, alpha_cool=0.995, T_min=1e-3, L_iter=100, semilla=0):
    """Mejora una ruta con recocido simulado. Devuelve (mejor_ruta, mejor_costo, historial).

    'historial' guarda el mejor costo encontrado hasta cada nivel de
    temperatura (no por cada movimiento individual, para que la lista sirva
    para graficar la convergencia en la fase 8 sin quedar enorme).
    """
    rng = random.Random(semilla)
    ruta = list(ruta_inicial)
    costo = longitud_ruta(ruta, D)
    mejor_ruta, mejor_costo = list(ruta), costo
    historial = [mejor_costo]

    T = T0
    while T > T_min:
        for _ in range(L_iter):
            i, j, delta = _movimiento_aleatorio(ruta, D, rng)

            # se acepta si mejora (Δ<=0), o si empeora pero la "suerte" cae
            # dentro de la probabilidad exp(-Δ/T) que da la temperatura actual
            if delta <= 0 or rng.random() < math.exp(-delta / T):
                ruta[i + 1:j + 1] = reversed(ruta[i + 1:j + 1])
                costo += delta
                if costo < mejor_costo:
                    mejor_costo = costo
                    mejor_ruta = list(ruta)

        historial.append(mejor_costo)
        T *= alpha_cool  # enfriamiento geométrico

    return mejor_ruta, mejor_costo, historial
