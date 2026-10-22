"""Corre vecino mas cercano (NN) y NN+2-opt sobre berlin52 completo.

Reporta la longitud de cada ruta y su gap contra el optimo conocido (7542),
y guarda los resultados en results/tables/heuristicas_berlin52.csv.

Parametros faciles de cambiar para una demo en vivo: CIUDAD_INICIO (desde
que ciudad arranca vecino mas cercano) y OPTIMO_BERLIN52 (el valor contra
el que se mide el gap, si algun dia se usa otra instancia).
"""
import csv
import time
from pathlib import Path

from tsp.datos import leer_tsp, longitud_ruta, matriz_distancias
from tsp.heuristicas import dos_opt, vecino_mas_cercano

RAIZ = Path(__file__).resolve().parents[1]
CIUDAD_INICIO = 0
OPTIMO_BERLIN52 = 7542


def main():
    inst = leer_tsp(RAIZ / "data" / "raw" / "berlin52.tsp")
    D = matriz_distancias(inst.coords)

    t0 = time.perf_counter()
    ruta_nn = vecino_mas_cercano(D, inicio=CIUDAD_INICIO)
    t_nn = time.perf_counter() - t0
    costo_nn = longitud_ruta(ruta_nn, D)

    t0 = time.perf_counter()
    ruta_2opt = dos_opt(ruta_nn, D)
    t_2opt = time.perf_counter() - t0
    costo_2opt = longitud_ruta(ruta_2opt, D)

    filas = [
        {
            "algoritmo": "vecino_mas_cercano",
            "longitud": costo_nn,
            "gap_pct": round((costo_nn - OPTIMO_BERLIN52) / OPTIMO_BERLIN52 * 100, 2),
            "tiempo_s": round(t_nn, 4),
        },
        {
            "algoritmo": "vecino_mas_cercano+2opt",
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
