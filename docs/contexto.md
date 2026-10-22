# Proyecto TSP — Contexto y plan de implementación (Optimización DS2011, UTEC, ciclo 2026-2)

> Documento de referencia del proyecto. Resume lo que se definió, cómo cambió y cómo quedó la versión final, y da un plan por fases con instrucciones listas para ejecutar.
> Equipo: Denilson (TheBoss), Timana, Alondra, Antony. Docente: Torres Castillo, Victor Antonio.

---

## 1. Cómo usar este archivo

1. Ejecutar **una fase a la vez** (sección 8). Para cada una, revisar el criterio de aceptación antes de pasar a la siguiente.

---

## 2. Qué es el proyecto

**Problema:** TSP (Problema del Vendedor Viajante). Un repartidor sale de un almacén, visita *n* clientes una sola vez cada uno y vuelve al inicio. Se busca el orden que minimiza la distancia total.

**Hilo del informe (cada sección responde la duda que deja la anterior):**
1. El TSP es fácil de enunciar pero difícil de resolver: hay (n−1)!/2 rutas.
2. Los métodos exactos garantizan el óptimo pero no escalan.
3. Las heurísticas son rápidas pero se atascan en óptimos locales.
4. Las metaheurísticas (recocido simulado, genético, hormigas) escapan aceptando empeoramientos de forma controlada.
5. Todas dependen de parámetros y de una función de costo `L(π)`.
6. Aplicación práctica con ACO.

**Conclusión del informe:** con pocos puntos se puede resolver exacto; con muchos, la enumeración es inviable y las metaheurísticas aportan valor. Se combinan: la heurística da la ruta inicial, la metaheurística la mejora y, si el tamaño lo permite, un método exacto certifica.

---

## 3. Estructura acordada y reparto

| Sección | Contenido | Responsable |
|---|---|---|
| 1 | Introducción a la optimización combinatoria | Alondra |
| 2, 2.1 | TSP y formulación matemática (DFJ / MTZ, subtours) | Alondra |
| 2.2 | Complejidad computacional | Timana |
| 3.1 | Métodos exactos (fuerza bruta, Held-Karp, Branch and Bound) | Timana |
| 3.2 | Heurísticas (vecino más cercano, inserción más barata, 2-opt) | Timana |
| **3.3** | **Metaheurísticas (recocido, genético, hormigas)** | **Denilson** |
| 4 | Comparativa exactos vs. heurísticos/metaheurísticos | Antony |
| **5.1** | **Parámetros a ajustar** | **Denilson** |
| **5.2** | **Función objetivo / de costo** | **Denilson** |
| 6.1, 6.2 | Aplicación práctica | Antony |

Informe en LaTeX (Overleaf), presentación en la semana 7.

**Notación acordada (no cambiar):**

| Símbolo | Significado |
|---|---|
| `n` | número de ciudades |
| `V` | conjunto de ciudades |
| `d_ij` | distancia entre ciudades i y j |
| `x_ij` | variable binaria de decisión |
| `π` | permutación que representa una ruta |
| `L(π)` | costo (longitud total) de la ruta, incluye el regreso al origen |

---

## 4. Cómo fue cambiando el proyecto

