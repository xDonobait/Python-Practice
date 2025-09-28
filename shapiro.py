from scipy.stats import shapiro
import numpy as np

# Paso 1: Datos ordenados
datos = [15.2, 14.8, 15.6, 15.0, 14.9, 15.1, 15.3]
datos_ordenados = sorted(datos)

print("📊 Datos ordenados:")
print(datos_ordenados)

# Paso 2: Media y desviación estándar
media = np.mean(datos_ordenados)
std = np.std(datos_ordenados, ddof=1)
print(f"\n📈 Media: {media:.4f}")
print(f"📉 Desviación estándar: {std:.4f}")

# Estadístico de Shapiro-Wilk (lo hace la librería internamente)
W, p_val = shapiro(datos_ordenados)
print(f"\n🔍 Estadístico de prueba W = {W:.4f}")
print(f"🔍 Valor p = {p_val:.4f}")

# Paso 3: Comparación con valor crítico
# OJO: los valores críticos exactos se encuentran en tablas, aquí usamos el p-value
alfa = 0.05
if p_val < alfa:
    print("\n❌ Se rechaza H₀: los datos NO siguen una distribución normal.")
else:
    print("\n✅ No se rechaza H₀: los datos podrían seguir una distribución normal.")
