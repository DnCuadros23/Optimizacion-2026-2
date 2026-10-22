"""Lee config/best.yaml: la configuración final de cada metaheurística, elegida en la fase 6.

No se usa una librería de YAML completa porque el archivo que se escribe
tiene un formato muy simple (un método por bloque, parámetros indentados
debajo); alcanza con un parser chico hecho a medida.
"""


def _convertir(texto):
    """Convierte el texto de un valor a su tipo real: None, int, float o string."""
    if texto == "None":
        return None
    try:
        return int(texto)
    except ValueError:
        pass
    try:
        return float(texto)
    except ValueError:
        pass
    return texto


def leer_config(ruta):
    """Lee un archivo con el formato de config/best.yaml y devuelve {metodo: {parametro: valor}}."""
    config = {}
    metodo_actual = None
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            if linea.strip().startswith("#") or not linea.strip():
                continue
            if not linea.startswith(" "):
                metodo_actual = linea.strip().rstrip(":")
                config[metodo_actual] = {}
            else:
                clave, valor = linea.strip().split(":", 1)
                config[metodo_actual][clave.strip()] = _convertir(valor.strip())
    return config