1. **Inicio.** Se dividió el trabajo en 4 bloques secuenciales para que cada integrante avanzara sin esperar a los demás. El proyecto era **solo teórico** (investigación y redacción, sin código).
2. **Primera versión del LaTeX.** Salió con 19 referencias y una sección 7 extra. Se bajó a **12 referencias**, se **quitó la sección 7** y la estructura volvió a las 6 secciones repartidas.
3. **Estilo.** Se adoptó el preámbulo del ciclo anterior: carátula con `utec_logo.png`, tablas con líneas verticales y `\hline`, `\renewcommand{\arraystretch}{1.3}`, flotantes `[H]`. Se agregaron `algorithm`/`algpseudocode` (pseudocódigos de 3.3) y `booktabs`/`fontenc[T1]` para corregir errores de compilación.
4. **Redacción.** Se pidió menos texto y más exacto, yendo al grano pero explicando lo que se hace. Se corrigió una subsección `Métodos Heurísticos` duplicada (que descuadraba 3.2 y 3.3) y las cifras de memoria de Held-Karp (≈1 GB con n=25, más de 30 GB con n=30). Se añadió una tabla de contraste heurística vs. metaheurística y el cierre de la aplicación conecta con la explosión combinatoria.
5. **Aplicación del informe.** Caso ficticio de 6 puntos (almacén + clientes A–E) resuelto con ACO.
6. **Revisión para la defensa.** Se detectó un punto débil: el ejemplo es ficticio y de solo 6 nodos, y hay que poder mostrar que el resultado de ACO sale de una **ejecución real**. De ahí surge implementar con un **dataset real**.
7. **Ahora (2026-10-21).** Cambio de alcance: además del informe, se **implementa el código** con TSPLIB.

---

## 5. Versión final: decisiones tomadas

| Tema | Decisión |
|---|---|
| Tipo de TSP | Simétrico, distancias euclidianas |
| Función de costo | `L(π) = Σ d(π_i, π_{i+1}) + d(π_n, π_1)` |
| Medida de calidad | Gap relativo `(L − L*) / L* × 100`, con `L*` óptimo conocido |
| Métodos exactos | Fuerza bruta y Held-Karp, solo para validar en subconjuntos pequeños |
| Heurísticas | Vecino más cercano y 2-opt (movimiento 2-opt evaluado con Δ en O(1)) |
| Metaheurísticas | Recocido simulado, algoritmo genético (OX), colonia de hormigas |
| Método de la aplicación | ACO |
| Dataset | **TSPLIB**: `berlin52` (principal) y `eil51` (confirmación) |

**Aplicación del informe (referencia para comparar):** 6 nodos, ruta de referencia 40.3 km, vecino más cercano 25.7 km, ACO y óptimo (fuerza bruta, 60 rutas) 24.9 km, ahorro 38.21 % de distancia. Parámetros usados: m=6, α=1, β=2, ρ=0.5, Q=100, t_max=50.

**Parámetros por método (nombres del informe):**
- Recocido: `T0`, `α` (enfriamiento `T ← α·T`), `T_min`, `L_iter`. Acepta empeoramientos con probabilidad `e^(−Δ/T)`.
- Genético: `N`, `p_c`, `p_m`, `G_max`, `e` (élite). Aptitud `f = 1/L(π)`, selección por torneo, cruce OX, mutación por intercambio o inversión, elitismo.
- ACO: `m`, `α`, `β`, `ρ`, `Q`, `t_max`. Probabilidad ∝ `τ^α · η^β` con `η = 1/d`. Actualización `τ ← (1−ρ)·τ + Σ Q/L_k`.

**Valores de partida propuestos** (salieron de la guía de estudio, **no fueron definidos por el equipo**; se calibran en la fase 6): recocido `α≈0.995` con `T0` tal que acepte ~80 % de empeoramientos al inicio; genético `N=100–200`, `p_c≈0.9`, `p_m≈0.02–0.1`, torneo de 3, élite 1–5; ACO `m=n`, `α=1`, `β=2–5`, `ρ=0.1–0.5`, `Q=100`.

---

## 6. Dataset

| Instancia | Ciudades | Óptimo conocido | Uso |
|---|---|---|---|
| **berlin52** | 52 | **7542** (confirmado en fuente) | Principal |
| eil51 | 51 | 426 (**verificar** contra el archivo de soluciones de TSPLIB) | Confirmación |

- Los archivos `.tsp` traen coordenadas `(x, y)` (`NODE_COORD_SECTION`, tipo `EUC_2D`).
- **Distancia TSPLIB:** euclidiana redondeada al entero más cercano, `int(sqrt(dx²+dy²) + 0.5)`. Los óptimos publicados usan ese redondeo; sin él el gap sale distinto.
- Fuente oficial: sitio TSPLIB95 de la Universidad de Heidelberg (`comopt.ifi.uni-heidelberg.de/software/TSPLIB95/`).
- El óptimo 7542 vale solo para las 52 ciudades completas. Para subconjuntos, el óptimo se calcula con tu propio código.

