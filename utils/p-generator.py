import random
import string
import secrets
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
import re


class PasswordStrength(Enum):
    WEAK = "débil"
    MEDIUM = "medio"
    STRONG = "fuerte"
    VERY_STRONG = "muy fuerte"


class PasswordConfig:
    def __init__(self):
        self.length = 12
        self.include_lowercase = True
        self.include_uppercase = True
        self.include_digits = True
        self.include_symbols = True
        self.exclude_ambiguous = False
        self.custom_symbols = ""
        self.exclude_chars = ""
        self.require_each_type = True

    def to_dict(self) -> Dict:
        return {
            'length': self.length,
            'include_lowercase': self.include_lowercase,
            'include_uppercase': self.include_uppercase,
            'include_digits': self.include_digits,
            'include_symbols': self.include_symbols,
            'exclude_ambiguous': self.exclude_ambiguous,
            'custom_symbols': self.custom_symbols,
            'exclude_chars': self.exclude_chars,
            'require_each_type': self.require_each_type
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'PasswordConfig':
        config = cls()
        for key, value in data.items():
            if hasattr(config, key):
                setattr(config, key, value)
        return config


class PasswordStats:
    def __init__(self):
        self.passwords_generated = 0
        self.generation_history = []
        self.strength_counts = {strength.value: 0 for strength in PasswordStrength}
        self.average_length = 0
        self.most_common_length = 0

    def add_password(self, length: int, strength: PasswordStrength):
        self.passwords_generated += 1
        self.generation_history.append({
            'timestamp': datetime.now().isoformat(),
            'length': length,
            'strength': strength.value
        })
        self.strength_counts[strength.value] += 1
        self._update_averages()

    def _update_averages(self):
        if not self.generation_history:
            return

        lengths = [entry['length'] for entry in self.generation_history]
        self.average_length = sum(lengths) / len(lengths)

        length_counts = {}
        for length in lengths:
            length_counts[length] = length_counts.get(length, 0) + 1
        self.most_common_length = max(length_counts, key=length_counts.get)

    def to_dict(self) -> Dict:
        return {
            'passwords_generated': self.passwords_generated,
            'generation_history': self.generation_history,
            'strength_counts': self.strength_counts,
            'average_length': self.average_length,
            'most_common_length': self.most_common_length
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'PasswordStats':
        stats = cls()
        stats.passwords_generated = data.get('passwords_generated', 0)
        stats.generation_history = data.get('generation_history', [])
        stats.strength_counts = data.get('strength_counts', {strength.value: 0 for strength in PasswordStrength})
        stats.average_length = data.get('average_length', 0)
        stats.most_common_length = data.get('most_common_length', 0)
        return stats


class PasswordGenerator:
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    AMBIGUOUS_CHARS = "il1Lo0O"

    def __init__(self, stats_file: str = "password_stats.json"):
        self.config = PasswordConfig()
        self.stats_file = stats_file
        self.stats = self.load_stats()

    def load_stats(self) -> PasswordStats:
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return PasswordStats.from_dict(data)
            except (json.JSONDecodeError, KeyError):
                print("⚠️  Error al cargar estadísticas")
        return PasswordStats()

    def save_stats(self):
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Error al guardar estadísticas: {e}")

    def get_character_set(self) -> str:
        char_set = ""

        if self.config.include_lowercase:
            char_set += self.LOWERCASE

        if self.config.include_uppercase:
            char_set += self.UPPERCASE

        if self.config.include_digits:
            char_set += self.DIGITS

        if self.config.include_symbols:
            if self.config.custom_symbols:
                char_set += self.config.custom_symbols
            else:
                char_set += self.SYMBOLS

        if self.config.exclude_ambiguous:
            for char in self.AMBIGUOUS_CHARS:
                char_set = char_set.replace(char, "")

        if self.config.exclude_chars:
            for char in self.config.exclude_chars:
                char_set = char_set.replace(char, "")

        return char_set

    def generate_password(self) -> str:
        char_set = self.get_character_set()

        if not char_set:
            raise ValueError("No hay caracteres disponibles para generar la contraseña")

        if self.config.require_each_type:
            password = self._generate_with_requirements()
        else:
            password = ''.join(secrets.choice(char_set) for _ in range(self.config.length))

        strength = self.analyze_strength(password)
        self.stats.add_password(len(password), strength)
        self.save_stats()

        return password

    def _generate_with_requirements(self) -> str:
        password_chars = []
        remaining_length = self.config.length

        char_types = []
        if self.config.include_lowercase:
            char_types.append(self.LOWERCASE)
        if self.config.include_uppercase:
            char_types.append(self.UPPERCASE)
        if self.config.include_digits:
            char_types.append(self.DIGITS)
        if self.config.include_symbols:
            symbols = self.config.custom_symbols if self.config.custom_symbols else self.SYMBOLS
            char_types.append(symbols)

        for char_type in char_types:
            if remaining_length > 0:
                available_chars = char_type

                if self.config.exclude_ambiguous:
                    for char in self.AMBIGUOUS_CHARS:
                        available_chars = available_chars.replace(char, "")

                if self.config.exclude_chars:
                    for char in self.config.exclude_chars:
                        available_chars = available_chars.replace(char, "")

                if available_chars:
                    password_chars.append(secrets.choice(available_chars))
                    remaining_length -= 1

        char_set = self.get_character_set()
        while remaining_length > 0:
            password_chars.append(secrets.choice(char_set))
            remaining_length -= 1

        random.shuffle(password_chars)
        return ''.join(password_chars)

    def generate_multiple(self, count: int) -> List[str]:
        return [self.generate_password() for _ in range(count)]

    def analyze_strength(self, password: str) -> PasswordStrength:
        score = 0

        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1

        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'\d', password):
            score += 1
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 1

        if len(set(password)) / len(password) > 0.7:
            score += 1

        if score <= 2:
            return PasswordStrength.WEAK
        elif score <= 4:
            return PasswordStrength.MEDIUM
        elif score <= 6:
            return PasswordStrength.STRONG
        else:
            return PasswordStrength.VERY_STRONG

    def get_strength_info(self, password: str) -> Dict:
        strength = self.analyze_strength(password)

        info = {
            'strength': strength,
            'length': len(password),
            'unique_chars': len(set(password)),
            'char_variety': len(set(password)) / len(password) * 100,
            'has_lowercase': bool(re.search(r'[a-z]', password)),
            'has_uppercase': bool(re.search(r'[A-Z]', password)),
            'has_digits': bool(re.search(r'\d', password)),
            'has_symbols': bool(re.search(r'[^a-zA-Z0-9]', password))
        }

        entropy = len(set(password)) * len(password)
        info['entropy_estimate'] = entropy

        return info


class PasswordGeneratorUI:
    def __init__(self):
        self.generator = PasswordGenerator()

    def show_title(self):
        print("\n" + "═" * 55)
        print("🔐 GENERADOR DE CONTRASEÑAS SEGURAS")
        print("═" * 55)

    def show_main_menu(self):
        config = self.generator.config
        stats = self.generator.stats

        print(f"\n📊 Contraseñas generadas: {stats.passwords_generated}")
        if stats.passwords_generated > 0:
            print(f"📏 Longitud promedio: {stats.average_length:.1f}")

        print("\n" + "─" * 55)
        print("1. 🚀 Generar contraseña")
        print("2. 🔢 Generar múltiples contraseñas")
        print("3. ⚙️  Configurar opciones")
        print("4. 🔍 Analizar contraseña existente")
        print("5. 📊 Ver estadísticas")
        print("6. 💾 Guardar/Cargar configuración")
        print("7. 🗑️  Limpiar estadísticas")
        print("8. 🚪 Salir")
        print("─" * 55)

        print(f"\n⚙️  Configuración actual:")
        print(f"   📏 Longitud: {config.length}")
        types = []
        if config.include_lowercase: types.append("abc")
        if config.include_uppercase: types.append("ABC")
        if config.include_digits: types.append("123")
        if config.include_symbols: types.append("!@#")
        print(f"   🔤 Tipos: {' + '.join(types)}")
        if config.exclude_ambiguous: print("   ⚠️  Sin caracteres ambiguos")

    def generate_single_password(self):
        print("\n🚀 GENERANDO CONTRASEÑA")
        print("─" * 25)

        try:
            password = self.generator.generate_password()
            info = self.generator.get_strength_info(password)

            print(f"🔐 Contraseña generada:")
            print(f"   {password}")

            strength_icons = {
                PasswordStrength.WEAK: "🔴",
                PasswordStrength.MEDIUM: "🟡",
                PasswordStrength.STRONG: "🟢",
                PasswordStrength.VERY_STRONG: "💚"
            }

            strength_icon = strength_icons.get(info['strength'], "❓")
            print(f"\n📈 Fortaleza: {strength_icon} {info['strength'].value.upper()}")
            print(f"📏 Longitud: {info['length']} caracteres")
            print(f"🎯 Variedad: {info['char_variety']:.1f}%")

            char_types = []
            if info['has_lowercase']: char_types.append("minúsculas")
            if info['has_uppercase']: char_types.append("mayúsculas")
            if info['has_digits']: char_types.append("números")
            if info['has_symbols']: char_types.append("símbolos")
            print(f"🔤 Incluye: {', '.join(char_types)}")

        except ValueError as e:
            print(f"❌ Error: {e}")

    def generate_multiple_passwords(self):
        print("\n🔢 GENERAR MÚLTIPLES CONTRASEÑAS")
        print("─" * 35)

        try:
            count = int(input("📝 ¿Cuántas contraseñas? (1-20): "))
            if not 1 <= count <= 20:
                print("❌ Número debe estar entre 1 y 20")
                return

            print(f"\n🔐 {count} contraseñas generadas:")
            print("─" * 40)

            passwords = self.generator.generate_multiple(count)

            for i, password in enumerate(passwords, 1):
                info = self.generator.get_strength_info(password)
                strength_icons = {
                    PasswordStrength.WEAK: "🔴",
                    PasswordStrength.MEDIUM: "🟡",
                    PasswordStrength.STRONG: "🟢",
                    PasswordStrength.VERY_STRONG: "💚"
                }
                icon = strength_icons.get(info['strength'], "❓")
                print(f"{i:2d}. {password} {icon}")

        except ValueError:
            print("❌ Por favor ingresa un número válido")

    def configure_settings(self):
        config = self.generator.config

        while True:
            print("\n⚙️  CONFIGURACIÓN")
            print("─" * 18)
            print(f"1. 📏 Longitud: {config.length}")
            print(f"2. 🔤 Minúsculas: {'✅' if config.include_lowercase else '❌'}")
            print(f"3. 🔠 Mayúsculas: {'✅' if config.include_uppercase else '❌'}")
            print(f"4. 🔢 Números: {'✅' if config.include_digits else '❌'}")
            print(f"5. 🔣 Símbolos: {'✅' if config.include_symbols else '❌'}")
            print(f"6. ⚠️  Excluir ambiguos: {'✅' if config.exclude_ambiguous else '❌'}")
            print(f"7. 🚫 Caracteres a excluir: '{config.exclude_chars}'")
            print(f"8. 🎯 Requerir cada tipo: {'✅' if config.require_each_type else '❌'}")
            print("9. 🔙 Volver al menú principal")

            choice = input("\n👉 Selecciona opción (1-9): ").strip()

            if choice == '1':
                try:
                    length = int(input("📏 Nueva longitud (4-128): "))
                    if 4 <= length <= 128:
                        config.length = length
                        print(f"✅ Longitud cambiada a {length}")
                    else:
                        print("❌ Longitud debe estar entre 4 y 128")
                except ValueError:
                    print("❌ Ingresa un número válido")

            elif choice == '2':
                config.include_lowercase = not config.include_lowercase
                print(f"✅ Minúsculas: {'activadas' if config.include_lowercase else 'desactivadas'}")

            elif choice == '3':
                config.include_uppercase = not config.include_uppercase
                print(f"✅ Mayúsculas: {'activadas' if config.include_uppercase else 'desactivadas'}")

            elif choice == '4':
                config.include_digits = not config.include_digits
                print(f"✅ Números: {'activados' if config.include_digits else 'desactivados'}")

            elif choice == '5':
                config.include_symbols = not config.include_symbols
                print(f"✅ Símbolos: {'activados' if config.include_symbols else 'desactivados'}")

            elif choice == '6':
                config.exclude_ambiguous = not config.exclude_ambiguous
                status = "activada" if config.exclude_ambiguous else "desactivada"
                print(f"✅ Exclusión de ambiguos: {status}")
                if config.exclude_ambiguous:
                    print(f"   Caracteres excluidos: {self.generator.AMBIGUOUS_CHARS}")

            elif choice == '7':
                chars = input("🚫 Caracteres a excluir (vacío para limpiar): ")
                config.exclude_chars = chars
                print(f"✅ Caracteres a excluir: '{chars}'")

            elif choice == '8':
                config.require_each_type = not config.require_each_type
                status = "activado" if config.require_each_type else "desactivado"
                print(f"✅ Requerir cada tipo: {status}")

            elif choice == '9':
                break

            else:
                print("❌ Opción inválida")

    def analyze_existing_password(self):
        print("\n🔍 ANALIZAR CONTRASEÑA")
        print("─" * 22)

        password = input("🔐 Ingresa la contraseña a analizar: ")
        if not password:
            print("❌ No se ingresó ninguna contraseña")
            return

        info = self.generator.get_strength_info(password)

        strength_icons = {
            PasswordStrength.WEAK: "🔴",
            PasswordStrength.MEDIUM: "🟡",
            PasswordStrength.STRONG: "🟢",
            PasswordStrength.VERY_STRONG: "💚"
        }

        print(f"\n📊 ANÁLISIS COMPLETO:")
        print("─" * 20)
        icon = strength_icons.get(info['strength'], "❓")
        print(f"📈 Fortaleza: {icon} {info['strength'].value.upper()}")
        print(f"📏 Longitud: {info['length']} caracteres")
        print(f"🎯 Caracteres únicos: {info['unique_chars']}")
        print(f"📊 Variedad: {info['char_variety']:.1f}%")
        print(f"🔢 Estimación de entropía: {info['entropy_estimate']}")

        print(f"\n🔤 Tipos de caracteres:")
        print(f"   Minúsculas: {'✅' if info['has_lowercase'] else '❌'}")
        print(f"   Mayúsculas: {'✅' if info['has_uppercase'] else '❌'}")
        print(f"   Números: {'✅' if info['has_digits'] else '❌'}")
        print(f"   Símbolos: {'✅' if info['has_symbols'] else '❌'}")

        if info['strength'] == PasswordStrength.WEAK:
            print(f"\n💡 Recomendaciones:")
            print(f"   • Usa al menos 12 caracteres")
            print(f"   • Incluye mayúsculas, minúsculas, números y símbolos")
            print(f"   • Evita patrones predecibles")

    def show_statistics(self):
        stats = self.generator.stats

        print("\n📊 ESTADÍSTICAS DETALLADAS")
        print("═" * 30)

        if stats.passwords_generated == 0:
            print("💭 No se han generado contraseñas aún")
            return

        print(f"🎯 Total generadas: {stats.passwords_generated}")
        print(f"📏 Longitud promedio: {stats.average_length:.1f}")
        print(f"⭐ Longitud más común: {stats.most_common_length}")

        print(f"\n📈 Distribución por fortaleza:")
        strength_icons = {
            "débil": "🔴",
            "medio": "🟡",
            "fuerte": "🟢",
            "muy fuerte": "💚"
        }

        for strength, count in stats.strength_counts.items():
            if count > 0:
                icon = strength_icons.get(strength, "❓")
                percentage = (count / stats.passwords_generated) * 100
                print(f"   {icon} {strength.capitalize()}: {count} ({percentage:.1f}%)")

        if len(stats.generation_history) > 0:
            print(f"\n📅 Últimas 5 generaciones:")
            recent = stats.generation_history[-5:]
            for entry in recent:
                timestamp = datetime.fromisoformat(entry['timestamp'])
                time_str = timestamp.strftime("%d/%m %H:%M")
                strength = entry['strength']
                icon = strength_icons.get(strength, "❓")
                print(f"   {time_str} - {entry['length']} chars {icon}")

    def save_load_config(self):
        print("\n💾 CONFIGURACIÓN")
        print("─" * 16)
        print("1. 💾 Guardar configuración actual")
        print("2. 📁 Cargar configuración")
        print("3. 🔙 Volver")

        choice = input("\n👉 Selecciona opción: ").strip()

        if choice == '1':
            filename = input("📝 Nombre del archivo (sin extensión): ").strip()
            if not filename:
                filename = "password_config"

            try:
                with open(f"{filename}.json", 'w', encoding='utf-8') as f:
                    json.dump(self.generator.config.to_dict(), f, indent=2)
                print(f"✅ Configuración guardada en {filename}.json")
            except Exception as e:
                print(f"❌ Error al guardar: {e}")

        elif choice == '2':
            filename = input("📁 Nombre del archivo: ").strip()
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.generator.config = PasswordConfig.from_dict(data)
                print(f"✅ Configuración cargada desde {filename}")
            except FileNotFoundError:
                print(f"❌ Archivo {filename} no encontrado")
            except Exception as e:
                print(f"❌ Error al cargar: {e}")

    def clear_statistics(self):
        print("\n🗑️  LIMPIAR ESTADÍSTICAS")
        print("─" * 22)

        confirm = input("⚠️  ¿Confirmar limpieza? (escribe 'SI'): ")
        if confirm == 'SI':
            self.generator.stats = PasswordStats()
            self.generator.save_stats()
            print("✅ Estadísticas limpiadas")
        else:
            print("↩️  Operación cancelada")

    def run(self):
        print("🚀 Bienvenido al Generador de Contraseñas Seguras")

        while True:
            try:
                self.show_title()
                self.show_main_menu()

                choice = input("👉 Selecciona una opción (1-8): ").strip()

                if choice == '1':
                    self.generate_single_password()
                elif choice == '2':
                    self.generate_multiple_passwords()
                elif choice == '3':
                    self.configure_settings()
                elif choice == '4':
                    self.analyze_existing_password()
                elif choice == '5':
                    self.show_statistics()
                elif choice == '6':
                    self.save_load_config()
                elif choice == '7':
                    self.clear_statistics()
                elif choice == '8':
                    print("\n👋 ¡Gracias por usar el Generador de Contraseñas!")
                    print("🔐 Mantén tus contraseñas seguras")
                    break
                else:
                    print("❌ Opción inválida. Selecciona del 1 al 8.")

                input("\n📱 Presiona Enter para continuar...")

            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"⚠️  Error inesperado: {e}")


if __name__ == "__main__":
    app = PasswordGeneratorUI()
    app.run()