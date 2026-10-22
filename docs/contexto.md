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

```
tsp/
├── README.md
├── requirements.txt
├── docs/contexto.md              # este archivo
├── data/raw/                     # berlin52.tsp, eil51.tsp
├── src/tsp/
│   ├── io.py                     # parser TSPLIB
│   ├── distance.py               # matriz de distancias, tour_length
│   ├── exact.py                  # fuerza bruta, Held-Karp
│   ├── heuristics.py             # vecino más cercano, 2-opt
│   ├── sa.py  ga.py  aco.py      # metaheurísticas
│   ├── experiments.py            # corridas y CSV
│   └── plots.py                  # figuras
├── tests/
└── results/{tables,figures}/
```

Python 3.11+, `numpy`, `pandas`, `matplotlib`, `pytest`. Sin librerías de optimización ya hechas: los algoritmos se implementan a mano porque son el objeto del proyecto.

---

## 8. Plan por fases

Cada fase tiene un criterio de aceptación. No avanzar si el criterio no se cumple.

### Fase 0 — Preparación
Crear la estructura de carpetas de la sección 7, `requirements.txt` y un entorno virtual. No escribir algoritmos todavía.
**Aceptación:** el árbol coincide con la sección 7 y `pytest` corre (aunque sin tests).

### Fase 1 — Datos y función de costo
Implementar `src/tsp/io.py` y `src/tsp/distance.py`.
- Descargar `berlin52.tsp` y `eil51.tsp` desde el sitio oficial TSPLIB95 a `data/raw/`. Si la descarga falla, documentarlo y esperar a que se coloquen los archivos manualmente.
- Parser propio de `NODE_COORD_SECTION` (tipo `EUC_2D`).
- Matriz de distancias con redondeo TSPLIB: `int(sqrt(dx**2+dy**2)+0.5)`.
- `tour_length(tour, D)` con regreso al origen: `L(π) = Σ d(π_i, π_{i+1}) + d(π_n, π_1)`.
- Tests: n=52 para berlin52 y n=51 para eil51; D simétrica con diagonal 0. Si existe el archivo de tour óptimo de berlin52, su longitud debe dar 7542.
**Aceptación:** tests en verde; `tour_length` del tour óptimo de berlin52 = 7542 (o, si no hay archivo de tour, se documenta que esa validación queda para la fase 2).

### Fase 2 — Validación exacta en subconjuntos pequeños
Implementar `src/tsp/exact.py` con fuerza bruta (fija la ciudad 0, permuta el resto) y Held-Karp (programación dinámica con bitmask, devuelve longitud y ruta).
Tests: en subconjuntos de las primeras 8, 9 y 10 ciudades de berlin52, fuerza bruta y Held-Karp deben dar la misma longitud.
Guardar en `results/tables/optimo_subconjuntos.csv` el óptimo de las primeras 10 y 12 ciudades (Held-Karp para 12). Reportar el tiempo de cada uno.
**Aceptación:** ambos métodos coinciden; el CSV existe. Estos óptimos son la referencia para validar las heurísticas en pequeño.

### Fase 3 — Heurísticas
Implementar `src/tsp/heuristics.py`:
- `nearest_neighbor(D, start)`: desempate determinista (menor índice).
- `two_opt(tour, D)`: primera mejora o mejor mejora (elegir una y documentarla). Evaluar cada movimiento con `Δ = d(a,c)+d(b,d)−d(a,b)−d(c,d)` en O(1) y revertir el tramo solo si Δ<0. Termina en óptimo local.
Tests: ambas devuelven permutaciones válidas; 2-opt nunca empeora la ruta de entrada; en el subconjunto de 10 ciudades, el gap vs. Held-Karp se reporta.
Correr NN y NN+2-opt en berlin52 y reportar longitud y gap vs. 7542.
**Aceptación:** NN+2-opt ≤ NN en longitud; gaps reportados. Como orden de magnitud, el informe esperaba ~25 % para NN y pocos % para 2-opt (no es meta a forzar).

