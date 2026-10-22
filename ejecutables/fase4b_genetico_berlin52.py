"""Corre el algoritmo genetico sobre berlin52.

Parametros del metodo (cambialos aqui para probar otros valores y volver a
correr):
"""
import csv
import time
from pathlib import Path

from tsp.datos import leer_tsp, matriz_distancias
from tsp.metaheuristicas import genetico

# Valores de partida de la guia (seccion 5 de docs/contexto.md), todavia sin
# calibrar: la fase 6 ajusta N y p_m con datos reales. Con p_m bajo, el
# genetico tiende a converger antes de tiempo (pierde diversidad); subir p_m
# ya adelanta una mejora, pero esa calibracion formal se deja para la fase 6.
N = 150
P_C = 0.9
P_M = 0.05
G_MAX = 500
E = 3
SEMILLA = 0

RAIZ = Path(__file__).resolve().parents[1]
OPTIMO_BERLIN52 = 7542


def main():
    inst = leer_tsp(RAIZ / "data" / "raw" / "berlin52.tsp")
    D = matriz_distancias(inst.coords)

    t0 = time.perf_counter()
    mejor_ruta, mejor_costo, historial = genetico(
        D.shape[0], D, N=N, p_c=P_C, p_m=P_M, G_max=G_MAX, e=E, semilla=SEMILLA
    )
    tiempo = time.perf_counter() - t0

    gap = round((mejor_costo - OPTIMO_BERLIN52) / OPTIMO_BERLIN52 * 100, 2)

    print(f"Poblacion inicial: {historial[0]}")
    print(f"Genetico: {mejor_costo} (gap {gap}%), {G_MAX} generaciones, {tiempo:.2f}s")

    salida_resumen = RAIZ / "results" / "tables" / "genetico_berlin52.csv"
    with open(salida_resumen, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=["algoritmo", "longitud", "gap_pct", "tiempo_s"])
        escritor.writeheader()
        escritor.writerow(
            {"algoritmo": "genetico", "longitud": mejor_costo, "gap_pct": gap, "tiempo_s": round(tiempo, 4)}
        )
    print(f"Resumen guardado en {salida_resumen}")

    salida_historial = RAIZ / "results" / "tables" / "genetico_berlin52_historial.csv"
    with open(salida_historial, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["generacion", "mejor_costo"])
        escritor.writerows(enumerate(historial))
    print(f"Historial de convergencia guardado en {salida_historial}")


if __name__ == "__main__":
    main()
