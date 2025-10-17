import math
import random
import time
import os
from datetime import datetime, timedelta


class PanelSolar:
    def __init__(self, potencia_nominal=300, num_paneles=10, eficiencia=0.18):
        """
        potencia_nominal: Watts por panel (típico 250-400W)
        num_paneles: Cantidad de paneles
        eficiencia: Eficiencia de conversión (típico 15-22%)
        """
        self.potencia_nominal = potencia_nominal
        self.num_paneles = num_paneles
        self.eficiencia = eficiencia
        self.potencia_total = potencia_nominal * num_paneles
        self.produccion_total = 0
        self.historial_produccion = []

    def calcular_irradiancia(self, hora, mes, latitud=10):
        """
        Calcula la irradiancia solar según hora y mes
        Retorna W/m² (0-1000)
        """
        # Radiación máxima al mediodía (1000 W/m²)
        irradiancia_maxima = 1000

        # Ajuste estacional (hemisferio norte)
        factor_estacional = 1 + 0.2 * math.cos(2 * math.pi * (mes - 6) / 12)

        # Curva solar diaria (usando función sinusoidal)
        if 6 <= hora < 18:  # Solo hay sol entre 6am y 6pm
            # Ángulo solar (máximo al mediodía)
            angulo = math.pi * (hora - 6) / 12
            intensidad = math.sin(angulo)
            irradiancia = irradiancia_maxima * intensidad * factor_estacional
        else:
            irradiancia = 0

        return max(0, irradiancia)

    def calcular_produccion(self, hora, mes, clima='soleado'):
        """
        Calcula la producción de energía en kWh
        """
        irradiancia = self.calcular_irradiancia(hora, mes)

        # Factor climático
        factores_clima = {
            'soleado': 1.0,
            'parcialmente_nublado': 0.6,
            'nublado': 0.3,
            'lluvia': 0.15,
            'tormenta': 0.05
        }
        factor_clima = factores_clima.get(clima, 1.0)

        # Producción en kW
        area_panel = 1.6  # m² por panel típico
        area_total = area_panel * self.num_paneles

        # Energía = Irradiancia × Área × Eficiencia × Factor climático
        produccion_kw = (irradiancia * area_total * self.eficiencia * factor_clima) / 1000

        return produccion_kw


class SistemaElectrico:
    def __init__(self):
        self.consumo_base = 0.5  # kW consumo constante (refrigerador, standby, etc)
        self.electrodomesticos = {
            'refrigerador': {'potencia': 0.15, 'activo': True, 'probabilidad': 1.0},
            'lavadora': {'potencia': 1.5, 'activo': False, 'probabilidad': 0.3},
            'aire_acondicionado': {'potencia': 2.5, 'activo': False, 'probabilidad': 0.5},
            'tv': {'potencia': 0.2, 'activo': False, 'probabilidad': 0.7},
            'computadora': {'potencia': 0.3, 'activo': False, 'probabilidad': 0.6},
            'luces': {'potencia': 0.4, 'activo': False, 'probabilidad': 0.8},
            'microondas': {'potencia': 1.2, 'activo': False, 'probabilidad': 0.2},
            'plancha': {'potencia': 1.8, 'activo': False, 'probabilidad': 0.15}
        }
        self.consumo_actual = 0
        self.consumo_total = 0
        self.historial_consumo = []

    def actualizar_electrodomesticos(self, hora):
        """Actualiza el estado de electrodomesticos según la hora"""
        # Patrón de uso típico
        if 6 <= hora < 9:  # Mañana
            self.electrodomesticos['luces']['probabilidad'] = 0.9
            self.electrodomesticos['tv']['probabilidad'] = 0.5
            self.electrodomesticos['aire_acondicionado']['probabilidad'] = 0.3
            self.electrodomesticos['lavadora']['probabilidad'] = 0.4
        elif 9 <= hora < 12:  # Media mañana
            self.electrodomesticos['luces']['probabilidad'] = 0.2
            self.electrodomesticos['aire_acondicionado']['probabilidad'] = 0.7
            self.electrodomesticos['lavadora']['probabilidad'] = 0.5
        elif 12 <= hora < 14:  # Mediodía
            self.electrodomesticos['microondas']['probabilidad'] = 0.6
            self.electrodomesticos['aire_acondicionado']['probabilidad'] = 0.9
        elif 14 <= hora < 18:  # Tarde
            self.electrodomesticos['aire_acondicionado']['probabilidad'] = 0.8
            self.electrodomesticos['plancha']['probabilidad'] = 0.3
        elif 18 <= hora < 23:  # Noche
            self.electrodomesticos['luces']['probabilidad'] = 1.0
            self.electrodomesticos['tv']['probabilidad'] = 0.9
            self.electrodomesticos['computadora']['probabilidad'] = 0.7
            self.electrodomesticos['aire_acondicionado']['probabilidad'] = 0.6
        else:  # Madrugada
            self.electrodomesticos['luces']['probabilidad'] = 0.1
            self.electrodomesticos['tv']['probabilidad'] = 0.1
            self.electrodomesticos['aire_acondicionado']['probabilidad'] = 0.4

        # Activar/desactivar según probabilidad
        for nombre, electrodomestico in self.electrodomesticos.items():
            if nombre != 'refrigerador':  # El refri siempre está activo
                electrodomestico['activo'] = random.random() < electrodomestico['probabilidad']

    def calcular_consumo(self):
        """Calcula el consumo actual en kW"""
        consumo = self.consumo_base

        for electrodomestico in self.electrodomesticos.values():
            if electrodomestico['activo']:
                consumo += electrodomestico['potencia']

        self.consumo_actual = consumo
        return consumo