### Fase 4 — Metaheurísticas
Una por vez (4a, 4b, 4c), cada una con su test.

**4a — Recocido simulado**
Implementar `src/tsp/sa.py` con movimiento 2-opt por Δ en O(1).
Parámetros: `T0`, `alpha_cool`, `T_min`, `L_iter` (usar `alpha_cool` para no confundir con α de ACO).
Acepta si Δ≤0, o con probabilidad `exp(−Δ/T)`. Enfriamiento `T ← alpha_cool·T`.
Entrada: ruta inicial (por defecto la de vecino más cercano) y semilla.
Devuelve mejor ruta, su longitud e historial del mejor-hasta-ahora por iteración.
Incluir una función que calcule `T0` para aceptar ~80 % de empeoramientos al inicio.

**4b — Genético**
Implementar `src/tsp/ga.py`: individuo = permutación, aptitud `1/L(π)`, selección por torneo (k=3), cruce OX, mutación por intercambio o inversión, elitismo `e`. Parámetros: `N`, `p_c`, `p_m`, `G_max`, `e`. Semilla fija.
Test: tras cruce y mutación, todo hijo es una permutación válida (sin repetidos ni faltantes).
Devuelve mejor ruta, longitud e historial.

**4c — ACO (Ant System)**
Implementar `src/tsp/aco.py`. Probabilidad de ir a j desde i ∝ `τ_ij^α · η_ij^β` con `η=1/d_ij` entre ciudades no visitadas. Actualización: `τ ← (1−ρ)τ + Σ_k Q/L_k` sobre las aristas de cada hormiga (matriz simétrica). Parámetros: `m`, `α`, `β`, `ρ`, `Q`, `t_max`.
Vectorizar con numpy; proteger `d_ij=0`. Semilla fija. Devuelve mejor ruta, longitud e historial.
Test: con τ inicial uniforme, la probabilidad de la primera decisión es proporcional a `1/d^β`.

**Aceptación (4a–4c):** cada algoritmo produce permutaciones válidas, es reproducible con la misma semilla y mejora claramente a una ruta aleatoria en berlin52.

### Fase 5 — Experimentos
Implementar `src/tsp/experiments.py`. Para berlin52: NN, NN+2-opt (determinísticos, 1 corrida) y SA, GA, ACO con 30 semillas (0..29), todos con la misma regla de presupuesto (mismo número de evaluaciones o mismo tope de tiempo; elegir una y documentarla).
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
Generar las figuras (ruta final de cada algoritmo sobre las coordenadas, curvas de convergencia promedio ± desviación, boxplot de longitudes por algoritmo) en `results/figures/`.
Exportar las tablas finales a LaTeX con el estilo del informe: columnas con líneas verticales y `\hline`, `\renewcommand{\arraystretch}{1.3}` y `[H]`. Escribir `README.md` con cómo reproducir todo (comandos, semillas, versión de Python) y qué sección del informe respalda cada resultado.
**Aceptación:** `README.md` permite reproducir desde cero; figuras y tablas listas para Overleaf.

---

## 9. Reglas de trabajo (código)

- Trabajar una fase a la vez (sección 8) y detenerse al terminar; no adelantar fases sin revisar el criterio de aceptación.
- Python 3.11+, `numpy`, `pandas`, `matplotlib`, `pytest`. Sin librerías de optimización/TSP ya hechas: los algoritmos se implementan a mano, porque son el objeto del proyecto.
- Notación del informe en el código: `n` (número de ciudades), `V` (conjunto de ciudades), `d_ij` (matriz de distancias), `π` (una ruta/permutación), `L(π)` (su costo). Parámetros de las metaheurísticas con los nombres del informe (SA: `T0, alpha_cool, T_min, L_iter`; GA: `N, p_c, p_m, G_max, e`; ACO: `m, alpha, beta, rho, Q, t_max`).
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
