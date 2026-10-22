"""Genera unas pocas figuras preliminares para el registro/informe tecnico.

No son las figuras finales de la fase 8 (esas van en src/tsp/graficos.py, con
el estilo definitivo para el LaTeX); aqui solo se arma lo minimo para poder
mostrar resultados reales mientras se documenta el avance.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from tsp.datos import leer_tsp, matriz_distancias
from tsp.heuristicas import vecino_mas_cercano
from tsp.metaheuristicas import calcular_T0, recocido_simulado

RAIZ = Path(__file__).resolve().parents[1]
TABLAS = RAIZ / "results" / "tables"
FIGURAS = RAIZ / "results" / "figures"
OPTIMO_BERLIN52 = 7542


def figura_explosion_combinatoria():
    """Tiempo de fuerza bruta vs Held-Karp segun el numero de ciudades (escala log)."""
    df = pd.read_csv(TABLAS / "optimo_subconjuntos.csv")
    fig, ax = plt.subplots(figsize=(6, 4))
    for metodo, grupo in df.groupby("metodo"):
        ax.plot(grupo["n_ciudades"], grupo["tiempo_s"], marker="o", label=metodo)
    ax.set_yscale("log")
    ax.set_xlabel("Numero de ciudades")
    ax.set_ylabel("Tiempo (s, escala log)")
    ax.set_title("Explosion combinatoria: fuerza bruta vs Held-Karp")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURAS / "explosion_combinatoria.png", dpi=150)
    plt.close(fig)


def figura_gap_por_algoritmo():
    """Gap medio y gap de la mejor corrida, por algoritmo (30 semillas sobre berlin52)."""
    df = pd.read_csv(TABLAS / "berlin52_resumen.csv").sort_values("gap_medio_pct")
    fig, ax = plt.subplots(figsize=(6, 4))
    x = range(len(df))
    ax.bar([i - 0.2 for i in x], df["gap_mejor_pct"], width=0.4, label="gap de la mejor corrida")
    ax.bar([i + 0.2 for i in x], df["gap_medio_pct"], width=0.4, label="gap medio (30 semillas)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(df["algo"], rotation=20, ha="right")
    ax.set_ylabel("Gap vs. optimo (%)")
    ax.set_title("Comparacion de algoritmos sobre berlin52")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURAS / "gap_por_algoritmo.png", dpi=150)
    plt.close(fig)


def figura_convergencia(algo, archivo_salida, titulo, etiqueta_x):
    """Curva de convergencia (mejor costo hasta el momento), promedio +/- desviacion entre semillas."""
    df = pd.read_csv(TABLAS / "berlin52_historial.csv")
    sub = df[df["algo"] == algo]
    resumen = sub.groupby("iteracion")["mejor_costo"].agg(["mean", "std"]).reset_index()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(resumen["iteracion"], resumen["mean"], color="C0", label="media (30 semillas)")
    ax.fill_between(
        resumen["iteracion"],
        resumen["mean"] - resumen["std"].fillna(0),
        resumen["mean"] + resumen["std"].fillna(0),
        color="C0", alpha=0.2, label="+/- 1 desviacion",
    )
    ax.axhline(OPTIMO_BERLIN52, color="gray", linestyle="--", label="optimo conocido (7542)")
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel("Mejor costo hasta el momento")
    ax.set_title(titulo)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURAS / archivo_salida, dpi=150)
    plt.close(fig)


def figura_ruta_recocido():
    """Dibuja sobre el mapa de berlin52 la ruta optima encontrada por el recocido simulado."""
    inst = leer_tsp(RAIZ / "data" / "raw" / "berlin52.tsp")
    D = matriz_distancias(inst.coords)
    ruta_inicial = vecino_mas_cercano(D, inicio=0)
    T0 = calcular_T0(ruta_inicial, D, semilla=0)
    mejor_ruta, mejor_costo, _ = recocido_simulado(
        ruta_inicial, D, T0=T0, alpha_cool=0.995, T_min=1e-3, L_iter=500, semilla=0
    )

    orden = mejor_ruta + [mejor_ruta[0]]
    xs = inst.coords[orden, 0]
    ys = inst.coords[orden, 1]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(xs, ys, "-o", color="C0", markersize=4, linewidth=1)
    ax.set_title(f"Ruta final del recocido simulado en berlin52 (L={mejor_costo})")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(FIGURAS / "ruta_recocido_berlin52.png", dpi=150)
    plt.close(fig)


def main():
    FIGURAS.mkdir(parents=True, exist_ok=True)
    figura_explosion_combinatoria()
    figura_gap_por_algoritmo()
    figura_convergencia("recocido_simulado", "convergencia_recocido.png",
                         "Convergencia del recocido simulado (berlin52)", "Nivel de temperatura")
    figura_convergencia("genetico", "convergencia_genetico.png",
                         "Convergencia del algoritmo genetico (berlin52)", "Generacion")
    figura_convergencia("hormigas", "convergencia_hormigas.png",
                         "Convergencia de la colonia de hormigas (berlin52)", "Ronda")
    figura_ruta_recocido()
    print(f"Figuras guardadas en {FIGURAS}")


if __name__ == "__main__":
    main()
