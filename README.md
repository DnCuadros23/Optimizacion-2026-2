# TSP — Optimización DS2011 (2026-2)

Implementación en código del proyecto del Problema del Vendedor Viajante (TSP):
métodos exactos, heurísticas y metaheurísticas, con experimentos reales sobre
instancias de TSPLIB (`berlin52`, `eil51`). Acompaña al informe teórico del
curso (contexto completo en [`docs/contexto.md`](docs/contexto.md)).

## Cómo reproducir todo

Requiere **Python 3.11+** (probado con 3.13).

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # Windows
# .venv/bin/pip install -r requirements.txt     # Linux/Mac
```

Los tests (reproducibles, deterministas) se corren con:

```bash
python -m pytest
```

Todos los scripts de `ejecutables/` asumen que `src/` está en el `PYTHONPATH`
(ya configurado para `pytest` vía `pyproject.toml`; para correrlos sueltos):

```bash
PYTHONPATH=src python ejecutables/<script>.py
```

## Orden de ejecución

Cada fase tiene su script en `ejecutables/`, en este orden (algunos dependen
de los resultados del anterior):

| # | Script | Qué genera | Tarda |
|---|---|---|---|
| 2 | `fase2_optimo_subconjuntos.py` | `results/tables/optimo_subconjuntos.csv` | segundos |
| 3 | `fase3_heuristicas_berlin52.py` | `results/tables/heuristicas_berlin52.csv` | segundos |
| 4a | `fase4a_recocido_berlin52.py` | `results/tables/recocido_berlin52*.csv` | ~5 s |
| 4b | `fase4b_genetico_berlin52.py` | `results/tables/genetico_berlin52*.csv` | ~2 s |
| 4c | `fase4c_hormigas_berlin52.py` | `results/tables/hormigas_berlin52*.csv` | ~4 s |
| 5 | `fase5_experimentos_berlin52.py` | `results/tables/berlin52_runs.csv`, `..._historial.csv`, `..._resumen.csv` (config base, 30 semillas) | ~5 min |
| 6 | `fase6_calibracion.py` | `results/tables/calibracion.csv`, `calibracion_resumen.csv`, `config/best.yaml` | ~10-12 min |
| 6 | `fase6_rerun_calibrado.py` | `results/tables/berlin52_*_calibrado.csv`, `calibracion_antes_despues.csv` | ~5 min |
| 7 | `fase7_eil51.py` | `results/tables/eil51_*.csv`, `comparacion_instancias.csv` | ~5 min |
| 8 | `fase8_entregables.py` | figuras finales en `results/figures/`, tablas en `results/tables/latex/` | ~1 min |

Todas las corridas con semillas usan `0..29` (experimentos) o `0..9`
(calibración), siempre reproducibles: la misma semilla da siempre el mismo
resultado.

## Notebooks (para correr en vivo en la exposición)

`notebooks/` tiene la misma lógica que `ejecutables/`, pero en celdas
separadas y comentadas, pensada para mostrar y correr en vivo frente al
profesor. Un notebook por fase (`01_datos_y_metodos_exactos.ipynb` ...
`07_entregables.ipynb`), cada parámetro en su propia celda para poder
cambiarlo y volver a correr sin buscar en el código. No repiten corridas
pesadas (30 semillas, calibración completa): corren una demo chica en vivo y
cargan los resultados completos ya guardados en `results/tables/`.

```bash
.venv/Scripts/jupyter notebook notebooks/   # Windows
# .venv/bin/jupyter notebook notebooks/     # Linux/Mac
```

## Qué sección del informe respalda cada resultado

| Sección del informe | Resultado en este repositorio |
|---|---|
| 2.2 Complejidad computacional | `results/tables/optimo_subconjuntos.csv` (explosión combinatoria, fuerza bruta vs. Held-Karp) |
| 3.1 Métodos exactos | `src/tsp/exactos/`, mismo CSV anterior |
| 3.2 Heurísticas | `src/tsp/heuristicas/`, `results/tables/heuristicas_berlin52.csv` |
| 3.3 Metaheurísticas | `src/tsp/metaheuristicas/`, `results/tables/berlin52_resumen_calibrado.csv` |
| 5.1 Parámetros a ajustar | `results/tables/calibracion.csv`, `calibracion_resumen.csv`, `config/best.yaml` |
| 5.2 Función de costo | `src/tsp/datos/distancias.py` (`longitud_ruta`) |
| 6. Aplicación práctica | `results/tables/eil51_resumen.csv`, `comparacion_instancias.csv` (reemplaza/complementa el ejemplo ficticio de 6 nodos con una ejecución real) |

## Estructura

Ver [`docs/contexto.md`](docs/contexto.md) para el plan completo por fases,
las decisiones tomadas y las reglas de trabajo del código.