---

## 7. Estructura del repositorio

La carpeta `src/tsp/` está dividida igual que el informe (una carpeta por subsección de la 3), para que sea fácil ubicar y explicar cada parte:

```
tsp/
├── README.md
├── requirements.txt
├── docs/contexto.md                    # este archivo
├── data/raw/                           # berlin52.tsp, eil51.tsp, optimos_conocidos.csv
├── src/tsp/
│   ├── datos/                          # lectura TSPLIB y función de costo (sección 5.2)
│   │   ├── lector_tsp.py               #   leer_tsp
│   │   └── distancias.py               #   matriz_distancias, longitud_ruta
│   ├── exactos/                        # métodos exactos (sección 3.1)
│   │   ├── fuerza_bruta.py
│   │   └── held_karp.py
│   ├── heuristicas/                    # heurísticas (sección 3.2)
│   │   ├── vecino_cercano.py
│   │   └── dos_opt.py
│   ├── metaheuristicas/                # metaheurísticas (sección 3.3) — fase 4
│   │   ├── recocido.py
│   │   ├── genetico.py
│   │   └── hormigas.py
│   ├── experimentos.py                 # corridas con varias semillas y CSV — fase 5
│   └── graficos.py                     # figuras — fase 8
├── ejecutables/                        # un script corto por fase: corre, imprime y guarda el CSV
├── tests/                              # misma organización que src/tsp/
└── results/{tables,figures}/
```

Python 3.11+, `numpy`, `pandas`, `matplotlib`, `pytest`. Sin librerías de optimización ya hechas: los algoritmos se implementan a mano porque son el objeto del proyecto.

---

## 8. Plan por fases

Cada fase tiene un criterio de aceptación. No avanzar si el criterio no se cumple.

### Fase 0 — Preparación
Crear la estructura de carpetas de la sección 7, `requirements.txt` y un entorno virtual. No escribir algoritmos todavía.
**Aceptación:** el árbol coincide con la sección 7 y `pytest` corre (aunque sin tests).

### Fase 1 — Datos y función de costo ✅
Implementado en `src/tsp/datos/` (`lector_tsp.py`, `distancias.py`).
- `berlin52.tsp` y `eil51.tsp` descargados a `data/raw/` (el sitio oficial no respondió; se usó un mirror verificado, ver nota al final de la sección 10).
- `leer_tsp`: parser propio de `NODE_COORD_SECTION` (tipo `EUC_2D`).
- `matriz_distancias`: redondeo TSPLIB `int(sqrt(dx**2+dy**2)+0.5)`.
- `longitud_ruta(ruta, D)` con regreso al origen: `L(π) = Σ d(π_i, π_{i+1}) + d(π_n, π_1)`.
- Tests en `tests/datos/`: n=52 para berlin52 y n=51 para eil51; D simétrica con diagonal 0.
**Aceptación:** tests en verde. No había un archivo de tour óptimo de berlin52 para comprobar `longitud_ruta` = 7542 directamente; esa comprobación queda cubierta por la fase 2 (validación exacta) y por los gaps de las fases 3 en adelante.

### Fase 2 — Validación exacta en subconjuntos pequeños ✅
Implementado en `src/tsp/exactos/` (`fuerza_bruta.py`, `held_karp.py`): fuerza bruta (fija la ciudad 0, permuta el resto) y Held-Karp (programación dinámica con bitmask, devuelve longitud y ruta).
Tests en `tests/exactos/`: en subconjuntos de las primeras 8, 9 y 10 ciudades de berlin52, fuerza bruta y Held-Karp dan la misma longitud (2551, 2820 y 2826).
`ejecutables/fase2_optimo_subconjuntos.py` genera `results/tables/optimo_subconjuntos.csv` con el óptimo y el tiempo de cada método (más el óptimo de 12 ciudades, solo con Held-Karp: 4056).
**Aceptación:** cumplida — ambos métodos coinciden; el CSV existe.

