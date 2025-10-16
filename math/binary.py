import os
import time
from typing import List


class BinaryConverter:
    """Conversor entre texto y binario con múltiples funcionalidades"""

    @staticmethod
    def text_to_binary(text: str, separator: str = " ") -> str:
        """Convierte texto a binario"""
        binary_values = []
        for char in text:
            # Obtener el código ASCII/Unicode del carácter
            ascii_value = ord(char)
            # Convertir a binario (sin el prefijo '0b')
            binary = bin(ascii_value)[2:]
            # Rellenar con ceros a la izquierda para tener 8 bits mínimo
            binary = binary.zfill(8)
            binary_values.append(binary)

        return separator.join(binary_values)

    @staticmethod
    def binary_to_text(binary: str) -> str:
        """Convierte binario a texto"""
        # Eliminar espacios y dividir en grupos de 8 bits
        binary = binary.replace(" ", "").replace("\n", "")

        # Dividir en chunks de 8 bits
        chunks = [binary[i:i + 8] for i in range(0, len(binary), 8)]

        text = ""
        for chunk in chunks:
            if len(chunk) == 8:
                # Convertir de binario a decimal
                decimal_value = int(chunk, 2)
                # Convertir a carácter
                text += chr(decimal_value)

        return text

    @staticmethod
    def text_to_hex(text: str, separator: str = " ") -> str:
        """Convierte texto a hexadecimal"""
        hex_values = [hex(ord(char))[2:].upper().zfill(2) for char in text]
        return separator.join(hex_values)

    @staticmethod
    def hex_to_text(hex_string: str) -> str:
        """Convierte hexadecimal a texto"""
        hex_string = hex_string.replace(" ", "").replace("\n", "")
        chunks = [hex_string[i:i + 2] for i in range(0, len(hex_string), 2)]
        return "".join(chr(int(chunk, 16)) for chunk in chunks if chunk)

    @staticmethod
    def visualize_binary_animation(text: str, delay: float = 0.05):
        """Muestra una animación de conversión a binario"""
        clear_screen()
        print("\n🔄 CONVERSIÓN EN PROGRESO...\n")

        for i, char in enumerate(text):
            ascii_val = ord(char)
            binary = bin(ascii_val)[2:].zfill(8)

            print(f"  Carácter: '{char}'")
            print(f"  ASCII: {ascii_val}")
            print(f"  Binario: ", end="")

            # Animar bit por bit
            for bit in binary:
                print(bit, end="", flush=True)
                time.sleep(delay)

            print("\n")
            time.sleep(delay * 2)

    @staticmethod
    def get_statistics(text: str) -> dict:
        """Obtiene estadísticas del texto"""
        binary = BinaryConverter.text_to_binary(text, separator="")

        return {
            "caracteres": len(text),
            "bits": len(binary),
            "bytes": len(binary) // 8,
            "unos": binary.count("1"),
            "ceros": binary.count("0"),
            "densidad_unos": (binary.count("1") / len(binary) * 100) if binary else 0
        }

    @staticmethod
    def create_ascii_table(start: int = 32, end: int = 126):
        """Crea una tabla ASCII con sus representaciones"""
        print("\n📊 TABLA ASCII\n")
        print(f"{'Dec':<6} {'Hex':<6} {'Bin':<12} {'Char':<6}")
        print("-" * 35)

        for i in range(start, end + 1):
            char = chr(i)
            hex_val = hex(i)[2:].upper()
            bin_val = bin(i)[2:].zfill(8)

            # Manejar caracteres especiales
            display_char = char if char.isprintable() else "·"

            print(f"{i:<6} {hex_val:<6} {bin_val:<12} {display_char:<6}")

            if (i - start + 1) % 20 == 0 and i != end:
                input("\nPresiona Enter para continuar...")
                print()


def clear_screen():
    """Limpia la pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Imprime el encabezado"""
    print("\n" + "=" * 70)
    print("              CONVERSOR DE TEXTO Y BINARIO")
    print("=" * 70)


def print_menu():
    """Imprime el menú principal"""
    print("\n📋 OPCIONES:")
    print("\n  Conversiones básicas:")
    print("    1. Texto → Binario")
    print("    2. Binario → Texto")
    print("    3. Texto → Hexadecimal")
    print("    4. Hexadecimal → Texto")

    print("\n  Herramientas:")
    print("    5. Conversión animada")
    print("    6. Estadísticas del texto")
    print("    7. Comparar texto vs binario")
    print("    8. Tabla ASCII")

    print("\n  Calculadoras:")
    print("    9. Carácter → Binario (individual)")
    print("    10. Número → Binario")

    print("\n    0. Salir")


def option_text_to_binary():
    """Opción: Texto a binario"""
    text = input("\n📝 Ingresa el texto: ")

    separator = input("Separador (Enter para espacio): ") or " "

    binary = BinaryConverter.text_to_binary(text, separator)

    print("\n✅ RESULTADO:")
    print(f"\nTexto original: {text}")
    print(f"Binario: {binary}")
    print(f"\nTotal de bits: {len(binary.replace(separator, ''))}")