class Bateria:
    def __init__(self, capacidad_kwh=10, carga_inicial=50):
        """
        capacidad_kwh: Capacidad total en kWh
        carga_inicial: Porcentaje inicial de carga
        """
        self.capacidad_kwh = capacidad_kwh
        self.carga_actual = (carga_inicial / 100) * capacidad_kwh
        self.historial_carga = []

    def cargar(self, energia_kwh):
        """Carga la batería con excedente solar"""
        espacio_disponible = self.capacidad_kwh - self.carga_actual
        energia_cargada = min(energia_kwh, espacio_disponible)
        self.carga_actual += energia_cargada
        return energia_cargada

    def descargar(self, energia_kwh):
        """Descarga la batería para cubrir déficit"""
        energia_disponible = self.carga_actual
        energia_descargada = min(energia_kwh, energia_disponible)
        self.carga_actual -= energia_descargada
        return energia_descargada

    def get_porcentaje(self):
        """Retorna el porcentaje de carga"""
        return (self.carga_actual / self.capacidad_kwh) * 100


class SimuladorSolar:
    def __init__(self, paneles, sistema_electrico, bateria):
        self.paneles = paneles
        self.sistema = sistema_electrico
        self.bateria = bateria
        self.hora_actual = 6
        self.dia_actual = 1
        self.mes_actual = 1
        self.clima_actual = 'soleado'
        self.energia_red = 0
        self.energia_exportada = 0

        # Estadísticas
        self.total_producido = 0
        self.total_consumido = 0
        self.total_red = 0
        self.total_exportado = 0

    def generar_clima(self):
        """Genera clima aleatorio con probabilidades realistas"""
        climas = ['soleado', 'soleado', 'soleado', 'parcialmente_nublado',
                  'parcialmente_nublado', 'nublado', 'lluvia']
        self.clima_actual = random.choice(climas)

    def simular_hora(self):
        """Simula una hora completa"""
        # Actualizar electrodomésticos
        self.sistema.actualizar_electrodomesticos(self.hora_actual)

        # Producción solar
        produccion = self.paneles.calcular_produccion(self.hora_actual, self.mes_actual, self.clima_actual)
        self.total_producido += produccion

        # Consumo
        consumo = self.sistema.calcular_consumo()
        self.total_consumido += consumo

        # Balance energético
        balance = produccion - consumo

        if balance > 0:  # Excedente
            # Cargar batería
            excedente = self.bateria.cargar(balance)
            # Exportar a la red lo que no cabe en la batería
            exportado = balance - excedente
            self.energia_exportada = exportado
            self.total_exportado += exportado
            self.energia_red = 0
        else:  # Déficit
            deficit = abs(balance)
            # Usar batería
            de_bateria = self.bateria.descargar(deficit)
            # Tomar de la red lo que falta
            de_red = deficit - de_bateria
            self.energia_red = de_red
            self.total_red += de_red
            self.energia_exportada = 0

        # Guardar en historial
        self.paneles.historial_produccion.append(produccion)
        self.sistema.historial_consumo.append(consumo)
        self.bateria.historial_carga.append(self.bateria.get_porcentaje())

        # Avanzar hora
        self.hora_actual += 1
        if self.hora_actual >= 24:
            self.hora_actual = 0
            self.dia_actual += 1
            self.generar_clima()

            if self.dia_actual > 30:
                self.dia_actual = 1
                self.mes_actual += 1
                if self.mes_actual > 12:
                    self.mes_actual = 1

        return {
            'produccion': produccion,
            'consumo': consumo,
            'balance': balance,
            'bateria_pct': self.bateria.get_porcentaje()
        }


