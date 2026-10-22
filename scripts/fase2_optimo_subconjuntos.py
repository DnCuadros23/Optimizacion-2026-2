"""Genera results/tables/optimo_subconjuntos.csv.

Corre fuerza bruta y Held-Karp sobre las primeras 8, 9 y 10 ciudades de
berlin52 (deben coincidir en el óptimo) y agrega el óptimo de las
primeras 12 ciudades solo con Held-Karp: a partir de ahí fuerza bruta
ya no es práctica (11! = 39 916 800 rutas).
"""
import csv
import time
from pathlib import Path

from tsp.distance import matriz_distancias
from tsp.exact import fuerza_bruta, held_karp
from tsp.io import leer_tsp

RAIZ = Path(__file__).resolve().parents[1]


def main():
    inst = leer_tsp(RAIZ / "data" / "raw" / "berlin52.tsp")
    filas = []

    for k in (8, 9, 10):
        D = matriz_distancias(inst.coords[:k])

        t0 = time.perf_counter()
        _, costo_fb = fuerza_bruta(D)
        t_fb = time.perf_counter() - t0

        t0 = time.perf_counter()
        _, costo_hk = held_karp(D)
        t_hk = time.perf_counter() - t0

        assert costo_fb == costo_hk, f"fuerza bruta y Held-Karp no coinciden para k={k}"

        filas.append({"n_ciudades": k, "metodo": "fuerza_bruta", "optimo": costo_fb, "tiempo_s": round(t_fb, 4)})
        filas.append({"n_ciudades": k, "metodo": "held_karp", "optimo": costo_hk, "tiempo_s": round(t_hk, 4)})

    D12 = matriz_distancias(inst.coords[:12])
    t0 = time.perf_counter()
    _, costo_hk12 = held_karp(D12)
    t_hk12 = time.perf_counter() - t0
    filas.append({"n_ciudades": 12, "metodo": "held_karp", "optimo": costo_hk12, "tiempo_s": round(t_hk12, 4)})

    salida = RAIZ / "results" / "tables" / "optimo_subconjuntos.csv"
    with open(salida, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=["n_ciudades", "metodo", "optimo", "tiempo_s"])
        escritor.writeheader()
        escritor.writerows(filas)

    for fila in filas:
        print(fila)
    print(f"\nGuardado en {salida}")


if __name__ == "__main__":
    main()
