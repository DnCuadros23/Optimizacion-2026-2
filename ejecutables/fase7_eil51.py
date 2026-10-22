"""Fase 7: repite los experimentos de la fase 5 sobre eil51, con la
configuracion calibrada en la fase 6, y compara contra berlin52.
"""
from pathlib import Path

import pandas as pd

from tsp.config import leer_config
from tsp.datos import leer_tsp, matriz_distancias
from tsp.experimentos import ejecutar_experimentos, resumen_por_algoritmo

RAIZ = Path(__file__).resolve().parents[1]
OPTIMO_EIL51 = 426
N_SEMILLAS = 30


def main():
    config = leer_config(RAIZ / "config" / "best.yaml")

    inst = leer_tsp(RAIZ / "data" / "raw" / "eil51.tsp")
    D = matriz_distancias(inst.coords)

    print(f"Corriendo NN, NN+2opt y 3 metaheuristicas x {N_SEMILLAS} semillas sobre eil51 (config calibrada)...")
    runs_df, historiales_df = ejecutar_experimentos(
        "eil51", D, OPTIMO_EIL51, semillas=range(N_SEMILLAS),
        params_recocido=config["recocido_simulado"],
        params_genetico=config["genetico"],
        params_hormigas=config["hormigas"],
        config_id="calibrado",
    )

    assert (runs_df["length"] >= OPTIMO_EIL51).all(), "hay una longitud menor que el optimo: revisar"

    runs_csv = RAIZ / "results" / "tables" / "eil51_runs.csv"
    runs_df.to_csv(runs_csv, index=False)
    print(f"{len(runs_df)} corridas guardadas en {runs_csv}")

    historial_csv = RAIZ / "results" / "tables" / "eil51_historial.csv"
    historiales_df.to_csv(historial_csv, index=False)
    print(f"Historial guardado en {historial_csv} ({len(historiales_df)} filas)")

    resumen = resumen_por_algoritmo(runs_df, OPTIMO_EIL51)
    resumen_csv = RAIZ / "results" / "tables" / "eil51_resumen.csv"
    resumen.to_csv(resumen_csv, index=False)
    print(f"\nResumen eil51 guardado en {resumen_csv}:\n")
    print(resumen.to_string(index=False))

    # tabla comparativa: berlin52 (calibrado, fase 6) vs eil51
    berlin_resumen_path = RAIZ / "results" / "tables" / "berlin52_resumen_calibrado.csv"
    if berlin_resumen_path.exists():
        berlin_resumen = pd.read_csv(berlin_resumen_path).assign(instance="berlin52")
        eil_resumen = resumen.assign(instance="eil51")
        comparacion = pd.concat([berlin_resumen, eil_resumen], ignore_index=True)
        comparacion_csv = RAIZ / "results" / "tables" / "comparacion_instancias.csv"
        comparacion.to_csv(comparacion_csv, index=False)
        print(f"\nComparacion berlin52 vs eil51 guardada en {comparacion_csv}")


if __name__ == "__main__":
    main()
