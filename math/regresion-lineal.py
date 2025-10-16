import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Datos
edad = np.array([25, 46, 58, 37, 55, 32, 41, 50, 23, 60])
ausentismo = np.array([18, 12, 8, 15, 10, 13, 7, 9, 16, 6])

# Cálculos intermedios
n = len(edad)
xy = edad * ausentismo
x2 = edad ** 2
y2 = ausentismo ** 2

# Tabla de datos
df = pd.DataFrame({
    "Edad (X)": edad,
    "Ausentismo (Y)": ausentismo,
    "X*Y": xy,
    "X^2": x2,
    "Y^2": y2
})

# Agregar sumatorias al final
suma_fila = pd.DataFrame(df.sum(), columns=["Total"]).T
df = pd.concat([df, suma_fila], ignore_index=True)

# Regresión lineal
slope, intercept, r_value, p_value, std_err = stats.linregress(edad, ausentismo)

# Ecuación de regresión
print(f"Ecuación de regresión: Y = {intercept:.2f} + {slope:.2f}X")
print(f"Coeficiente de correlación (r): {r_value:.3f}")
print(f"Coeficiente de determinación (R^2): {r_value**2:.3f}")

# Mostrar tabla
print("\nTabla con sumatorias:")
print(df)

# Gráfica
plt.scatter(edad, ausentismo, color='blue', label='Datos reales')
plt.plot(edad, intercept + slope * edad, color='red', label='Recta de regresión')
plt.title('Relación entre Edad y Ausentismo')
plt.xlabel('Edad (años)')
plt.ylabel('Ausentismo (días por año)')
plt.legend()
plt.grid(True)
plt.show()
