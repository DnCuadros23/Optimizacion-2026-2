"""Pruebas del algoritmo genetico: cruce y mutacion siempre deben dar permutaciones validas."""
import random

from tsp.datos import leer_tsp, matriz_distancias
from tsp.metaheuristicas import genetico
from tsp.metaheuristicas.genetico import _cruce_ox, _mutacion, _poblacion_inicial


def test_poblacion_inicial_son_permutaciones_validas():
    rng = random.Random(0)
    poblacion = _poblacion_inicial(n=10, N=20, rng=rng)
    for individuo in poblacion:
        assert sorted(individuo) == list(range(10))


def test_cruce_ox_siempre_da_una_permutacion_valida():
    rng = random.Random(0)
    n = 12
    for _ in range(50):
        padre1 = list(range(n))
        padre2 = list(range(n))
        rng.shuffle(padre1)
        rng.shuffle(padre2)
        hijo = _cruce_ox(padre1, padre2, rng)
        assert sorted(hijo) == list(range(n))


def test_mutacion_siempre_da_una_permutacion_valida():
    rng = random.Random(0)
    n = 10
    ruta = list(range(n))
    for _ in range(50):
        mutada = _mutacion(ruta, p_m=1.0, rng=rng)  # p_m=1 para forzar que siempre mute
        assert sorted(mutada) == list(range(n))


def test_genetico_devuelve_una_permutacion_valida(data_dir):
    inst = leer_tsp(data_dir / "berlin52.tsp")
    D = matriz_distancias(inst.coords)
    mejor_ruta, _, _ = genetico(D.shape[0], D, N=30, G_max=20, semilla=0)
    assert sorted(mejor_ruta) == list(range(D.shape[0]))


def test_genetico_es_reproducible_con_la_misma_semilla(data_dir):
    inst = leer_tsp(data_dir / "berlin52.tsp")
    D = matriz_distancias(inst.coords)
    _, costo_1, _ = genetico(D.shape[0], D, N=30, G_max=20, semilla=7)
    _, costo_2, _ = genetico(D.shape[0], D, N=30, G_max=20, semilla=7)
    assert costo_1 == costo_2


def test_genetico_mejora_respecto_a_la_poblacion_inicial(data_dir):
    inst = leer_tsp(data_dir / "berlin52.tsp")
    D = matriz_distancias(inst.coords)
    _, mejor_costo, historial = genetico(D.shape[0], D, N=60, G_max=150, semilla=3)
    assert mejor_costo < historial[0]
