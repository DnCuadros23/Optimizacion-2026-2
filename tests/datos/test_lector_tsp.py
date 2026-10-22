"""Pruebas del parser TSPLIB: que lea bien el nombre, la dimensión (n) y las coordenadas."""
from tsp.datos import leer_tsp


def test_berlin52_tiene_52_ciudades(data_dir):
    inst = leer_tsp(data_dir / "berlin52.tsp")
    assert inst.nombre == "berlin52"
    assert inst.dimension == 52
    assert inst.coords.shape == (52, 2)


def test_eil51_tiene_51_ciudades(data_dir):
    inst = leer_tsp(data_dir / "eil51.tsp")
    assert inst.nombre == "eil51"
    assert inst.dimension == 51
    assert inst.coords.shape == (51, 2)


def test_primera_ciudad_berlin52_coincide_con_el_archivo(data_dir):
    # chequeo puntual: la ciudad 1 del archivo trae las coordenadas 565.0, 575.0
    inst = leer_tsp(data_dir / "berlin52.tsp")
    assert tuple(inst.coords[0]) == (565.0, 575.0)