def option_binary_to_text():
    """Opción: Binario a texto"""
    print("\n📝 Ingresa el binario (puedes usar espacios o no):")
    binary = input()

    try:
        text = BinaryConverter.binary_to_text(binary)
        print("\n✅ RESULTADO:")
        print(f"\nBinario: {binary}")
        print(f"Texto: {text}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def option_text_to_hex():
    """Opción: Texto a hexadecimal"""
    text = input("\n📝 Ingresa el texto: ")

    separator = input("Separador (Enter para espacio): ") or " "

    hex_result = BinaryConverter.text_to_hex(text, separator)

    print("\n✅ RESULTADO:")
    print(f"\nTexto original: {text}")
    print(f"Hexadecimal: {hex_result}")


def option_hex_to_text():
    """Opción: Hexadecimal a texto"""
    print("\n📝 Ingresa el hexadecimal:")
    hex_string = input()

    try:
        text = BinaryConverter.hex_to_text(hex_string)
        print("\n✅ RESULTADO:")
        print(f"\nHexadecimal: {hex_string}")
        print(f"Texto: {text}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def option_animated_conversion():
    """Opción: Conversión animada"""
    text = input("\n📝 Ingresa el texto (máximo 20 caracteres): ")[:20]

    BinaryConverter.visualize_binary_animation(text)

    print("\n✅ Conversión completa:")
    print(f"Texto: {text}")
    print(f"Binario: {BinaryConverter.text_to_binary(text)}")


def option_statistics():
    """Opción: Estadísticas del texto"""
    text = input("\n📝 Ingresa el texto: ")

    stats = BinaryConverter.get_statistics(text)

    print("\n📊 ESTADÍSTICAS:")
    print(f"\n  Caracteres: {stats['caracteres']}")
    print(f"  Bits totales: {stats['bits']}")
    print(f"  Bytes: {stats['bytes']}")
    print(f"  Unos (1): {stats['unos']}")
    print(f"  Ceros (0): {stats['ceros']}")
    print(f"  Densidad de unos: {stats['densidad_unos']:.2f}%")

    # Visualización de densidad
    bar_length = 50
    ones_bar = int(stats['densidad_unos'] / 100 * bar_length)
    zeros_bar = bar_length - ones_bar

    print(f"\n  Densidad visual:")
    print(f"  [{'█' * ones_bar}{'░' * zeros_bar}]")


def option_compare():
    """Opción: Comparar texto vs binario"""
    text = input("\n📝 Ingresa el texto: ")

    binary = BinaryConverter.text_to_binary(text, "")
    hex_val = BinaryConverter.text_to_hex(text, "")

    print("\n📊 COMPARACIÓN:")
    print(f"\n{'Formato':<15} {'Representación':<40} {'Tamaño'}")
    print("-" * 70)
    print(f"{'Texto':<15} {text:<40} {len(text)} caracteres")
    print(f"{'Binario':<15} {binary[:40]}... {len(binary)} bits")
    print(f"{'Hexadecimal':<15} {hex_val[:40]}... {len(hex_val)} dígitos")

    print(f"\n💾 Eficiencia:")
    print(f"  Texto: {len(text)} bytes")
    print(f"  Binario: {len(binary) // 8} bytes")
    print(f"  Hexadecimal: {len(hex_val) // 2} bytes")


def option_char_to_binary():
    """Opción: Carácter a binario (individual)"""
    char = input("\n📝 Ingresa un carácter: ")

    if len(char) != 1:
        print("❌ Por favor ingresa solo un carácter")
        return

    ascii_val = ord(char)
    binary = bin(ascii_val)[2:].zfill(8)
    hex_val = hex(ascii_val)[2:].upper()

    print("\n✅ RESULTADO:")
    print(f"\n  Carácter: '{char}'")
    print(f"  ASCII/Unicode: {ascii_val}")
    print(f"  Binario: {binary}")
    print(f"  Hexadecimal: {hex_val}")

    # Visualización de bits
    print(f"\n  Visualización de bits:")
    print(f"  {'Posición:':<12} 7  6  5  4  3  2  1  0")
    print(f"  {'Bit:':<12} {' '.join(binary)}")
    print(f"  {'Valor:':<12} {128:>2} {64:>2} {32:>2} {16:>2} {8:>2} {4:>2} {2:>2} {1:>2}")


def option_number_to_binary():
    """Opción: Número a binario"""
    try:
        num = int(input("\n📝 Ingresa un número entero: "))

        binary = bin(num)[2:] if num >= 0 else bin(num)[3:]
        octal = oct(num)[2:] if num >= 0 else oct(num)[3:]
        hexadecimal = hex(num)[2:].upper() if num >= 0 else hex(num)[3:].upper()

        print("\n✅ RESULTADO:")
        print(f"\n  Decimal: {num}")
        print(f"  Binario: {binary}")
        print(f"  Octal: {octal}")
        print(f"  Hexadecimal: {hexadecimal}")

        if num >= 0 and num <= 255:
            print(f"\n  Como carácter ASCII: '{chr(num)}'")

    except ValueError:
        print("\n❌ Error: Ingresa un número válido")


def main():
    """Función principal"""
    while True:
        clear_screen()
        print_header()
        print_menu()

        choice = input("\n➤ Selecciona una opción: ")

        try:
            if choice == "0":
                print("\n¡Hasta luego! 👋\n")
                break
            elif choice == "1":
                option_text_to_binary()
            elif choice == "2":
                option_binary_to_text()
            elif choice == "3":
                option_text_to_hex()
            elif choice == "4":
                option_hex_to_text()
            elif choice == "5":
                option_animated_conversion()
            elif choice == "6":
                option_statistics()
            elif choice == "7":
                option_compare()
            elif choice == "8":
                BinaryConverter.create_ascii_table()
            elif choice == "9":
                option_char_to_binary()
            elif choice == "10":
                option_number_to_binary()
            else:
                print("\n❌ Opción inválida")

        except Exception as e:
            print(f"\n❌ Error: {e}")

        input("\n Presiona Enter para continuar...")


if __name__ == "__main__":
    main()