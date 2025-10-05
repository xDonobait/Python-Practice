import random
import time


def lanzar_moneda():
    """Simula el lanzamiento de una moneda"""
    print("\n🪙 Lanzando moneda...")
    time.sleep(1)
    resultado = random.choice(["CARA", "CRUZ"])
    print(f"Resultado: {resultado}")
    return resultado


def lanzar_dados(cantidad=1, caras=6):
    """Simula el lanzamiento de uno o varios dados"""
    print(f"\n🎲 Lanzando {cantidad} dado(s) de {caras} caras...")
    time.sleep(1)

    resultados = [random.randint(1, caras) for _ in range(cantidad)]

    print("Resultados individuales:", resultados)
    print(f"Suma total: {sum(resultados)}")

    return resultados


def menu_principal():
    """Muestra el menú principal y gestiona las opciones"""
    print("\n" + "=" * 50)
    print("🎰 SIMULADOR DE DADOS Y MONEDAS 🎰")
    print("=" * 50)

    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Lanzar una moneda")
        print("2. Lanzar dados")
        print("3. Salir")

        opcion = input("\nElige una opción (1-3): ").strip()

        if opcion == "1":
            lanzar_moneda()

        elif opcion == "2":
            try:
                cantidad = int(input("¿Cuántos dados quieres lanzar? (1-10): "))
                if cantidad < 1 or cantidad > 10:
                    print("❌ Por favor, elige entre 1 y 10 dados.")
                    continue

                caras = int(input("¿Cuántas caras tiene cada dado? (4, 6, 8, 10, 12, 20): "))
                if caras not in [4, 6, 8, 10, 12, 20]:
                    print("❌ Número de caras no válido. Usando dado de 6 caras.")
                    caras = 6

                lanzar_dados(cantidad, caras)

            except ValueError:
                print("❌ Por favor, ingresa números válidos.")

        elif opcion == "3":
            print("\n👋 ¡Gracias por usar el simulador! ¡Buena suerte!")
            break

        else:
            print("❌ Opción no válida. Por favor, elige 1, 2 o 3.")


def modo_rapido():
    """Modo rápido para tomar decisiones rápidas"""
    print("\n⚡ MODO DECISIÓN RÁPIDA")
    print("1. Cara o Cruz")
    print("2. Dado de 6 caras")

    opcion = input("Elige (1-2): ").strip()

    if opcion == "1":
        lanzar_moneda()
    elif opcion == "2":
        lanzar_dados(1, 6)


if __name__ == "__main__":
    # Puedes cambiar entre menu_principal() o modo_rapido()
    menu_principal()