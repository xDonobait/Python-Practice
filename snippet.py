import datetime
import random
import json
import os
from pathlib import Path


class SnippetManager:
    """Gestor de snippets de código y utilidades"""

    def __init__(self, base_dir="dev_snippets"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.config_file = self.base_dir / "config.json"
        self.load_config()

    def load_config(self):
        """Carga o crea la configuración"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "total_snippets": 0,
                "categorias": {},
                "ultimo_snippet": None
            }
            self.save_config()

    def save_config(self):
        """Guarda la configuración"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def crear_snippet_aleatorio(self):
        """Genera un snippet útil aleatorio"""
        snippets = [
            self._snippet_timer(),
            self._snippet_logger(),
            self._snippet_retry(),
            self._snippet_cache(),
            self._snippet_validator(),
            self._snippet_parser(),
            self._snippet_formatter(),
            self._snippet_helper()
        ]

        snippet_func = random.choice(snippets)
        return snippet_func

    def _snippet_timer(self):
        """Decorador para medir tiempo de ejecución"""
        codigo = '''"""Decorador para medir tiempo de ejecución de funciones"""
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} ejecutado en {end-start:.4f}s")
        return result
    return wrapper

# Uso:
# @timer
# def mi_funcion():
#     pass
'''
        return ("utils", "timer_decorator.py", codigo)

    def _snippet_logger(self):
        """Sistema simple de logging"""
        codigo = '''"""Sistema simple de logging con niveles"""
import datetime

class SimpleLogger:
    LEVELS = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3}

    def __init__(self, level='INFO'):
        self.level = self.LEVELS.get(level, 1)

    def _log(self, level, msg):
        if self.LEVELS[level] >= self.level:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] {level}: {msg}")

    def debug(self, msg): self._log('DEBUG', msg)
    def info(self, msg): self._log('INFO', msg)
    def warning(self, msg): self._log('WARNING', msg)
    def error(self, msg): self._log('ERROR', msg)

# logger = SimpleLogger('DEBUG')
# logger.info("Aplicación iniciada")
'''
        return ("logging", "simple_logger.py", codigo)

    def _snippet_retry(self):
        """Decorador de reintentos"""
        codigo = '''"""Decorador para reintentar funciones que fallan"""
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Intento {attempt+1} falló: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

# @retry(max_attempts=3, delay=2)
# def funcion_inestable():
#     pass
'''
        return ("utils", "retry_decorator.py", codigo)

    def _snippet_cache(self):
        """Sistema simple de caché"""
        codigo = '''"""Caché simple en memoria con expiración"""
import time
from functools import wraps

class SimpleCache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        if key in self.cache:
            value, expiry = self.cache[key]
            if expiry is None or time.time() < expiry:
                return value
            del self.cache[key]
        return None

    def set(self, key, value, ttl=None):
        expiry = time.time() + ttl if ttl else None
        self.cache[key] = (value, expiry)

    def clear(self):
        self.cache.clear()

def memoize(ttl=None):
    cache = SimpleCache()
    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            key = str(args)
            result = cache.get(key)
            if result is None:
                result = func(*args)
                cache.set(key, result, ttl)
            return result
        return wrapper
    return decorator
'''
        return ("cache", "simple_cache.py", codigo)

    def _snippet_validator(self):
        """Validador de datos"""
        codigo = '''"""Validadores comunes para datos"""
import re

class Validator:
    @staticmethod
    def email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def phone(phone):
        # Formato: +57 300 123 4567 o similar
        pattern = r'^\\+?[0-9\\s-]{10,15}$'
        return re.match(pattern, phone) is not None

    @staticmethod
    def url(url):
        pattern = r'^https?://[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'
        return re.match(pattern, url) is not None

    @staticmethod
    def not_empty(value):
        return value is not None and str(value).strip() != ''

    @staticmethod
    def length(value, min_len=0, max_len=float('inf')):
        return min_len <= len(str(value)) <= max_len

# if Validator.email("test@example.com"):
#     print("Email válido")
'''
        return ("validators", "data_validator.py", codigo)

    def _snippet_parser(self):
        """Parser de configuración"""
        codigo = '''"""Parser simple para archivos de configuración"""
import json
from pathlib import Path

class ConfigParser:
    def __init__(self, config_path):
        self.path = Path(config_path)
        self.config = {}
        self.load()

    def load(self):
        if self.path.exists():
            with open(self.path, 'r') as f:
                if self.path.suffix == '.json':
                    self.config = json.load(f)
                else:
                    self._parse_ini(f)

    def _parse_ini(self, file):
        section = 'default'
        self.config[section] = {}
        for line in file:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1]
                self.config[section] = {}
            elif '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                self.config[section][key.strip()] = value.strip()

    def get(self, key, section='default', default=None):
        return self.config.get(section, {}).get(key, default)

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.config, f, indent=2)
'''
        return ("parsers", "config_parser.py", codigo)

    def _snippet_formatter(self):
        """Formateadores de texto"""
        codigo = '''"""Utilidades para formatear texto y datos"""

class Formatter:
    @staticmethod
    def truncate(text, length=50, suffix='...'):
        if len(text) <= length:
            return text
        return text[:length-len(suffix)] + suffix

    @staticmethod
    def slug(text):
        import re
        text = text.lower().strip()
        text = re.sub(r'[^a-z0-9\\s-]', '', text)
        text = re.sub(r'[\\s-]+', '-', text)
        return text

    @staticmethod
    def bytes_to_human(bytes_size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"

    @staticmethod
    def time_ago(timestamp):
        import datetime
        now = datetime.datetime.now()
        diff = now - timestamp

        if diff.days > 365:
            return f"hace {diff.days // 365} años"
        elif diff.days > 30:
            return f"hace {diff.days // 30} meses"
        elif diff.days > 0:
            return f"hace {diff.days} días"
        elif diff.seconds > 3600:
            return f"hace {diff.seconds // 3600} horas"
        elif diff.seconds > 60:
            return f"hace {diff.seconds // 60} minutos"
        return "hace unos segundos"

# print(Formatter.bytes_to_human(1536000))  # 1.46 MB
# print(Formatter.slug("Hola Mundo 2024!"))  # hola-mundo-2024
'''
        return ("formatters", "text_formatter.py", codigo)

    def _snippet_helper(self):
        """Helpers generales"""
        codigo = '''"""Funciones helper de uso general"""
import os
import hashlib
from pathlib import Path

class Helpers:
    @staticmethod
    def get_file_hash(filepath, algorithm='md5'):
        hash_func = getattr(hashlib, algorithm)()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    @staticmethod
    def ensure_dir(path):
        Path(path).mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def flatten_list(nested_list):
        result = []
        for item in nested_list:
            if isinstance(item, list):
                result.extend(Helpers.flatten_list(item))
            else:
                result.append(item)
        return result

    @staticmethod
    def chunk_list(lst, size):
        return [lst[i:i+size] for i in range(0, len(lst), size)]

    @staticmethod
    def safe_divide(a, b, default=0):
        try:
            return a / b
        except ZeroDivisionError:
            return default

# chunks = Helpers.chunk_list([1,2,3,4,5,6,7], 3)
# print(chunks)  # [[1,2,3], [4,5,6], [7]]
'''
        return ("helpers", "general_helpers.py", codigo)

    def generar(self):
        """Genera un snippet del día"""
        categoria, filename, codigo = self.crear_snippet_aleatorio()

        # Crear directorio de categoría
        cat_dir = self.base_dir / categoria
        cat_dir.mkdir(exist_ok=True)

        # Agregar timestamp al archivo
        hoy = datetime.datetime.now()
        base_name = Path(filename).stem
        ext = Path(filename).suffix
        final_filename = f"{base_name}_{hoy.strftime('%Y%m%d')}{ext}"

        filepath = cat_dir / final_filename

        # Escribir snippet
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Generado: {hoy.strftime('%Y-%m-%d %H:%M')}\n")
            f.write(codigo)

        # Actualizar config
        self.config["total_snippets"] += 1
        if categoria not in self.config["categorias"]:
            self.config["categorias"][categoria] = 0
        self.config["categorias"][categoria] += 1
        self.config["ultimo_snippet"] = str(filepath)
        self.save_config()

        return filepath, categoria

    def stats(self):
        """Muestra estadísticas"""
        print("\n📊 Estadísticas de Snippets")
        print("=" * 40)
        print(f"Total de snippets: {self.config['total_snippets']}")
        print(f"\nPor categoría:")
        for cat, count in self.config["categorias"].items():
            print(f"  • {cat}: {count}")
        if self.config["ultimo_snippet"]:
            print(f"\nÚltimo generado: {self.config['ultimo_snippet']}")
        print("=" * 40)


def main():
    manager = SnippetManager()

    filepath, categoria = manager.generar()

    print("\n✨ Snippet generado exitosamente!")
    print(f"📁 Categoría: {categoria}")
    print(f"📄 Archivo: {filepath}")

    manager.stats()

    print("\n💡 Estos snippets son utilidades reutilizables")
    print("   que puedes usar en tus proyectos.\n")


if __name__ == "__main__":
    main()