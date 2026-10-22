"""Pruebas de los metodos exactos: en subconjuntos chicos, fuerza bruta y Held-Karp deben coincidir."""
from tsp.distance import matriz_distancias
from tsp.exact import fuerza_bruta, held_karp
from tsp.io import leer_tsp


def _matriz_subconjunto(data_dir, k):
    # toma las primeras k ciudades de berlin52 como una instancia chica, solo para validar
    inst = leer_tsp(data_dir / "berlin52.tsp")
    return matriz_distancias(inst.coords[:k])


def test_fuerza_bruta_y_held_karp_coinciden_en_8_ciudades(data_dir):
    D = _matriz_subconjunto(data_dir, 8)
    _, costo_fb = fuerza_bruta(D)
    _, costo_hk = held_karp(D)
    assert costo_fb == costo_hk


def test_fuerza_bruta_y_held_karp_coinciden_en_9_ciudades(data_dir):
    D = _matriz_subconjunto(data_dir, 9)
    _, costo_fb = fuerza_bruta(D)
    _, costo_hk = held_karp(D)
    assert costo_fb == costo_hk


def test_fuerza_bruta_y_held_karp_coinciden_en_10_ciudades(data_dir):
    D = _matriz_subconjunto(data_dir, 10)
    _, costo_fb = fuerza_bruta(D)
    _, costo_hk = held_karp(D)
    assert costo_fb == costo_hk


def test_ambos_metodos_devuelven_una_permutacion_valida(data_dir):
    D = _matriz_subconjunto(data_dir, 9)
    ruta_fb, _ = fuerza_bruta(D)
    ruta_hk, _ = held_karp(D)
    assert sorted(ruta_fb) == list(range(9))
    assert sorted(ruta_hk) == list(range(9))
