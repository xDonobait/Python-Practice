import numpy as np
from scipy import stats

# Datos de duración de batería (en horas)
duraciones = np.array([5.2, 5.9, 7.1, 4.2, 6.5, 8.5, 4.6, 6.8, 6.9, 5.8,
                       5.1, 6.5, 7.0, 5.3, 6.2, 5.7, 6.6, 7.5, 5.1, 6.1])

# Parámetro poblacional
media_esperada = 6.0
nivel_confianza = 0.95

# Estadísticos muestrales
media_muestral = np.mean(duraciones)
desv_std_muestral = np.std(duraciones, ddof=1)
n = len(duraciones)
grados_libertad = n - 1

# Estadístico t
error_estandar = desv_std_muestral / np.sqrt(n)
t_stat = (media_muestral - media_esperada) / error_estandar

# Valor crítico para prueba bilateral
valor_critico = stats.t.ppf(1 - (1 - nivel_confianza)/2, df=grados_libertad)

# Resultado
print("Media muestral:", round(media_muestral, 2))
print("Desviación estándar muestral:", round(desv_std_muestral, 2))
print("Error estándar:", round(error_estandar, 2))
print("Estadístico t:", round(t_stat, 2))
print("Valor crítico t:", round(valor_critico, 3))

# Decisión
if abs(t_stat) > valor_critico:
    print("Conclusión: Se rechaza la hipótesis nula. La duración de la batería es significativamente diferente de 6 horas.")
else:
    print("Conclusión: No se rechaza la hipótesis nula. No hay evidencia suficiente para afirmar que la duración de la batería sea diferente de 6 horas.")
