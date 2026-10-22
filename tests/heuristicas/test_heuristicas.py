"""Pruebas de las heuristicas: rutas validas y que 2-opt nunca empeore la ruta de entrada."""
from tsp.datos import leer_tsp, longitud_ruta, matriz_distancias
from tsp.exactos import held_karp
from tsp.heuristicas import dos_opt, vecino_mas_cercano


def test_vecino_mas_cercano_devuelve_una_permutacion_valida(data_dir):
    inst = leer_tsp(data_dir / "berlin52.tsp")
    D = matriz_distancias(inst.coords)
    ruta = vecino_mas_cercano(D, inicio=0)
    assert sorted(ruta) == list(range(52))


def test_dos_opt_devuelve_una_permutacion_valida(data_dir):
    inst = leer_tsp(data_dir / "berlin52.tsp")
    D = matriz_distancias(inst.coords)
    ruta_mejorada = dos_opt(vecino_mas_cercano(D, inicio=0), D)
    assert sorted(ruta_mejorada) == list(range(52))


def test_dos_opt_nunca_empeora_la_ruta_de_entrada(data_dir):
    inst = leer_tsp(data_dir / "berlin52.tsp")
    D = matriz_distancias(inst.coords)
    ruta_inicial = vecino_mas_cercano(D, inicio=0)
    costo_inicial = longitud_ruta(ruta_inicial, D)
    costo_mejorado = longitud_ruta(dos_opt(ruta_inicial, D), D)
    assert costo_mejorado <= costo_inicial


def test_gap_de_nn_y_dos_opt_en_el_subconjunto_de_10_ciudades(data_dir, capsys):
    # en el subconjunto chico sí conocemos el optimo real (Held-Karp), asi que
    # aqui se puede medir el gap de verdad, no solo comparar NN contra NN+2opt
    inst = leer_tsp(data_dir / "berlin52.tsp")
    D = matriz_distancias(inst.coords[:10])
    _, optimo = held_karp(D)

    ruta_nn = vecino_mas_cercano(D, inicio=0)
    costo_nn = longitud_ruta(ruta_nn, D)
    costo_2opt = longitud_ruta(dos_opt(ruta_nn, D), D)

    gap_nn = (costo_nn - optimo) / optimo * 100
    gap_2opt = (costo_2opt - optimo) / optimo * 100
    print(
        f"\n10 ciudades: optimo={optimo}  NN={costo_nn} (gap {gap_nn:.1f}%)  "
        f"NN+2opt={costo_2opt} (gap {gap_2opt:.1f}%)"
    )

    assert costo_nn >= optimo
    assert costo_2opt >= optimo
    assert costo_2opt <= costo_nn