### Fase 3 — Heurísticas ✅
Implementado en `src/tsp/heuristicas/` (`vecino_cercano.py`, `dos_opt.py`):
- `vecino_mas_cercano(D, inicio)`: desempate determinista (menor índice).
- `dos_opt(ruta, D)`: estrategia de primera mejora. Evalúa cada movimiento con `Δ = d(a,c)+d(b,d)−d(a,b)−d(c,d)` en O(1) y revierte el tramo solo si Δ<0. Termina en óptimo local.
Tests en `tests/heuristicas/`: ambas devuelven permutaciones válidas; 2-opt nunca empeora la ruta de entrada; en el subconjunto de 10 ciudades, 2-opt llega al óptimo exacto (gap 0 %).
`ejecutables/fase3_heuristicas_berlin52.py` corre NN y NN+2-opt en berlin52 completo: NN = 8980 (gap 19.07 %), NN+2-opt = 7967 (gap 5.64 %), guardado en `results/tables/heuristicas_berlin52.csv`.
**Aceptación:** cumplida — NN+2-opt ≤ NN en longitud; gaps dentro del orden de magnitud esperado por el informe.

### Fase 4 — Metaheurísticas
Una por vez (4a, 4b, 4c), cada una en su propio archivo dentro de `src/tsp/metaheuristicas/`, con su test y su script en `ejecutables/`. Como esta parte sí se va a exponer y correr en vivo, los parámetros de cada método van como argumentos con valor por defecto bien visible al inicio de la función (no escondidos ni repetidos en varios lados), para poder cambiarlos y volver a correr sin rebuscar.

**4a — Recocido simulado** ✅
Implementado en `src/tsp/metaheuristicas/recocido.py` con movimiento 2-opt por Δ en O(1): `_movimiento_aleatorio` (el mismo vecindario de 2-opt, elegido al azar), `calcular_T0` (calibra T0 para ~80 % de empeoramientos aceptados al inicio) y `recocido_simulado` (bucle con enfriamiento `T ← alpha_cool·T`). 3 tests en verde.
`ejecutables/fase4a_recocido_berlin52.py`, partiendo de vecino más cercano con `L_iter=500`, llega al **óptimo exacto: 7542 (gap 0 %)**.

**4b — Genético** ✅
Implementado en `src/tsp/metaheuristicas/genetico.py`: `_poblacion_inicial`, `_evaluar` (aptitud `1/L(π)`), `_seleccion_por_torneo` (k=3), `_cruce_ox` (Order Crossover), `_mutacion` (intercambio o inversión, elegido al azar) y `genetico` (bucle con elitismo `e`). 6 tests en verde, incluyendo que cruce y mutación siempre dan permutaciones válidas.
`ejecutables/fase4b_genetico_berlin52.py`, con los valores de partida de la sección 5 (`N=150, p_c=0.9, p_m=0.05, G_max=500, e=3`), da 8610 (gap 14.16 %) — peor que 2-opt. Es esperado: con `p_m` bajo, el genético converge antes de tiempo. Una prueba rápida con varias semillas mostró que subir `p_m` a 0.2–0.3 mejora mucho el resultado (llegó a tocar el óptimo exacto alguna vez) — buena pista para la calibración formal de la fase 6, que justo ajusta `N` y `p_m`.

