"""Pruebas de la colonia de hormigas (Ant System)."""
import random

import numpy as np

from tsp.datos import leer_tsp, longitud_ruta, matriz_distancias
from tsp.metaheuristicas import hormigas
from tsp.metaheuristicas.hormigas import _construir_ruta, _matriz_eta, _probabilidades


def test_probabilidad_con_tau_uniforme_es_proporcional_a_eta_beta():
    # con tau igual para todas las ciudades, tau^alpha es una constante que se
    # cancela al normalizar: lo unico que debe quedar es eta^beta
    tau_fila = np.array([1.0, 1.0, 1.0, 1.0])
    eta_fila = np.array([0.5, 0.2, 0.1, 0.0])  # eta_fila[0] no se usa (ciudad actual)
    candidatos = [1, 2, 3]
    beta = 2

    probs = _probabilidades(tau_fila, eta_fila, candidatos, alpha=1, beta=beta)

    esperado = eta_fila[candidatos] ** beta
    esperado = esperado / esperado.sum()
    assert np.allclose(probs, esperado)


def test_construir_ruta_devuelve_una_permutacion_valida(data_dir):
    inst = leer_tsp(data_dir / "berlin52.tsp")
    D = matriz_distancias(inst.coords)
    n = D.shape[0]
    eta = _matriz_eta(D)
    tau = np.ones((n, n))

    ruta = _construir_ruta(tau, eta, alpha=1, beta=3, rng=random.Random(0))
    assert sorted(ruta) == list(range(n))


def test_hormigas_devuelve_una_permutacion_valida(data_dir):
    inst = leer_tsp(data_dir / "berlin52.tsp")
    D = matriz_distancias(inst.coords)
    mejor_ruta, _, _ = hormigas(D.shape[0], D, m=10, t_max=5, semilla=0)
    assert sorted(mejor_ruta) == list(range(D.shape[0]))


def test_hormigas_es_reproducible_con_la_misma_semilla(data_dir):
    inst = leer_tsp(data_dir / "berlin52.tsp")
    D = matriz_distancias(inst.coords)
    _, costo_1, _ = hormigas(D.shape[0], D, m=10, t_max=5, semilla=3)
    _, costo_2, _ = hormigas(D.shape[0], D, m=10, t_max=5, semilla=3)
    assert costo_1 == costo_2


def test_hormigas_mejora_claramente_una_ruta_al_azar(data_dir):
    inst = leer_tsp(data_dir / "berlin52.tsp")
    D = matriz_distancias(inst.coords)
    n = D.shape[0]

    rng = random.Random(1)
    ruta_aleatoria = list(range(n))
    rng.shuffle(ruta_aleatoria)
    costo_aleatorio = longitud_ruta(ruta_aleatoria, D)

    _, mejor_costo, historial = hormigas(n, D, m=n, t_max=50, semilla=1)

    assert mejor_costo < costo_aleatorio
    assert historial[0] >= historial[-1]  # el mejor-hasta-ahora nunca empeora
