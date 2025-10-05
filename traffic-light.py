import time
import os


def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_semaforo(estado):
    limpiar_consola()

    print("\n" + "=" * 40)
    print("     SIMULADOR DE SEMÁFORO")
    print("=" * 40 + "\n")

    if estado == "ROJO":
        print("        ⬤ ROJO - DETENTE")
    else:
        print("        ○ Rojo")

    print()

    if estado == "AMARILLO":
        print("        ⬤ AMARILLO - PRECAUCIÓN")
    else:
        print("        ○ Amarillo")

    print()

    if estado == "VERDE":
        print("        ⬤ VERDE - AVANZA")
    else:
        print("        ○ Verde")

    print("\n" + "=" * 40)
    print("Presiona Ctrl+C para detener")
    print("=" * 40 + "\n")


def simulador_semaforo():
    tiempos = {
        "VERDE": 5,
        "AMARILLO": 2,
        "ROJO": 5
    }

    estados = ["VERDE", "AMARILLO", "ROJO"]

    print("\n¡Iniciando simulador de semáforo!\n")
    time.sleep(1)

    try:
        while True:
            for estado in estados:
                mostrar_semaforo(estado)
                time.sleep(tiempos[estado])

    except KeyboardInterrupt:
        limpiar_consola()
        print("\n✓ Simulador detenido. ¡Hasta pronto!\n")


if __name__ == "__main__":
    simulador_semaforo()