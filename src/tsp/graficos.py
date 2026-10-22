"""Figuras y tablas finales para el informe (fase 8).

Tres tipos de figura: la ruta final de un algoritmo sobre las coordenadas,
la curva de convergencia (media +/- desviación entre semillas) y un boxplot
de longitudes por algoritmo. Además, tabla_a_latex exporta una tabla con el
estilo del informe (columnas con líneas verticales, \\hline, \\arraystretch).
"""
import matplotlib
import pandas as pd

matplotlib.use("Agg")  # sin GUI: estos graficos solo se guardan a archivo, nunca se muestran en pantalla
import matplotlib.pyplot as plt


def figura_ruta(coords, ruta, titulo, archivo_salida):
    """Dibuja una ruta (lista de índices de ciudad) sobre sus coordenadas (x, y)."""
    orden = list(ruta) + [ruta[0]]
    xs = coords[orden, 0]
    ys = coords[orden, 1]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(xs, ys, "-o", color="C0", markersize=4, linewidth=1)
    ax.set_title(titulo)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(archivo_salida, dpi=150)
    plt.close(fig)


def figura_convergencia(historial_df, algo, optimo, titulo, etiqueta_x, archivo_salida):
    """Media +/- desviación del mejor-costo-hasta-el-momento, entre semillas, para un algoritmo."""
    sub = historial_df[historial_df["algo"] == algo]
    resumen = sub.groupby("iteracion")["mejor_costo"].agg(["mean", "std"]).reset_index()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(resumen["iteracion"], resumen["mean"], color="C0", label="media")
    ax.fill_between(
        resumen["iteracion"],
        resumen["mean"] - resumen["std"].fillna(0),
        resumen["mean"] + resumen["std"].fillna(0),
        color="C0", alpha=0.2, label="+/- 1 desviación",
    )
    ax.axhline(optimo, color="gray", linestyle="--", label=f"óptimo conocido ({optimo})")
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel("Mejor costo hasta el momento")
    ax.set_title(titulo)
    ax.legend()
    fig.tight_layout()
    fig.savefig(archivo_salida, dpi=150)
    plt.close(fig)


def figura_boxplot(runs_df, titulo, archivo_salida):
    """Boxplot de longitudes por algoritmo (de las corridas con semilla, las estocásticas)."""
    algoritmos = [a for a in runs_df["algo"].unique() if runs_df[runs_df["algo"] == a]["seed"].notna().any()]
    datos = [runs_df[runs_df["algo"] == a]["length"].values for a in algoritmos]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.boxplot(datos, tick_labels=algoritmos)
    ax.set_ylabel("Longitud")
    ax.set_title(titulo)
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    fig.tight_layout()
    fig.savefig(archivo_salida, dpi=150)
    plt.close(fig)


def tabla_a_latex(df, caption, label):
    """Convierte un DataFrame a una tabla LaTeX con el estilo del informe
    (columnas con líneas verticales y \\hline, \\renewcommand{\\arraystretch}{1.3}, [H])."""

    def escapar(valor):
        texto = str(valor)
        return texto.replace("_", r"\_").replace("%", r"\%")

    columnas = list(df.columns)
    # texto a la izquierda, numeros a la derecha (pandas 3 usa dtype "str" para texto, ya no "object")
    spec_columnas = "|" + "|".join("r" if pd.api.types.is_numeric_dtype(df[c]) else "l" for c in columnas) + "|"

    lineas = [
        r"\begin{table}[H]",
        r"\centering",
        r"\renewcommand{\arraystretch}{1.3}",
        rf"\begin{{tabular}}{{{spec_columnas}}}",
        r"\hline",
        " & ".join(escapar(c) for c in columnas) + r" \\",
        r"\hline",
    ]
    for _, fila in df.iterrows():
        lineas.append(" & ".join(escapar(v) for v in fila) + r" \\")
    lineas += [
        r"\hline",
        r"\end{tabular}",
        rf"\caption{{{caption}}}",
        rf"\label{{{label}}}",
        r"\end{table}",
    ]
    return "\n".join(lineas)
