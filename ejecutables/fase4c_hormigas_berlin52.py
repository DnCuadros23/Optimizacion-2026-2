"""Corre la colonia de hormigas (ACO) sobre berlin52.

Parametros del metodo (cambialos aqui para probar otros valores y volver a
correr). M, ALPHA y Q son valores razonables de la guia que no se vuelven
a tocar; BETA y RHO son justo los que calibra la fase 6.
"""
import csv
import time
from pathlib import Path

from tsp.datos import leer_tsp, matriz_distancias
from tsp.metaheuristicas import hormigas

M = None  # None -> una hormiga por ciudad (m=n), como sugiere la guia
ALPHA = 1
BETA = 3
RHO = 0.3
Q = 100
T_MAX = 100
SEMILLA = 0

RAIZ = Path(__file__).resolve().parents[1]
OPTIMO_BERLIN52 = 7542


def main():
    inst = leer_tsp(RAIZ / "data" / "raw" / "berlin52.tsp")
    D = matriz_distancias(inst.coords)
    n = D.shape[0]

    t0 = time.perf_counter()
    mejor_ruta, mejor_costo, historial = hormigas(
        n, D, m=M, alpha=ALPHA, beta=BETA, rho=RHO, Q=Q, t_max=T_MAX, semilla=SEMILLA
    )
    tiempo = time.perf_counter() - t0

    gap = round((mejor_costo - OPTIMO_BERLIN52) / OPTIMO_BERLIN52 * 100, 2)

    print(f"Colonia de hormigas: {mejor_costo} (gap {gap}%), {T_MAX} rondas, {tiempo:.2f}s")

    salida_resumen = RAIZ / "results" / "tables" / "hormigas_berlin52.csv"
    with open(salida_resumen, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=["algoritmo", "longitud", "gap_pct", "tiempo_s"])
        escritor.writeheader()
        escritor.writerow(
            {"algoritmo": "hormigas", "longitud": mejor_costo, "gap_pct": gap, "tiempo_s": round(tiempo, 4)}
        )
    print(f"Resumen guardado en {salida_resumen}")

    salida_historial = RAIZ / "results" / "tables" / "hormigas_berlin52_historial.csv"
    with open(salida_historial, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["ronda", "mejor_costo"])
        escritor.writerows(enumerate(historial))
    print(f"Historial de convergencia guardado en {salida_historial}")


if __name__ == "__main__":
    main()
