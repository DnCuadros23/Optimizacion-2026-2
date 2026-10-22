"""Vuelve a correr los experimentos de la fase 5 sobre berlin52, ahora con la
configuracion final elegida en la fase 6 (config/best.yaml).

Los resultados de la fase 5 (antes de calibrar) no se borran: quedan en
berlin52_runs.csv / berlin52_resumen.csv como punto de comparacion "antes".
Esta corrida se guarda aparte, con sufijo _calibrado, como el resultado
"despues" de calibrar.
"""
from pathlib import Path

import pandas as pd

from tsp.config import leer_config
from tsp.datos import leer_tsp, matriz_distancias
from tsp.experimentos import ejecutar_experimentos, resumen_por_algoritmo

RAIZ = Path(__file__).resolve().parents[1]
OPTIMO_BERLIN52 = 7542
N_SEMILLAS = 30


def main():
    config = leer_config(RAIZ / "config" / "best.yaml")

    inst = leer_tsp(RAIZ / "data" / "raw" / "berlin52.tsp")
    D = matriz_distancias(inst.coords)

    print(f"Corriendo berlin52 con la configuracion calibrada x {N_SEMILLAS} semillas...")
    runs_df, historiales_df = ejecutar_experimentos(
        "berlin52", D, OPTIMO_BERLIN52, semillas=range(N_SEMILLAS),
        params_recocido=config["recocido_simulado"],
        params_genetico=config["genetico"],
        params_hormigas=config["hormigas"],
        config_id="calibrado",
    )

    assert (runs_df["length"] >= OPTIMO_BERLIN52).all(), "hay una longitud menor que el optimo: revisar"

    runs_csv = RAIZ / "results" / "tables" / "berlin52_runs_calibrado.csv"
    runs_df.to_csv(runs_csv, index=False)
    print(f"{len(runs_df)} corridas guardadas en {runs_csv}")

    historial_csv = RAIZ / "results" / "tables" / "berlin52_historial_calibrado.csv"
    historiales_df.to_csv(historial_csv, index=False)
    print(f"Historial guardado en {historial_csv} ({len(historiales_df)} filas)")

    resumen = resumen_por_algoritmo(runs_df, OPTIMO_BERLIN52)
    resumen_csv = RAIZ / "results" / "tables" / "berlin52_resumen_calibrado.csv"
    resumen.to_csv(resumen_csv, index=False)
    print(f"\nResumen (calibrado) guardado en {resumen_csv}:\n")
    print(resumen.to_string(index=False))

    # comparacion antes/despues de calibrar
    antes = pd.read_csv(RAIZ / "results" / "tables" / "berlin52_resumen.csv")
    antes = antes[antes["algo"].isin(["recocido_simulado", "genetico", "hormigas"])].assign(config_id="base")
    despues = resumen[resumen["algo"].isin(["recocido_simulado", "genetico", "hormigas"])].assign(config_id="calibrado")
    comparacion = pd.concat([antes, despues], ignore_index=True)
    comparacion_csv = RAIZ / "results" / "tables" / "calibracion_antes_despues.csv"
    comparacion.to_csv(comparacion_csv, index=False)
    print(f"\nComparacion antes/despues de calibrar guardada en {comparacion_csv}")


if __name__ == "__main__":
    main()
