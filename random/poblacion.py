import random
import time
import os


class Poblacion:
    def __init__(self, poblacion_inicial=1000, tasa_natalidad=0.025,
                 tasa_mortalidad=0.015, capacidad_maxima=10000):
        self.poblacion = poblacion_inicial
        self.tasa_natalidad = tasa_natalidad
        self.tasa_mortalidad = tasa_mortalidad
        self.capacidad_maxima = capacidad_maxima
        self.tasa_migracion = 0.0

        # Estadísticas por edad
        self.jovenes = int(poblacion_inicial * 0.25)  # 0-20 años
        self.adultos = int(poblacion_inicial * 0.55)  # 21-60 años
        self.ancianos = int(poblacion_inicial * 0.20)  # 60+ años

        # Historial
        self.historial = [poblacion_inicial]
        self.años_simulados = 0

    def calcular_nacimientos(self):
        """Calcula nacimientos considerando capacidad de carga"""
        factor_hacinamiento = 1 - (self.poblacion / self.capacidad_maxima)
        if factor_hacinamiento < 0:
            factor_hacinamiento = 0

        nacimientos = int(self.adultos * self.tasa_natalidad * factor_hacinamiento)
        return max(0, nacimientos)

    def calcular_muertes(self):
        """Calcula muertes por grupos de edad"""
        muertes_jovenes = int(self.jovenes * self.tasa_mortalidad * 0.5)
        muertes_adultos = int(self.adultos * self.tasa_mortalidad)
        muertes_ancianos = int(self.ancianos * self.tasa_mortalidad * 3)

        return muertes_jovenes + muertes_adultos + muertes_ancianos

    def calcular_migracion(self):
        """Calcula migración neta"""
        return int(self.poblacion * self.tasa_migracion)

    def envejecer_poblacion(self):
        """Simula el envejecimiento natural"""
        # Porcentaje que pasa al siguiente grupo
        jovenes_a_adultos = int(self.jovenes * 0.04)  # 4% por año
        adultos_a_ancianos = int(self.adultos * 0.025)  # 2.5% por año

        self.jovenes -= jovenes_a_adultos
        self.adultos += jovenes_a_adultos - adultos_a_ancianos
        self.ancianos += adultos_a_ancianos

    def aplicar_evento_aleatorio(self):
        """Eventos aleatorios que afectan la población"""
        evento = random.randint(1, 100)

        if evento <= 2:  # 2% de probabilidad - Epidemia
            muertes = int(self.poblacion * random.uniform(0.05, 0.15))
            self.poblacion -= muertes
            return f"💀 EPIDEMIA: -{muertes} habitantes"

        elif evento <= 5:  # 3% de probabilidad - Baby boom
            nacimientos = int(self.adultos * random.uniform(0.1, 0.2))
            self.jovenes += nacimientos
            self.poblacion += nacimientos
            return f"👶 BABY BOOM: +{nacimientos} nacimientos"

        elif evento <= 8:  # 3% de probabilidad - Inmigración masiva
            inmigrantes = int(self.poblacion * random.uniform(0.05, 0.1))
            self.poblacion += inmigrantes
            self.adultos += int(inmigrantes * 0.7)
            self.jovenes += int(inmigrantes * 0.3)
            return f"✈️  INMIGRACIÓN: +{inmigrantes} personas"

        elif evento <= 11:  # 3% de probabilidad - Emigración
            emigrantes = int(self.poblacion * random.uniform(0.05, 0.1))
            self.poblacion -= emigrantes
            return f"🚢 EMIGRACIÓN: -{emigrantes} personas"

        return None

    def simular_año(self):
        """Simula un año completo"""
        # Nacimientos y muertes
        nacimientos = self.calcular_nacimientos()
        muertes = self.calcular_muertes()
        migracion = self.calcular_migracion()

        # Actualizar grupos de edad
        self.jovenes += nacimientos

        # Envejecimiento
        self.envejecer_poblacion()

        # Aplicar cambios
        self.poblacion += nacimientos - muertes + migracion

        # Eventos aleatorios
        evento = self.aplicar_evento_aleatorio()

        # No permitir población negativa
        if self.poblacion < 0:
            self.poblacion = 0

        # Ajustar grupos de edad si hay inconsistencias
        total_grupos = self.jovenes + self.adultos + self.ancianos
        if total_grupos != self.poblacion and self.poblacion > 0:
            factor = self.poblacion / total_grupos if total_grupos > 0 else 0
            self.jovenes = int(self.jovenes * factor)
            self.adultos = int(self.adultos * factor)
            self.ancianos = int(self.ancianos * factor)

        # Guardar en historial
        self.historial.append(self.poblacion)
        self.años_simulados += 1

        return {
            'nacimientos': nacimientos,
            'muertes': muertes,
            'migracion': migracion,
            'evento': evento
        }

    def obtener_estadisticas(self):
        """Retorna estadísticas actuales"""
        if self.poblacion > 0:
            porcentaje_jovenes = (self.jovenes / self.poblacion) * 100
            porcentaje_adultos = (self.adultos / self.poblacion) * 100
            porcentaje_ancianos = (self.ancianos / self.poblacion) * 100
        else:
            porcentaje_jovenes = porcentaje_adultos = porcentaje_ancianos = 0

        return {
            'poblacion_total': self.poblacion,
            'jovenes': self.jovenes,
            'adultos': self.adultos,
            'ancianos': self.ancianos,
            'porcentaje_jovenes': porcentaje_jovenes,
            'porcentaje_adultos': porcentaje_adultos,
            'porcentaje_ancianos': porcentaje_ancianos,
            'capacidad_utilizada': (self.poblacion / self.capacidad_maxima) * 100
        }


