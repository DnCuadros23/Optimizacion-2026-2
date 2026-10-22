"""Corre recocido simulado sobre berlin52, partiendo de la ruta de vecino mas cercano.

Parametros del metodo (cambialos aqui para probar otros valores y volver a
correr; T0 se calcula solo, pero tambien se puede fijar a mano):
"""
import csv
import time
from pathlib import Path

from tsp.datos import leer_tsp, longitud_ruta, matriz_distancias
from tsp.heuristicas import vecino_mas_cercano
from tsp.metaheuristicas import calcular_T0, recocido_simulado

ALPHA_COOL = 0.995
T_MIN = 1e-3
L_ITER = 500
SEMILLA = 0

RAIZ = Path(__file__).resolve().parents[1]
OPTIMO_BERLIN52 = 7542


def main():
    inst = leer_tsp(RAIZ / "data" / "raw" / "berlin52.tsp")
    D = matriz_distancias(inst.coords)

    ruta_inicial = vecino_mas_cercano(D, inicio=0)
    costo_inicial = longitud_ruta(ruta_inicial, D)

    T0 = calcular_T0(ruta_inicial, D, fraccion_aceptada=0.8, semilla=SEMILLA)

    t0 = time.perf_counter()
    mejor_ruta, mejor_costo, historial = recocido_simulado(
        ruta_inicial, D, T0=T0, alpha_cool=ALPHA_COOL, T_min=T_MIN, L_iter=L_ITER, semilla=SEMILLA
    )
    tiempo = time.perf_counter() - t0

    gap = round((mejor_costo - OPTIMO_BERLIN52) / OPTIMO_BERLIN52 * 100, 2)

    niveles_temperatura = len(historial) - 1
    total_movimientos = niveles_temperatura * L_ITER

    print(f"Ruta inicial (vecino mas cercano): {costo_inicial}")
    print(f"T0 calculado (acepta ~80% de empeoramientos al inicio): {T0:.1f}")
    print(
        f"Recocido simulado: {mejor_costo} (gap {gap}%), "
        f"{niveles_temperatura} niveles de temperatura ({total_movimientos} movimientos en total), {tiempo:.2f}s"
    )

    salida_resumen = RAIZ / "results" / "tables" / "recocido_berlin52.csv"
    with open(salida_resumen, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=["algoritmo", "longitud", "gap_pct", "tiempo_s"])
        escritor.writeheader()
        escritor.writerow(
            {"algoritmo": "recocido_simulado", "longitud": mejor_costo, "gap_pct": gap, "tiempo_s": round(tiempo, 4)}
        )
    print(f"Resumen guardado en {salida_resumen}")

    salida_historial = RAIZ / "results" / "tables" / "recocido_berlin52_historial.csv"
    with open(salida_historial, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["iteracion", "mejor_costo"])
        escritor.writerows(enumerate(historial))
    print(f"Historial de convergencia guardado en {salida_historial}")


if __name__ == "__main__":
    main()