def crear_grafico_barra(valor, maximo, ancho=40):
    """Crea una barra de progreso ASCII"""
    porcentaje = min(100, (valor / maximo) * 100) if maximo > 0 else 0
    lleno = int((ancho * porcentaje) / 100)
    vacio = ancho - lleno

    barra = '█' * lleno + '░' * vacio
    return f"[{barra}] {porcentaje:.1f}%"


def crear_grafico_produccion_consumo(produccion, consumo, ancho=50):
    """Gráfico comparativo de producción vs consumo"""
    maximo = max(produccion, consumo, 1)

    prod_lleno = int((ancho * produccion) / maximo)
    cons_lleno = int((ancho * consumo) / maximo)

    barra_prod = '█' * prod_lleno + '░' * (ancho - prod_lleno)
    barra_cons = '█' * cons_lleno + '░' * (ancho - cons_lleno)

    return barra_prod, barra_cons


def icono_clima(clima):
    """Retorna emoji del clima"""
    iconos = {
        'soleado': '☀️',
        'parcialmente_nublado': '⛅',
        'nublado': '☁️',
        'lluvia': '🌧️',
        'tormenta': '⛈️'
    }
    return iconos.get(clima, '☀️')


def limpiar_pantalla():
    """Limpia la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_interfaz(simulador, resultado):
    """Muestra la interfaz principal"""
    limpiar_pantalla()

    print("=" * 80)
    print("☀️  SIMULADOR DE ENERGÍA SOLAR  ☀️".center(80))
    print("=" * 80)

    # Fecha y hora
    print(f"\n📅 Día {simulador.dia_actual} - Mes {simulador.mes_actual} | "
          f"🕐 Hora: {simulador.hora_actual:02d}:00 | "
          f"{icono_clima(simulador.clima_actual)} {simulador.clima_actual.replace('_', ' ').title()}")

    # Panel de producción
    print("\n" + "─" * 80)
    print("⚡ PRODUCCIÓN SOLAR")
    print("─" * 80)
    print(f"🔆 Paneles: {simulador.paneles.num_paneles} × {simulador.paneles.potencia_nominal}W "
          f"= {simulador.paneles.potencia_total}W")
    print(f"📊 Producción actual: {resultado['produccion']:.2f} kW")
    barra_prod, barra_cons = crear_grafico_produccion_consumo(
        resultado['produccion'], resultado['consumo'])
    print(f"   {barra_prod} {resultado['produccion']:.2f} kW")

    # Panel de consumo
    print("\n" + "─" * 80)
    print("🏠 CONSUMO DEL HOGAR")
    print("─" * 80)
    print(f"💡 Consumo actual: {resultado['consumo']:.2f} kW")
    print(f"   {barra_cons} {resultado['consumo']:.2f} kW")

    # Electrodomésticos activos
    activos = [nombre for nombre, e in simulador.sistema.electrodomesticos.items() if e['activo']]
    if activos:
        print(f"\n🔌 Activos: {', '.join(activos)}")

    # Balance energético
    print("\n" + "─" * 80)
    print("⚖️  BALANCE ENERGÉTICO")
    print("─" * 80)
    balance = resultado['balance']
    if balance > 0:
        print(f"✅ Excedente: +{balance:.2f} kW (Cargando batería/Exportando)")
    elif balance < 0:
        print(f"⚠️  Déficit: {balance:.2f} kW (Usando batería/red)")
    else:
        print(f"⚖️  Balanceado: {balance:.2f} kW")

    if simulador.energia_red > 0:
        print(f"🔴 Tomando de la red: {simulador.energia_red:.2f} kW")
    if simulador.energia_exportada > 0:
        print(f"🟢 Exportando a la red: {simulador.energia_exportada:.2f} kW")

    # Batería
    print("\n" + "─" * 80)
    print("🔋 BATERÍA")
    print("─" * 80)
    print(f"Capacidad: {simulador.bateria.capacidad_kwh} kWh | "
          f"Carga actual: {simulador.bateria.carga_actual:.2f} kWh")
    print(f"{crear_grafico_barra(resultado['bateria_pct'], 100)}")

    # Estadísticas acumuladas
    if simulador.dia_actual > 1 or simulador.hora_actual > 6:
        print("\n" + "─" * 80)
        print("📈 ESTADÍSTICAS ACUMULADAS")
        print("─" * 80)
        print(f"☀️  Total producido:    {simulador.total_producido:.2f} kWh")
        print(f"🏠 Total consumido:    {simulador.total_consumido:.2f} kWh")
        print(f"🔴 Total de la red:    {simulador.total_red:.2f} kWh")
        print(f"🟢 Total exportado:    {simulador.total_exportado:.2f} kWh")

        if simulador.total_consumido > 0:
            autosuficiencia = ((simulador.total_consumido - simulador.total_red) /
                               simulador.total_consumido * 100)
            print(f"\n🎯 Autosuficiencia:     {autosuficiencia:.1f}%")

    print("\n" + "=" * 80)


def menu_configuracion():
    """Menú de configuración inicial"""
    limpiar_pantalla()
    print("=" * 80)
    print("⚙️  CONFIGURACIÓN DEL SISTEMA SOLAR  ⚙️".center(80))
    print("=" * 80)

    print("\n🔆 PANELES SOLARES:")
    try:
        num_paneles = int(input("  Número de paneles (10): ") or "10")
        potencia = int(input("  Potencia por panel en W (300): ") or "300")

        print("\n🔋 BATERÍA:")
        capacidad_bat = float(input("  Capacidad en kWh (10): ") or "10")
        carga_inicial = float(input("  Carga inicial en % (50): ") or "50")

        return num_paneles, potencia, capacidad_bat, carga_inicial
    except ValueError:
        print("\n⚠️  Error en los valores, usando configuración predeterminada...")
        time.sleep(2)
        return 10, 300, 10, 50


def main():
    """Función principal"""
    # Configuración
    config = menu_configuracion()

    # Crear sistema
    paneles = PanelSolar(potencia_nominal=config[1], num_paneles=config[0])
    sistema = SistemaElectrico()
    bateria = Bateria(capacidad_kwh=config[2], carga_inicial=config[3])
    simulador = SimuladorSolar(paneles, sistema, bateria)

    # Generar clima inicial
    simulador.generar_clima()

    # Modo de simulación
    print("\n🎮 MODO DE SIMULACIÓN:")
    print("  [1] Automático (simula un día completo)")
    print("  [2] Manual (avanza hora por hora)")
    modo = input("\nSelecciona (1): ").strip() or "1"

    if modo == "1":
        horas = int(input("\n⏰ ¿Cuántas horas simular? (24): ") or "24")
        velocidad = float(input("⚡ Velocidad en segundos (0.5): ") or "0.5")

        for _ in range(horas):
            resultado = simulador.simular_hora()
            mostrar_interfaz(simulador, resultado)
            time.sleep(velocidad)

        print("\n✓ Simulación completada")
        input("\nPresiona Enter para salir...")

    else:
        print("\n🎮 Modo manual: Presiona Enter para avanzar una hora, 'q' para salir")

        while True:
            resultado = simulador.simular_hora()
            mostrar_interfaz(simulador, resultado)

            comando = input("\n⏩ [Enter] Siguiente hora | [q] Salir: ").strip().lower()

            if comando == 'q':
                break

        print("\n✓ Simulación finalizada")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulación interrumpida por el usuario")
    except Exception as e:
        print(f"\n✗ Error: {e}")