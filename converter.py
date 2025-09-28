import requests
import json
from typing import Dict, Optional


class TemperatureConverter:

    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        return (celsius * 9 / 5) + 32

    @staticmethod
    def celsius_to_kelvin(celsius: float) -> float:
        return celsius + 273.15

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        return (fahrenheit - 32) * 5 / 9

    @staticmethod
    def fahrenheit_to_kelvin(fahrenheit: float) -> float:
        return TemperatureConverter.fahrenheit_to_celsius(fahrenheit) + 273.15

    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        return kelvin - 273.15

    @staticmethod
    def kelvin_to_fahrenheit(kelvin: float) -> float:
        return TemperatureConverter.celsius_to_fahrenheit(kelvin - 273.15)


class DistanceConverter:
    CONVERSION_FACTORS = {
        'mm': 0.001,
        'cm': 0.01,
        'm': 1.0,
        'km': 1000.0,
        'in': 0.0254,
        'ft': 0.3048,
        'yd': 0.9144,
        'mi': 1609.34
    }

    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str) -> float:
        if from_unit not in cls.CONVERSION_FACTORS or to_unit not in cls.CONVERSION_FACTORS:
            raise ValueError("Unidad no válida")

        meters = value * cls.CONVERSION_FACTORS[from_unit]
        result = meters / cls.CONVERSION_FACTORS[to_unit]
        return result


class WeightConverter:
    CONVERSION_FACTORS = {
        'mg': 0.001,
        'g': 1.0,
        'kg': 1000.0,
        'oz': 28.3495,
        'lb': 453.592,
        'ton': 1000000.0
    }

    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str) -> float:
        if from_unit not in cls.CONVERSION_FACTORS or to_unit not in cls.CONVERSION_FACTORS:
            raise ValueError("Unidad no válida")

        grams = value * cls.CONVERSION_FACTORS[from_unit]
        result = grams / cls.CONVERSION_FACTORS[to_unit]
        return result


class CurrencyConverter:

    def __init__(self):
        self.base_url = "https://api.exchangerate-api.com/v4/latest/"
        self.rates = {}
        self.last_update = None

    def get_exchange_rates(self, base_currency: str = "USD") -> Dict:
        try:
            response = requests.get(f"{self.base_url}{base_currency}", timeout=10)
            response.raise_for_status()
            data = response.json()
            self.rates = data.get('rates', {})
            self.last_update = data.get('date', 'Desconocido')
            return self.rates
        except requests.RequestException as e:
            print(f"Error al obtener tasas de cambio: {e}")
            return {}

    def convert(self, amount: float, from_currency: str, to_currency: str) -> Optional[float]:
        if not self.rates:
            self.get_exchange_rates()

        if not self.rates:
            return None

        try:
            if from_currency == "USD":
                rate = self.rates.get(to_currency)
                if rate:
                    return amount * rate
            elif to_currency == "USD":
                rate = self.rates.get(from_currency)
                if rate:
                    return amount / rate
            else:
                usd_amount = amount / self.rates.get(from_currency, 1)
                return usd_amount * self.rates.get(to_currency, 1)
        except (KeyError, ZeroDivisionError):
            return None

        return None


def show_menu():
    print("\n" + "=" * 50)
    print("          CONVERSOR DE UNIDADES")
    print("=" * 50)
    print("1. Temperatura")
    print("2. Distancia")
    print("3. Peso")
    print("4. Moneda")
    print("5. Salir")
    print("-" * 50)


def temperature_menu():
    print("\n--- CONVERSOR DE TEMPERATURA ---")
    print("1. Celsius → Fahrenheit")
    print("2. Celsius → Kelvin")
    print("3. Fahrenheit → Celsius")
    print("4. Fahrenheit → Kelvin")
    print("5. Kelvin → Celsius")
    print("6. Kelvin → Fahrenheit")

    choice = input("\nSelecciona una opción (1-6): ")

    try:
        value = float(input("Ingresa el valor: "))

        conversions = {
            '1': lambda x: TemperatureConverter.celsius_to_fahrenheit(x),
            '2': lambda x: TemperatureConverter.celsius_to_kelvin(x),
            '3': lambda x: TemperatureConverter.fahrenheit_to_celsius(x),
            '4': lambda x: TemperatureConverter.fahrenheit_to_kelvin(x),
            '5': lambda x: TemperatureConverter.kelvin_to_celsius(x),
            '6': lambda x: TemperatureConverter.kelvin_to_fahrenheit(x)
        }

        if choice in conversions:
            result = conversions[choice](value)
            print(f"Resultado: {result:.2f}")
        else:
            print("Opción no válida")

    except ValueError:
        print("Error: Ingresa un número válido")


def distance_menu():
    print("\n--- CONVERSOR DE DISTANCIA ---")
    units = list(DistanceConverter.CONVERSION_FACTORS.keys())
    print("Unidades disponibles:", ", ".join(units))

    try:
        value = float(input("Ingresa el valor: "))
        from_unit = input("Unidad origen: ").lower()
        to_unit = input("Unidad destino: ").lower()

        result = DistanceConverter.convert(value, from_unit, to_unit)
        print(f"Resultado: {value} {from_unit} = {result:.6f} {to_unit}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: Ingresa valores válidos")


def weight_menu():
    print("\n--- CONVERSOR DE PESO ---")
    units = list(WeightConverter.CONVERSION_FACTORS.keys())
    print("Unidades disponibles:", ", ".join(units))

    try:
        value = float(input("Ingresa el valor: "))
        from_unit = input("Unidad origen: ").lower()
        to_unit = input("Unidad destino: ").lower()

        result = WeightConverter.convert(value, from_unit, to_unit)
        print(f"Resultado: {value} {from_unit} = {result:.6f} {to_unit}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: Ingresa valores válidos")


def currency_menu():
    print("\n--- CONVERSOR DE MONEDA ---")
    print("Monedas comunes: USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, MXN, COP")

    try:
        converter = CurrencyConverter()
        print("Obteniendo tasas de cambio...")

        amount = float(input("Ingresa la cantidad: "))
        from_currency = input("Moneda origen (ej. USD): ").upper()
        to_currency = input("Moneda destino (ej. EUR): ").upper()

        result = converter.convert(amount, from_currency, to_currency)

        if result is not None:
            print(f"Resultado: {amount} {from_currency} = {result:.4f} {to_currency}")
            print(f"Última actualización: {converter.last_update}")
        else:
            print("Error: No se pudo realizar la conversión")

    except ValueError:
        print("Error: Ingresa valores válidos")
    except Exception as e:
        print(f"Error: {e}")


def main():
    print("¡Bienvenido al Conversor de Unidades!")

    while True:
        show_menu()
        choice = input("Selecciona una opción: ")

        if choice == '1':
            temperature_menu()
        elif choice == '2':
            distance_menu()
        elif choice == '3':
            weight_menu()
        elif choice == '4':
            currency_menu()
        elif choice == '5':
            print("¡Gracias por usar el conversor!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

        input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    main()