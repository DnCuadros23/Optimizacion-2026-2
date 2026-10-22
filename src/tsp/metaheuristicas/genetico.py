"""Algoritmo genético con cruce OX (Order Crossover) para el TSP.

Idea: una población de N rutas evoluciona por generaciones. En cada
generación se eligen padres por torneo, se cruzan (con probabilidad p_c)
para armar hijos, se los muta un poco (con probabilidad p_m), y los mejores
individuos (élite) pasan directo a la siguiente generación sin tocarlos.

Parámetros (nombres del informe):
    N       tamaño de la población.
    p_c     probabilidad de cruce.
    p_m     probabilidad de mutación.
    G_max   número de generaciones.
    e       cantidad de individuos élite que se preservan sin cambios.
"""
import random

from tsp.datos import longitud_ruta


def _poblacion_inicial(n, N, rng):
    """N rutas al azar, cada una una permutación de las n ciudades."""
    base = list(range(n))
    poblacion = []
    for _ in range(N):
        individuo = base[:]
        rng.shuffle(individuo)
        poblacion.append(individuo)
    return poblacion


def _evaluar(poblacion, D):
    """Costo L(π) y aptitud f=1/L(π) de cada individuo de la población."""
    costos = [longitud_ruta(individuo, D) for individuo in poblacion]
    aptitudes = [1.0 / costo for costo in costos]
    return costos, aptitudes


def _seleccion_por_torneo(poblacion, aptitudes, k, rng):
    """Elige k individuos al azar de la población y devuelve el de mejor aptitud."""
    indices = rng.sample(range(len(poblacion)), k)
    mejor = max(indices, key=lambda i: aptitudes[i])
    return list(poblacion[mejor])


def _cruce_ox(padre1, padre2, rng):
    """Cruce OX (Order Crossover): copia un tramo de padre1 y completa el resto con el orden de padre2."""
    n = len(padre1)
    i, j = sorted(rng.sample(range(n), 2))

    hijo = [None] * n
    hijo[i:j + 1] = padre1[i:j + 1]
    usados = set(hijo[i:j + 1])

    posiciones_libres = [pos for pos in range(n) if hijo[pos] is None]
    orden_de_padre2 = [ciudad for ciudad in padre2 if ciudad not in usados]

    for pos, ciudad in zip(posiciones_libres, orden_de_padre2):
        hijo[pos] = ciudad

    return hijo


def _mutacion(ruta, p_m, rng):
    """Con probabilidad p_m, muta la ruta por intercambio o por inversión de un tramo (al azar cuál)."""
    if rng.random() >= p_m:
        return list(ruta)

    n = len(ruta)
    i, j = sorted(rng.sample(range(n), 2))
    ruta = list(ruta)

    if rng.random() < 0.5:
        ruta[i], ruta[j] = ruta[j], ruta[i]  # intercambio de dos ciudades
    else:
        ruta[i:j + 1] = reversed(ruta[i:j + 1])  # inversión del tramo entre ellas

    return ruta


def genetico(n, D, N=150, p_c=0.9, p_m=0.05, G_max=500, e=3, semilla=0):
    """Busca una ruta corta con un algoritmo genético. Devuelve (mejor_ruta, mejor_costo, historial)."""
    rng = random.Random(semilla)
    poblacion = _poblacion_inicial(n, N, rng)
    costos, aptitudes = _evaluar(poblacion, D)

    mejor_idx = min(range(N), key=lambda i: costos[i])
    mejor_ruta, mejor_costo = list(poblacion[mejor_idx]), costos[mejor_idx]
    historial = [mejor_costo]

    for _ in range(G_max):
        # élite: los e mejores de esta generación pasan directo, sin cruce ni mutación
        orden_por_costo = sorted(range(N), key=lambda i: costos[i])
        nueva_poblacion = [list(poblacion[i]) for i in orden_por_costo[:e]]

        while len(nueva_poblacion) < N:
            padre1 = _seleccion_por_torneo(poblacion, aptitudes, k=3, rng=rng)
            padre2 = _seleccion_por_torneo(poblacion, aptitudes, k=3, rng=rng)

            hijo = _cruce_ox(padre1, padre2, rng) if rng.random() < p_c else padre1
            hijo = _mutacion(hijo, p_m, rng)
            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion
        costos, aptitudes = _evaluar(poblacion, D)

        mejor_idx = min(range(N), key=lambda i: costos[i])
        if costos[mejor_idx] < mejor_costo:
            mejor_costo = costos[mejor_idx]
            mejor_ruta = list(poblacion[mejor_idx])

        historial.append(mejor_costo)

    return mejor_ruta, mejor_costo, historial
