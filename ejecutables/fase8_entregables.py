"""Fase 8: figuras finales, tablas en LaTeX y README.md reproducible.

Usa los resultados ya calibrados (fase 6) y la segunda instancia (fase 7):
berlin52_runs_calibrado.csv / berlin52_historial_calibrado.csv y los
equivalentes de eil51.
"""
from pathlib import Path

import pandas as pd

from tsp.config import leer_config
from tsp.datos import leer_tsp, longitud_ruta, matriz_distancias
from tsp.graficos import figura_boxplot, figura_convergencia, figura_ruta, tabla_a_latex
from tsp.heuristicas import dos_opt, vecino_mas_cercano
from tsp.metaheuristicas import calcular_T0, genetico, hormigas, recocido_simulado

RAIZ = Path(__file__).resolve().parents[1]
TABLAS = RAIZ / "results" / "tables"
FIGURAS = RAIZ / "results" / "figures"
OPTIMOS = {"berlin52": 7542, "eil51": 426}
SEMILLA_RUTA = 0  # semilla usada para la ruta "representativa" de cada metaheuristica


def rutas_representativas(instancia, D, config):
    """Una ruta por algoritmo: NN y NN+2opt (deterministicas) y una corrida fija de cada metaheuristica."""
    n = D.shape[0]
    ruta_nn = vecino_mas_cercano(D, inicio=0)
    ruta_2opt = dos_opt(ruta_nn, D)

    T0 = calcular_T0(ruta_nn, D, semilla=SEMILLA_RUTA)
    params_recocido = dict(config["recocido_simulado"])
    params_recocido.pop("T0", None)
    ruta_recocido, _, _ = recocido_simulado(ruta_nn, D, T0=T0, semilla=SEMILLA_RUTA, **params_recocido)

    ruta_genetico, _, _ = genetico(n, D, semilla=SEMILLA_RUTA, **config["genetico"])
    ruta_hormigas, _, _ = hormigas(n, D, semilla=SEMILLA_RUTA, **config["hormigas"])

    return {
        "nearest_neighbor": ruta_nn,
        "nearest_neighbor+2opt": ruta_2opt,
        "recocido_simulado": ruta_recocido,
        "genetico": ruta_genetico,
        "hormigas": ruta_hormigas,
    }


def generar_figuras_instancia(instancia, archivo_tsp, runs_csv, historial_csv, config):
    inst = leer_tsp(archivo_tsp)
    D = matriz_distancias(inst.coords)
    optimo = OPTIMOS[instancia]

    rutas = rutas_representativas(instancia, D, config)
    for algo, ruta in rutas.items():
        costo = longitud_ruta(ruta, D)
        figura_ruta(
            inst.coords, ruta, f"{algo} en {instancia} (L={costo})",
            FIGURAS / f"ruta_{instancia}_{algo}.png",
        )

    historial_df = pd.read_csv(historial_csv)
    etiquetas_x = {"recocido_simulado": "Nivel de temperatura", "genetico": "Generación", "hormigas": "Ronda"}
    for algo, etiqueta_x in etiquetas_x.items():
        figura_convergencia(
            historial_df, algo, optimo, f"Convergencia de {algo} en {instancia}", etiqueta_x,
            FIGURAS / f"convergencia_{instancia}_{algo}_final.png",
        )

    runs_df = pd.read_csv(runs_csv)
    figura_boxplot(runs_df, f"Longitud por algoritmo en {instancia} (30 semillas)", FIGURAS / f"boxplot_{instancia}.png")


COLUMNAS_LEGIBLES = {
    "berlin52_resumen_calibrado.csv": {
        "algo": "Algoritmo", "mejor": "Mejor", "media": "Media", "desviacion": "Desviación",
        "gap_mejor_pct": "Gap mejor (%)", "gap_medio_pct": "Gap medio (%)",
    },
    "eil51_resumen.csv": {
        "algo": "Algoritmo", "mejor": "Mejor", "media": "Media", "desviacion": "Desviación",
        "gap_mejor_pct": "Gap mejor (%)", "gap_medio_pct": "Gap medio (%)",
    },
    "calibracion_resumen.csv": {
        "metodo": "Método", "parametro": "Parámetro", "nivel": "Nivel", "valor": "Valor",
        "gap_medio": "Gap medio (%)", "gap_desviacion": "Desviación (%)",
    },
    "optimo_subconjuntos.csv": {
        "n_ciudades": "Ciudades", "metodo": "Método", "optimo": "Óptimo", "tiempo_s": "Tiempo (s)",
    },
}


def exportar_tablas_latex():
    tablas_latex = RAIZ / "results" / "tables" / "latex"
    tablas_latex.mkdir(parents=True, exist_ok=True)

    especificaciones = [
        ("berlin52_resumen_calibrado.csv", "Resultados sobre berlin52 (configuración calibrada, 30 semillas)", "tab:berlin52"),
        ("eil51_resumen.csv", "Resultados sobre eil51 (configuración calibrada, 30 semillas)", "tab:eil51"),
        ("calibracion_resumen.csv", "Efecto de cada parámetro en la calibración (fase 6)", "tab:calibracion"),
        ("optimo_subconjuntos.csv", "Óptimo y tiempo de fuerza bruta vs. Held-Karp en subconjuntos pequeños", "tab:exactos"),
    ]
    for nombre_csv, caption, label in especificaciones:
        ruta_csv = TABLAS / nombre_csv
        if not ruta_csv.exists():
            print(f"(omitido: no existe {ruta_csv})")
            continue
        df = pd.read_csv(ruta_csv)
        df = df.round(2).rename(columns=COLUMNAS_LEGIBLES[nombre_csv])  # 2 decimales y encabezados legibles
        latex = tabla_a_latex(df, caption, label)
        destino = tablas_latex / nombre_csv.replace(".csv", ".tex")
        destino.write_text(latex, encoding="utf-8")
        print(f"Tabla LaTeX guardada en {destino}")


def main():
    FIGURAS.mkdir(parents=True, exist_ok=True)
    config = leer_config(RAIZ / "config" / "best.yaml")

    print("Generando figuras finales para berlin52...")
    generar_figuras_instancia(
        "berlin52", RAIZ / "data" / "raw" / "berlin52.tsp",
        TABLAS / "berlin52_runs_calibrado.csv", TABLAS / "berlin52_historial_calibrado.csv", config,
    )

    print("Generando figuras finales para eil51...")
    generar_figuras_instancia(
        "eil51", RAIZ / "data" / "raw" / "eil51.tsp",
        TABLAS / "eil51_runs.csv", TABLAS / "eil51_historial.csv", config,
    )

    print("Exportando tablas finales a LaTeX...")
    exportar_tablas_latex()

    print(f"\nListo. Figuras en {FIGURAS}, tablas LaTeX en {TABLAS / 'latex'}")


if __name__ == "__main__":
    main()
