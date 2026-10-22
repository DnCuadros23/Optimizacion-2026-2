"""Corre los experimentos de la fase 5 sobre berlin52.

NN y NN+2-opt (deterministicos, 1 corrida) y recocido/genetico/hormigas con
30 semillas (0..29), con los mismos parametros de partida ya probados en la
fase 4. Tarda unos minutos: son 90 corridas de metaheuristicas en total.
"""
from pathlib import Path

from tsp.datos import leer_tsp, matriz_distancias
from tsp.experimentos import ejecutar_experimentos, resumen_por_algoritmo

N_SEMILLAS = 30
RAIZ = Path(__file__).resolve().parents[1]
OPTIMO_BERLIN52 = 7542


def main():
    inst = leer_tsp(RAIZ / "data" / "raw" / "berlin52.tsp")
    D = matriz_distancias(inst.coords)

    print(f"Corriendo NN, NN+2opt y 3 metaheuristicas x {N_SEMILLAS} semillas sobre berlin52...")
    runs_df, historiales_df = ejecutar_experimentos(
        "berlin52", D, OPTIMO_BERLIN52, semillas=range(N_SEMILLAS)
    )

    # criterio de aceptacion de la fase: ninguna longitud puede ser menor que el optimo conocido
    assert (runs_df["length"] >= OPTIMO_BERLIN52).all(), "hay una longitud menor que el optimo: revisar distancias/ruta"

    runs_csv = RAIZ / "results" / "tables" / "berlin52_runs.csv"
    runs_df.to_csv(runs_csv, index=False)
    print(f"{len(runs_df)} corridas guardadas en {runs_csv}")

    historial_csv = RAIZ / "results" / "tables" / "berlin52_historial.csv"
    historiales_df.to_csv(historial_csv, index=False)
    print(f"Historial de convergencia guardado en {historial_csv} ({len(historiales_df)} filas)")

    resumen = resumen_por_algoritmo(runs_df, OPTIMO_BERLIN52)
    resumen_csv = RAIZ / "results" / "tables" / "berlin52_resumen.csv"
    resumen.to_csv(resumen_csv, index=False)
    print(f"\nResumen guardado en {resumen_csv}:\n")
    print(resumen.to_string(index=False))


if __name__ == "__main__":
    main()
