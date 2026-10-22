"""Prueba del parser de config/best.yaml."""
from tsp.config import leer_config


def test_leer_config_convierte_tipos_correctamente(tmp_path):
    archivo = tmp_path / "best.yaml"
    archivo.write_text(
        "# comentario\n"
        "recocido_simulado:\n"
        "  alpha_cool: 0.995\n"
        "  L_iter: 500\n"
        "  T0: 1234.5\n"
        "hormigas:\n"
        "  m: None\n"
        "  beta: 3\n",
        encoding="utf-8",
    )

    config = leer_config(archivo)

    assert config["recocido_simulado"]["alpha_cool"] == 0.995
    assert config["recocido_simulado"]["L_iter"] == 500
    assert isinstance(config["recocido_simulado"]["L_iter"], int)
    assert config["hormigas"]["m"] is None
    assert config["hormigas"]["beta"] == 3