**4c — ACO (colonia de hormigas)** ✅
Implementado en `src/tsp/metaheuristicas/hormigas.py`: `_matriz_eta` (η=1/d, protegiendo la diagonal), `_probabilidades` (∝ τ^α·η^β), `_construir_ruta` (una hormiga recorre todas las ciudades al azar según esas probabilidades), `_actualizar_feromona` (evapora ρ, refuerza con Q/L_k sobre las aristas de cada hormiga) y `hormigas` (bucle principal). 5 tests en verde, incluyendo el pedido por el plan: con τ inicial uniforme, la probabilidad de la primera decisión es proporcional a `η^β` (se cancela τ^α al ser constante).
`ejecutables/fase4c_hormigas_berlin52.py`, con `m=n, alpha=1, beta=3, rho=0.3, Q=100, t_max=100` (valores de la guía, `beta` y `rho` sin calibrar todavía), da **7911 (gap 4.89 %)** — mejor que el genético y parecido a 2-opt, sin necesitar ningún ajuste fino.

**Aceptación (4a–4c):** cumplida — los tres algoritmos producen permutaciones válidas, son reproducibles con la misma semilla y mejoran claramente una ruta aleatoria en berlin52. Resumen de resultados sobre berlin52 completo con los valores de partida de la guía: recocido 7542 (gap 0 %), hormigas 7911 (gap 4.89 %), 2-opt 7967 (gap 5.64 %), genético 8610 (gap 14.16 %) — ese orden, con las brechas más grandes en los métodos cuyos parámetros (p_m, beta, rho) todavía no se calibran, es justo el punto que desarrolla la fase 6.

### Fase 5 — Experimentos
Implementar `src/tsp/experimentos.py`. Para berlin52: NN, NN+2-opt (determinísticos, 1 corrida) y SA, GA, ACO con 30 semillas (0..29), todos con la misma regla de presupuesto (mismo número de evaluaciones o mismo tope de tiempo; elegir una y documentarla).
Guardar `results/tables/berlin52_runs.csv` con columnas: `instance, algo, config_id, seed, length, gap_pct, time_s`.
Guardar también el historial de convergencia de cada corrida.
Luego generar `results/tables/berlin52_resumen.csv` con mejor, media, desviación, gap de la mejor y gap medio por algoritmo.
**Aceptación:** los dos CSV existen, `gap_pct` usa 7542, ninguna longitud es menor que 7542 (si lo es, hay un error de distancia o de ruta).

### Fase 6 — Calibración de parámetros (sección 5.1)
Con una configuración base por método, variar un parámetro a la vez con 10 semillas (SA: `T0` y `alpha_cool`; GA: `N` y `p_m`; ACO: `rho` y `beta`), con valores bajo/medio/alto.
Guardar `results/tables/calibracion.csv` y una figura por parámetro (media ± desviación del largo final).
Resumir en una tabla qué pasó con valores muy altos y muy bajos, para contrastar con la tabla de la sección 5.1 del informe.
Elegir la configuración final de cada método y guardarla en `config/best.yaml`.
**Aceptación:** la configuración final sale de datos y está guardada; la fase 5 se vuelve a correr con ella.

### Fase 7 — Segunda instancia y cierre del punto débil
Repetir la fase 5 con eil51 (óptimo conocido: verificar el valor en el archivo de soluciones de TSPLIB antes de usarlo). Comparar con berlin52.
**Opcional** (si se aporta la matriz de distancias del caso de 6 nodos del informe): con esa matriz, correr fuerza bruta, vecino más cercano y ACO con `m=6, α=1, β=2, ρ=0.5, Q=100, t_max=50`. Comparar con 40.3 / 25.7 / 24.9 km del informe.
**Aceptación:** tabla comparativa por instancia; si la matriz de 6 nodos se aporta, los resultados reproducen o corrigen las cifras del informe.

### Fase 8 — Entregables
Implementar `src/tsp/graficos.py` y generar las figuras (ruta final de cada algoritmo sobre las coordenadas, curvas de convergencia promedio ± desviación, boxplot de longitudes por algoritmo) en `results/figures/`.
Exportar las tablas finales a LaTeX con el estilo del informe: columnas con líneas verticales y `\hline`, `\renewcommand{\arraystretch}{1.3}` y `[H]`. Escribir `README.md` con cómo reproducir todo (comandos, semillas, versión de Python) y qué sección del informe respalda cada resultado.
**Aceptación:** `README.md` permite reproducir desde cero; figuras y tablas listas para Overleaf.

