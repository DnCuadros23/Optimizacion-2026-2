"""Pruebas de la fase 5: orquestar corridas con varias semillas y armar el resumen."""
import pandas as pd

from tsp.datos import leer_tsp, matriz_distancias
from tsp.experimentos import ejecutar_experimentos, resumen_por_algoritmo


def test_resumen_por_algoritmo_calcula_bien_las_metricas():
    runs_df = pd.DataFrame([
        {"algo": "x", "length": 100},
        {"algo": "x", "length": 110},
        {"algo": "y", "length": 90},
    ])
    resumen = resumen_por_algoritmo(runs_df, optimo=100)

    fila_x = resumen[resumen["algo"] == "x"].iloc[0]
    assert fila_x["mejor"] == 100
    assert fila_x["media"] == 105
    assert fila_x["gap_mejor_pct"] == 0.0

    fila_y = resumen[resumen["algo"] == "y"].iloc[0]
    assert fila_y["gap_mejor_pct"] == -10.0  # unica corrida de "y", por debajo del optimo de prueba


def test_ejecutar_experimentos_con_pocas_semillas_y_presupuesto_chico(data_dir):
    # parametros chicos solo para que el test corra rapido; la fase 5 "de verdad"
    # usa los PARAMS_* por defecto (ya probados en la fase 4) y 30 semillas
    inst = leer_tsp(data_dir / "berlin52.tsp")
    D = matriz_distancias(inst.coords)

    runs_df, historiales_df = ejecutar_experimentos(
        "berlin52", D, optimo=7542, semillas=range(2),
        params_recocido=dict(alpha_cool=0.9, T_min=1.0, L_iter=20),
        params_genetico=dict(N=20, p_c=0.9, p_m=0.1, G_max=10, e=2),
        params_hormigas=dict(m=10, alpha=1, beta=3, rho=0.3, Q=100, t_max=10),
    )

    # NN y NN+2opt (1 corrida cada uno) + 3 metaheuristicas x 2 semillas
    assert len(runs_df) == 2 + 3 * 2
    assert (runs_df["length"] >= 7542).all()  # ninguna longitud puede ganarle al optimo conocido
    assert not historiales_df.empty
