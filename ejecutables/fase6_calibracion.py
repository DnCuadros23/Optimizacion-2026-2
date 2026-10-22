"""Fase 6: calibracion de parametros (seccion 5.1 del informe).

Varia un parametro a la vez por metaheuristica (bajo/medio/alto, 10 semillas
cada uno), guarda resultados y figuras, elige la configuracion final de cada
metodo con los datos (no a ojo) y la guarda en config/best.yaml.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from tsp.calibracion import (
    BASE_GENETICO, BASE_HORMIGAS, BASE_RECOCIDO,
    calibrar_genetico, calibrar_hormigas, calibrar_recocido_T0, calibrar_recocido_alpha_cool,
)
from tsp.datos import leer_tsp, matriz_distancias
from tsp.heuristicas import vecino_mas_cercano
from tsp.metaheuristicas import calcular_T0

RAIZ = Path(__file__).resolve().parents[1]
TABLAS = RAIZ / "results" / "tables"
FIGURAS = RAIZ / "results" / "figures"
OPTIMO_BERLIN52 = 7542


def figura_por_parametro(df, metodo, parametro, archivo_salida):
    """Media +/- desviacion del largo final, por nivel (bajo/medio/alto) de un parametro."""
    sub = df[(df["metodo"] == metodo) & (df["parametro"] == parametro)]
    resumen = sub.groupby(["nivel", "valor"], sort=False)["length"].agg(["mean", "std"]).reset_index()
    resumen["orden"] = resumen["nivel"].map({"bajo": 0, "medio": 1, "alto": 2})
    resumen = resumen.sort_values("orden")

    fig, ax = plt.subplots(figsize=(5, 4))
    etiquetas = [f"{n}\n({v})" for n, v in zip(resumen["nivel"], resumen["valor"])]
    ax.bar(etiquetas, resumen["mean"], yerr=resumen["std"].fillna(0), capsize=5, color="C0")
    ax.set_ylabel("Longitud final (media +/- desviacion)")
    ax.set_title(f"{metodo}: efecto de {parametro}")
    fig.tight_layout()
    fig.savefig(FIGURAS / archivo_salida, dpi=150)
    plt.close(fig)


def main():
    inst = leer_tsp(RAIZ / "data" / "raw" / "berlin52.tsp")
    D = matriz_distancias(inst.coords)
    n = D.shape[0]
    ruta_inicial = vecino_mas_cercano(D, inicio=0)
    T0_base = calcular_T0(ruta_inicial, D, semilla=0)

    print(f"T0 base (referencia): {T0_base:.1f}")

    todas_las_filas = []

    print("Calibrando recocido: T0...")
    todas_las_filas += calibrar_recocido_T0(
        D, "berlin52", OPTIMO_BERLIN52, valores_T0=[round(T0_base * 0.3), round(T0_base), round(T0_base * 3)]
    )

    print("Calibrando recocido: alpha_cool...")
    todas_las_filas += calibrar_recocido_alpha_cool(
        D, "berlin52", OPTIMO_BERLIN52, valores_alpha=[0.90, 0.995, 0.998], T0_fijo=T0_base
    )

    print("Calibrando genetico: N...")
    todas_las_filas += calibrar_genetico(n, D, "berlin52", OPTIMO_BERLIN52, "N", valores=[50, 150, 300])

    print("Calibrando genetico: p_m...")
    todas_las_filas += calibrar_genetico(n, D, "berlin52", OPTIMO_BERLIN52, "p_m", valores=[0.02, 0.1, 0.3])

    print("Calibrando hormigas: rho...")
    todas_las_filas += calibrar_hormigas(n, D, "berlin52", OPTIMO_BERLIN52, "rho", valores=[0.1, 0.3, 0.7])

    print("Calibrando hormigas: beta...")
    todas_las_filas += calibrar_hormigas(n, D, "berlin52", OPTIMO_BERLIN52, "beta", valores=[1, 3, 6])

    df = pd.DataFrame(todas_las_filas)
    assert (df["length"] >= OPTIMO_BERLIN52).all(), "hay una longitud menor que el optimo: revisar"

    salida_csv = TABLAS / "calibracion.csv"
    df.to_csv(salida_csv, index=False)
    print(f"\n{len(df)} corridas de calibracion guardadas en {salida_csv}")

    FIGURAS.mkdir(parents=True, exist_ok=True)
    combinaciones = [
        ("recocido_simulado", "T0", "calibracion_recocido_T0.png"),
        ("recocido_simulado", "alpha_cool", "calibracion_recocido_alpha_cool.png"),
        ("genetico", "N", "calibracion_genetico_N.png"),
        ("genetico", "p_m", "calibracion_genetico_p_m.png"),
        ("hormigas", "rho", "calibracion_hormigas_rho.png"),
        ("hormigas", "beta", "calibracion_hormigas_beta.png"),
    ]
    for metodo, parametro, archivo in combinaciones:
        figura_por_parametro(df, metodo, parametro, archivo)
    print(f"6 figuras guardadas en {FIGURAS}")

    # resumen: que paso en cada nivel (bajo/medio/alto) de cada parametro
    resumen = (
        df.groupby(["metodo", "parametro", "nivel", "valor"], sort=False)["gap_pct"]
        .agg(gap_medio="mean", gap_desviacion="std")
        .reset_index()
    )
    resumen["orden"] = resumen["nivel"].map({"bajo": 0, "medio": 1, "alto": 2})
    resumen = resumen.sort_values(["metodo", "parametro", "orden"]).drop(columns="orden")
    resumen_csv = TABLAS / "calibracion_resumen.csv"
    resumen.to_csv(resumen_csv, index=False)
    print(f"\nResumen por nivel guardado en {resumen_csv}:\n")
    print(resumen.to_string(index=False))

    # configuracion final: por cada parametro, el nivel con menor gap medio
    mejor_por_parametro = resumen.loc[resumen.groupby(["metodo", "parametro"])["gap_medio"].idxmin()]

    # al juntar todos los parametros en una sola columna "valor", pandas la vuelve
    # float64 aunque algunos sean enteros (N, G_max, e, L_iter, m, t_max); hay que
    # devolverlos a int o range(N) y las demas funciones que los usan como entero fallan
    PARAMETROS_ENTEROS = {"N", "G_max", "e", "L_iter", "m", "t_max"}

    def _valor_final(parametro, valor):
        return int(valor) if parametro in PARAMETROS_ENTEROS else valor

    config_final = {
        "recocido_simulado": dict(BASE_RECOCIDO),
        "genetico": dict(BASE_GENETICO),
        "hormigas": dict(BASE_HORMIGAS),
    }
    for _, fila in mejor_por_parametro.iterrows():
        config_final[fila["metodo"]][fila["parametro"]] = _valor_final(fila["parametro"], fila["valor"])

    print("\nConfiguracion final elegida por los datos:")
    for metodo, params in config_final.items():
        print(f"  {metodo}: {params}")

    (RAIZ / "config").mkdir(parents=True, exist_ok=True)
    with open(RAIZ / "config" / "best.yaml", "w", encoding="utf-8") as f:
        f.write("# Configuracion final de cada metaheuristica, elegida en la fase 6\n")
        f.write("# (el nivel bajo/medio/alto con menor gap medio en la calibracion)\n")
        for metodo, params in config_final.items():
            f.write(f"{metodo}:\n")
            for clave, valor in params.items():
                f.write(f"  {clave}: {valor}\n")

    print(f"\nGuardado en {RAIZ / 'config' / 'best.yaml'}")


if __name__ == "__main__":
    main()