---

## 9. Reglas de trabajo (código)

- Trabajar una fase a la vez (sección 8) y detenerse al terminar; no adelantar fases sin revisar el criterio de aceptación.
- Python 3.11+, `numpy`, `pandas`, `matplotlib`, `pytest`. Sin librerías de optimización/TSP ya hechas: los algoritmos se implementan a mano, porque son el objeto del proyecto.
- **Nombres en español** (carpetas, archivos, funciones, variables), para que se entiendan sin traducir: `vecino_mas_cercano`, `dos_opt`, `fuerza_bruta`, `longitud_ruta`, `ruta`, etc. Excepciones: nombres propios de algoritmos (`held_karp`) y la notación matemática del informe, que se mantiene tal cual (`n`, `V`, `d_ij`, `π`, `L(π)`, y los parámetros de las metaheurísticas: SA `T0, alpha_cool, T_min, L_iter`; GA `N, p_c, p_m, G_max, e`; ACO `m, alpha, beta, rho, Q, t_max`).
- **El código se expone y se corre en vivo** (el profesor puede pedir cambiar un valor y volver a correr, o preguntar cómo funciona una parte): cada método va en su propio archivo chico y enfocado en una sola cosa (nunca todo junto en uno gigante), organizado en carpetas que calzan con las secciones del informe (`exactos/` ↔ 3.1, `heuristicas/` ↔ 3.2, `metaheuristicas/` ↔ 3.3), y los parámetros de cada función quedan como argumentos con su valor por defecto visible, fáciles de ubicar y cambiar.
- Distancias TSPLIB: `int(sqrt(dx**2+dy**2)+0.5)`. `L(π)` incluye el regreso a la ciudad de origen.
- Gap = `(L − L*)/L* × 100`. Óptimos conocidos: berlin52 = 7542, eil51 = 426 (ver `data/raw/optimos_conocidos.csv`). Si alguna longitud calculada resulta menor que el óptimo, hay un error que corregir.
- Todo algoritmo estocástico recibe una semilla y es reproducible; los experimentos finales se corren con 30 semillas.
- Todo algoritmo devuelve una permutación válida (sin ciudades repetidas ni faltantes); eso se valida con un test.
- Si falta algo (un archivo, la red, un dato) se documenta y se pregunta; no se inventan valores ni resultados.
- Código corto y legible: comentarios breves en español solo donde algo no sea obvio, y una línea de docstring por función explicando qué hace.
- Los resultados (CSV, figuras) van en `results/`, nunca en `src/`.

## 10. Pendientes y dudas abiertas

- **Dónde entran los resultados en el informe.** El informe era teórico: hay que decidir si los resultados reemplazan la aplicación de 6 nodos (6.1, 6.2 de Antony) o se agregan como sección nueva. Hay que coordinarlo con el equipo.
- ~~**Valor de eil51 (426)** sin confirmar en fuente~~ → **confirmado en la fase 1**: el archivo `solutions` oficial de TSPLIB95 lista `eil51 : 426` y `berlin52 : 7542`. Ver `data/raw/optimos_conocidos.csv`.
- **Matriz del caso de 6 nodos:** está en el `.tex` (sección 6.1). Sin ella, la fase 7 opcional no se puede correr.
- **Presupuesto de comparación** (evaluaciones o tiempo) sin definir; se elige en la fase 5 y se documenta.

**Nota sobre la fuente de datos (fase 1):** el sitio oficial `comopt.ifi.uni-heidelberg.de` no respondió al intentar la descarga (timeout). Se usó el mirror público de TSPLIB95 en GitHub (`github.com/mastqe/tsplib`), que contiene los mismos archivos `.tsp` y el archivo `solutions` con los óptimos publicados por TSPLIB. Para la cita bibliográfica en el informe se sigue usando la fuente oficial (TSPLIB95, Universidad de Heidelberg); el mirror es solo el medio de descarga.