def limpiar_pantalla():
    """Limpia la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def crear_grafico_barra(valor, maximo, ancho=50):
    """Crea una barra de progreso ASCII"""
    porcentaje = min(100, (valor / maximo) * 100) if maximo > 0 else 0
    lleno = int((ancho * porcentaje) / 100)
    vacio = ancho - lleno

    barra = '█' * lleno + '░' * vacio
    return f"[{barra}] {porcentaje:.1f}%"


def mostrar_grafico_poblacion(historial, altura=15, ancho=60):
    """Muestra un gráfico ASCII de la evolución de la población"""
    if len(historial) < 2:
        return

    max_pob = max(historial)
    min_pob = min(historial)
    rango = max_pob - min_pob if max_pob != min_pob else 1

    print("\n📊 EVOLUCIÓN DE LA POBLACIÓN")
    print("=" * (ancho + 15))

    for i in range(altura, -1, -1):
        valor = min_pob + (rango * i / altura)
        linea = f"{int(valor):>8} |"

        for j, pob in enumerate(historial[-ancho:]):
            nivel = int(((pob - min_pob) / rango) * altura)
            if nivel == i:
                linea += "●"
            elif nivel > i:
                linea += "│"
            else:
                linea += " "

        print(linea)

    print(" " * 9 + "+" + "─" * len(historial[-ancho:]))
    print(" " * 11 + f"Últimos {min(len(historial), ancho)} años")


def mostrar_interfaz(poblacion, resultado_año):
    """Muestra la interfaz principal"""
    limpiar_pantalla()
    stats = poblacion.obtener_estadisticas()

    print("=" * 70)
    print("🌍  SIMULADOR DE POBLACIÓN  🌍".center(70))
    print("=" * 70)

    print(f"\n⏰ AÑO: {poblacion.años_simulados}")
    print(f"👥 POBLACIÓN TOTAL: {stats['poblacion_total']:,} habitantes")
    print(f"📈 Capacidad máxima: {poblacion.capacidad_maxima:,}")
    print(f"\n{crear_grafico_barra(stats['poblacion_total'], poblacion.capacidad_maxima)}")

    print("\n" + "─" * 70)
    print("📊 DISTRIBUCIÓN POR EDAD:")
    print("─" * 70)
    print(f"👶 Jóvenes (0-20):   {stats['jovenes']:>8,} ({stats['porcentaje_jovenes']:>5.1f}%)")
    print(f"💼 Adultos (21-60):  {stats['adultos']:>8,} ({stats['porcentaje_adultos']:>5.1f}%)")
    print(f"👴 Ancianos (60+):   {stats['ancianos']:>8,} ({stats['porcentaje_ancianos']:>5.1f}%)")

    if resultado_año:
        print("\n" + "─" * 70)
        print("📋 RESUMEN DEL AÑO:")
        print("─" * 70)
        print(f"👶 Nacimientos: +{resultado_año['nacimientos']}")
        print(f"💀 Muertes:     -{resultado_año['muertes']}")
        if resultado_año['migracion'] != 0:
            signo = "+" if resultado_año['migracion'] > 0 else ""
            print(f"✈️  Migración:   {signo}{resultado_año['migracion']}")

        if resultado_año['evento']:
            print(f"\n⚠️  {resultado_año['evento']}")

    # Gráfico de evolución
    if len(poblacion.historial) > 1:
        mostrar_grafico_poblacion(poblacion.historial)

    print("\n" + "=" * 70)


def menu_configuracion():
    """Menú de configuración inicial"""
    limpiar_pantalla()
    print("=" * 70)
    print("⚙️  CONFIGURACIÓN DEL SIMULADOR  ⚙️".center(70))
    print("=" * 70)

    try:
        pob_inicial = int(input("\n👥 Población inicial (1000): ") or "1000")
        tasa_nat = float(input("👶 Tasa de natalidad 0-1 (0.025): ") or "0.025")
        tasa_mort = float(input("💀 Tasa de mortalidad 0-1 (0.015): ") or "0.015")
        capacidad = int(input("📈 Capacidad máxima (10000): ") or "10000")

        return pob_inicial, tasa_nat, tasa_mort, capacidad
    except ValueError:
        print("\n⚠️  Error en los valores, usando configuración predeterminada...")
        time.sleep(2)
        return 1000, 0.025, 0.015, 10000


def main():
    """Función principal"""
    config = menu_configuracion()
    poblacion = Poblacion(config[0], config[1], config[2], config[3])

    modo = input("\n🎮 Modo: [1] Automático [2] Manual (1): ").strip() or "1"

    if modo == "1":
        años = int(input("⏰ ¿Cuántos años simular? (50): ") or "50")
        velocidad = float(input("⚡ Velocidad en segundos (0.5): ") or "0.5")

        resultado = None
        for _ in range(años):
            resultado = poblacion.simular_año()
            mostrar_interfaz(poblacion, resultado)

            if poblacion.poblacion <= 0:
                print("\n💀 La población se ha extinguido...")
                break

            time.sleep(velocidad)

        print("\n✓ Simulación completada")
        input("\nPresiona Enter para salir...")

    else:
        print("\n🎮 Modo manual: Presiona Enter para avanzar un año, 'q' para salir")
        resultado = None

        while True:
            mostrar_interfaz(poblacion, resultado)

            if poblacion.poblacion <= 0:
                print("\n💀 La población se ha extinguido...")
                break

            comando = input("\n⏩ [Enter] Siguiente año | [q] Salir: ").strip().lower()

            if comando == 'q':
                break

            resultado = poblacion.simular_año()

        print("\n✓ Simulación finalizada")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulación interrumpida por el usuario")
    except Exception as e:
        print(f"\n✗ Error: {e}")