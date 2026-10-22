"""Pruebas de las figuras y de la exportacion a tablas LaTeX."""
import numpy as np
import pandas as pd

from tsp.graficos import figura_boxplot, figura_convergencia, figura_ruta, tabla_a_latex


def test_tabla_a_latex_tiene_el_estilo_del_informe():
    df = pd.DataFrame([{"algoritmo": "recocido_simulado", "gap_pct": 0.0}])
    latex = tabla_a_latex(df, caption="Resultados", label="tab:resultados")

    assert r"\begin{table}[H]" in latex
    assert r"\renewcommand{\arraystretch}{1.3}" in latex
    assert r"\hline" in latex
    assert r"recocido\_simulado" in latex  # el guion bajo se escapa para LaTeX
    assert r"\caption{Resultados}" in latex
    assert r"\label{tab:resultados}" in latex


def test_figura_ruta_genera_un_archivo(tmp_path):
    coords = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
    salida = tmp_path / "ruta.png"
    figura_ruta(coords, [0, 1, 2, 3], "ruta de prueba", salida)
    assert salida.exists()


def test_figura_convergencia_genera_un_archivo(tmp_path):
    historial_df = pd.DataFrame([
        {"algo": "recocido_simulado", "seed": s, "iteracion": i, "mejor_costo": 100 - i}
        for s in range(3) for i in range(5)
    ])
    salida = tmp_path / "convergencia.png"
    figura_convergencia(historial_df, "recocido_simulado", optimo=90, titulo="t", etiqueta_x="iter", archivo_salida=salida)
    assert salida.exists()


def test_figura_boxplot_genera_un_archivo(tmp_path):
    runs_df = pd.DataFrame([
        {"algo": "recocido_simulado", "seed": s, "length": 100 + s} for s in range(5)
    ] + [
        {"algo": "nearest_neighbor", "seed": None, "length": 130},
    ])
    salida = tmp_path / "boxplot.png"
    figura_boxplot(runs_df, "titulo", salida)
    assert salida.exists()
