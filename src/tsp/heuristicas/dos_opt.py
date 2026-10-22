"""2-opt: toma una ruta ya armada (por ejemplo, la de vecino más cercano) y la mejora
invirtiendo tramos, hasta quedar en un óptimo local (ninguna inversión ya ayuda).
"""
import numpy as np


def dos_opt(ruta, D: np.ndarray):
    """Mejora local 2-opt con estrategia de primera mejora (first improvement).

    Para cada par de aristas (a,b) y (c,d) de la ruta, invertir el tramo entre
    ellas cambia el costo en Δ = d(a,c) + d(b,d) − d(a,b) − d(c,d). En cuanto
    se encuentra un Δ<0 se aplica de inmediato y se reinicia el barrido; el
    resultado es un óptimo local: ninguna de esas inversiones ya mejora la ruta.
    """
    ruta = list(ruta)
    n = len(ruta)
    hay_mejora = True

    while hay_mejora:
        hay_mejora = False
        for i in range(n - 1):
            a, b = ruta[i], ruta[i + 1]
            for j in range(i + 2, n):
                c, d = ruta[j], ruta[(j + 1) % n]
                if d == a:
                    continue  # aristas adyacentes (comparten la ciudad a): no es un movimiento 2-opt válido
                delta = D[a, c] + D[b, d] - D[a, b] - D[c, d]
                if delta < 0:
                    ruta[i + 1:j + 1] = reversed(ruta[i + 1:j + 1])
                    hay_mejora = True
                    break  # primera mejora: se aplica el cambio y se reinicia el barrido
            if hay_mejora:
                break

    return ruta
