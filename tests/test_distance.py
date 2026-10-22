"""Pruebas de la matriz de distancias (d_ij) y del costo de una ruta L(π)."""
import numpy as np

from tsp.distance import matriz_distancias, tour_length
from tsp.io import leer_tsp


def test_matriz_simetrica_con_diagonal_cero(data_dir):
    # d_ij debe ser simétrica (d_ij = d_ji) y la distancia de una ciudad a sí misma es 0
    inst = leer_tsp(data_dir / "berlin52.tsp")
    D = matriz_distancias(inst.coords)
    assert D.shape == (52, 52)
    assert np.all(np.diag(D) == 0)
    assert np.array_equal(D, D.T)


def test_matriz_eil51_tiene_la_forma_correcta(data_dir):
    inst = leer_tsp(data_dir / "eil51.tsp")
    D = matriz_distancias(inst.coords)
    assert D.shape == (51, 51)
    assert np.all(np.diag(D) == 0)


def test_redondeo_tsplib_en_un_triangulo_3_4_5():
    # triángulo rectángulo de lados 3-4-5: sirve para comprobar el redondeo sin decimales raros
    coords = np.array([[0.0, 0.0], [3.0, 0.0], [3.0, 4.0]])
    D = matriz_distancias(coords)
    assert D[0, 1] == 3
    assert D[1, 2] == 4
    assert D[0, 2] == 5


def test_tour_length_incluye_el_regreso_al_origen():
    # la ruta 0->1->2 debe sumar también el tramo de vuelta 2->0 (perímetro del triángulo 3-4-5)
    coords = np.array([[0.0, 0.0], [3.0, 0.0], [3.0, 4.0]])
    D = matriz_distancias(coords)
    assert tour_length([0, 1, 2], D) == 3 + 4 + 5
