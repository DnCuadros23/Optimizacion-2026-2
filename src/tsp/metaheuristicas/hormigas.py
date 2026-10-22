"""Colonia de hormigas / Ant System para el TSP.

Idea: m hormigas construyen, cada una, una ruta completa. En cada paso
eligen la siguiente ciudad al azar, pero con más probabilidad hacia las
ciudades con más feromona (τ, lo que "recomiendan" las hormigas anteriores)
y más cercanas (η = 1/distancia). Al final de cada ronda se evapora un poco
de feromona y se refuerzan las aristas que usaron las rutas más cortas.

Parámetros (nombres del informe):
    m       número de hormigas (por defecto, una por ciudad: m=n).
    alpha   cuánto pesa la feromona (τ) al elegir la siguiente ciudad.
    beta    cuánto pesa la cercanía (η=1/d) al elegir la siguiente ciudad.
    rho     fracción de feromona que se evapora en cada ronda.
    Q       feromona total que deposita cada hormiga, repartida en su ruta.
    t_max   número de rondas.
"""
import random

import numpy as np

from tsp.datos import longitud_ruta


def _matriz_eta(D):
    """η_ij = 1/d_ij: qué tan atractiva es cada arista por cercanía (η_ii se deja en 0, no se usa)."""
    D_sin_diagonal = D.astype(float).copy()
    np.fill_diagonal(D_sin_diagonal, np.inf)  # evita dividir por 0 en la diagonal
    return 1.0 / D_sin_diagonal


def _probabilidades(tau_fila, eta_fila, candidatos, alpha, beta):
    """Probabilidad de ir a cada ciudad de 'candidatos' desde la ciudad actual: ∝ τ^alpha · η^beta."""
    pesos = (tau_fila[candidatos] ** alpha) * (eta_fila[candidatos] ** beta)
    return pesos / pesos.sum()


def _construir_ruta(tau, eta, alpha, beta, rng):
    """Una hormiga recorre todas las ciudades, eligiendo cada paso al azar según las probabilidades."""
    n = tau.shape[0]
    ruta = [0]
    no_visitadas = list(range(1, n))
    actual = 0

    while no_visitadas:
        probs = _probabilidades(tau[actual], eta[actual], no_visitadas, alpha, beta)
        siguiente = rng.choices(no_visitadas, weights=list(probs))[0]
        ruta.append(siguiente)
        no_visitadas.remove(siguiente)
        actual = siguiente

    return ruta


def _actualizar_feromona(tau, rutas, costos, rho, Q):
    """Evapora una fracción rho de feromona y refuerza las aristas de cada ruta con Q/costo (matriz simétrica)."""
    tau = tau * (1 - rho)
    for ruta, costo in zip(rutas, costos):
        aporte = Q / costo
        aristas = zip(ruta, ruta[1:] + ruta[:1])  # incluye el regreso de la última ciudad a la primera
        for a, b in aristas:
            tau[a, b] += aporte
            tau[b, a] += aporte
    return tau


def hormigas(n, D, m=None, alpha=1, beta=3, rho=0.3, Q=100, t_max=100, semilla=0):
    """Busca una ruta corta con colonia de hormigas. Devuelve (mejor_ruta, mejor_costo, historial)."""
    rng = random.Random(semilla)
    m = n if m is None else m

    eta = _matriz_eta(D)
    tau = np.ones((n, n))  # feromona inicial uniforme: al principio solo manda la cercania (eta)

    mejor_ruta, mejor_costo = None, None
    historial = []

    for _ in range(t_max):
        rutas = [_construir_ruta(tau, eta, alpha, beta, rng) for _ in range(m)]
        costos = [longitud_ruta(ruta, D) for ruta in rutas]

        idx_mejor = min(range(m), key=lambda i: costos[i])
        if mejor_costo is None or costos[idx_mejor] < mejor_costo:
            mejor_costo = costos[idx_mejor]
            mejor_ruta = list(rutas[idx_mejor])

        tau = _actualizar_feromona(tau, rutas, costos, rho, Q)
        historial.append(mejor_costo)

    return mejor_ruta, mejor_costo, historial
