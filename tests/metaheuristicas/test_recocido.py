"""Pruebas del recocido simulado: ruta valida, reproducible, y que mejore una ruta al azar."""
import random

from tsp.datos import leer_tsp, longitud_ruta, matriz_distancias
from tsp.metaheuristicas import calcular_T0, recocido_simulado


def _matriz_berlin52(data_dir):
    inst = leer_tsp(data_dir / "berlin52.tsp")
    return matriz_distancias(inst.coords)


def test_recocido_devuelve_una_permutacion_valida(data_dir):
    D = _matriz_berlin52(data_dir)
    ruta_inicial = list(range(D.shape[0]))
    T0 = calcular_T0(ruta_inicial, D, semilla=0)
    mejor_ruta, _, _ = recocido_simulado(ruta_inicial, D, T0=T0, L_iter=20, semilla=0)
    assert sorted(mejor_ruta) == list(range(D.shape[0]))


def test_recocido_es_reproducible_con_la_misma_semilla(data_dir):
    D = _matriz_berlin52(data_dir)
    ruta_inicial = list(range(D.shape[0]))
    T0 = calcular_T0(ruta_inicial, D, semilla=0)
    _, costo_1, _ = recocido_simulado(ruta_inicial, D, T0=T0, L_iter=20, semilla=42)
    _, costo_2, _ = recocido_simulado(ruta_inicial, D, T0=T0, L_iter=20, semilla=42)
    assert costo_1 == costo_2


def test_recocido_mejora_claramente_una_ruta_armada_al_azar(data_dir):
    D = _matriz_berlin52(data_dir)
    n = D.shape[0]

    rng = random.Random(1)
    ruta_aleatoria = list(range(n))
    rng.shuffle(ruta_aleatoria)
    costo_inicial = longitud_ruta(ruta_aleatoria, D)

    T0 = calcular_T0(ruta_aleatoria, D, semilla=1)
    _, mejor_costo, historial = recocido_simulado(
        ruta_aleatoria, D, T0=T0, alpha_cool=0.97, L_iter=50, semilla=1
    )

    assert mejor_costo < costo_inicial
    assert historial[0] >= historial[-1]  # el historial del "mejor hasta ahora" nunca empeora
