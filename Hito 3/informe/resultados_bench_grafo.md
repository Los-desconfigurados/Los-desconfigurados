
# Resultados del Benchmark del Grafo

Se realizó una comparación de memoria entre la lista de adyacencia y la matriz de adyacencia utilizando grafos sintéticos de 100, 250, 500 y 1.000 vértices, con diferentes densidades de conexiones.

## Tabla de resultados

| Vértices | Densidad | Aristas | Lista estimada (bytes) | Lista medida (bytes) | Matriz estimada (bytes) | Matriz medida (bytes) | Menor memoria |
|---:|---|---:|---:|---:|---:|---:|---|
| 100 | Disperso (grado 4) | 391 | 64.228 | 73.896 | 103.868 | 93.192 | Lista |
| 100 | 5% | 516 | 81.728 | 92.848 | 107.368 | 93.144 | Lista |
| 100 | 25% | 2.523 | 362.708 | 397.912 | 163.564 | 93.144 | Matriz |
| 100 | 50% | 5.032 | 713.968 | 779.280 | 233.816 | 93.144 | Matriz |
| 250 | Disperso (grado 4) | 1.008 | 162.424 | 186.648 | 580.424 | 552.424 | Lista |
| 250 | 5% | 3.084 | 453.064 | 502.200 | 638.552 | 552.424 | Lista |
| 250 | 25% | 15.708 | 2.220.424 | 2.421.048 | 992.024 | 552.424 | Matriz |
| 250 | 50% | 31.086 | 4.373.344 | 4.758.504 | 1.422.608 | 552.424 | Matriz |
| 500 | Disperso (grado 4) | 1.950 | 315.512 | 370.816 | 2.166.816 | 2.112.536 | Lista |
| 500 | 5% | 12.510 | 1.793.912 | 1.975.936 | 2.462.496 | 2.112.536 | Lista |
| 500 | 25% | 62.517 | 8.794.892 | 9.577.000 | 3.862.692 | 2.112.536 | Matriz |
| 500 | 50% | 124.727 | 17.504.292 | 19.037.112 | 5.604.572 | 2.112.536 | Matriz |
| 1.000 | Disperso (grado 4) | 3.957 | 638.932 | 758.320 | 8.975.652 | 8.865.176 | Lista |
| 1.000 | 5% | 49.715 | 7.045.052 | 7.713.536 | 10.256.876 | 8.865.176 | Lista |
| 1.000 | 25% | 250.225 | 35.116.452 | 38.200.928 | 15.871.156 | 8.865.176 | Matriz |
| 1.000 | 50% | 499.139 | 69.964.412 | 76.057.936 | 22.840.748 | 8.865.176 | Matriz |

## Análisis de resultados

Los resultados muestran que la lista de adyacencia utiliza menos memoria en grafos dispersos, mientras que la matriz de adyacencia presenta menor consumo en grafos con mayor densidad de conexiones.
A medida que aumenta el número de vértices y la densidad de las conexiones, se observa un incremento en el consumo de memoria de ambas estructuras. La lista de adyacencia resulta conveniente cuando existen pocas conexiones, mientras que la matriz puede ser más eficiente en memoria en grafos densos.
