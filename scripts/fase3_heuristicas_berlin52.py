"""Corre vecino mas cercano (NN) y NN+2-opt sobre berlin52 completo.

Reporta la longitud de cada ruta y su gap contra el optimo conocido (7542),
y guarda los resultados en results/tables/heuristicas_berlin52.csv.
"""
import csv
import time
from pathlib import Path

from tsp.distance import matriz_distancias, tour_length
from tsp.heuristics import nearest_neighbor, two_opt
from tsp.io import leer_tsp

RAIZ = Path(__file__).resolve().parents[1]
OPTIMO_BERLIN52 = 7542


def main():
    inst = leer_tsp(RAIZ / "data" / "raw" / "berlin52.tsp")
    D = matriz_distancias(inst.coords)

    t0 = time.perf_counter()
    ruta_nn = nearest_neighbor(D, start=0)
    t_nn = time.perf_counter() - t0
    costo_nn = tour_length(ruta_nn, D)

    t0 = time.perf_counter()
    ruta_2opt = two_opt(ruta_nn, D)
    t_2opt = time.perf_counter() - t0
    costo_2opt = tour_length(ruta_2opt, D)

    filas = [
        {
            "algoritmo": "nearest_neighbor",
            "longitud": costo_nn,
            "gap_pct": round((costo_nn - OPTIMO_BERLIN52) / OPTIMO_BERLIN52 * 100, 2),
            "tiempo_s": round(t_nn, 4),
        },
        {
            "algoritmo": "nearest_neighbor+2opt",
            "longitud": costo_2opt,
            "gap_pct": round((costo_2opt - OPTIMO_BERLIN52) / OPTIMO_BERLIN52 * 100, 2),
            "tiempo_s": round(t_2opt, 4),
        },
    ]

    salida = RAIZ / "results" / "tables" / "heuristicas_berlin52.csv"
    with open(salida, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=["algoritmo", "longitud", "gap_pct", "tiempo_s"])
        escritor.writeheader()
        escritor.writerows(filas)

    for fila in filas:
        print(fila)
    print(f"\nGuardado en {salida}")


if __name__ == "__main__":
    main()
