"""Prueba rapida de la fase 6: que cada funcion de calibracion arme bien las filas."""
import tsp.calibracion as calibracion
from tsp.datos import leer_tsp, matriz_distancias


def test_calibrar_genetico_arma_filas_por_nivel_y_semilla(data_dir, monkeypatch):
    # semillas y presupuesto chicos, solo para que el test corra rapido
    monkeypatch.setattr(calibracion, "SEMILLAS", range(2))
    monkeypatch.setattr(calibracion, "BASE_GENETICO", dict(N=10, p_c=0.9, p_m=0.05, G_max=5, e=1))

    inst = leer_tsp(data_dir / "berlin52.tsp")
    D = matriz_distancias(inst.coords)

    filas = calibracion.calibrar_genetico(D.shape[0], D, "berlin52", optimo=7542, parametro="p_m", valores=[0.02, 0.1, 0.3])

    assert len(filas) == 3 * 2  # 3 niveles x 2 semillas
    assert {f["nivel"] for f in filas} == {"bajo", "medio", "alto"}
    assert all(f["length"] >= 7542 for f in filas)
