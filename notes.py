import datetime
import random
import os

# Ideas y reflexiones random
notas = [
    "Recordar: revisar la documentación de async/await",
    "TODO: explorar más sobre patrones de diseño",
    "Idea: implementar sistema de cache en el próximo proyecto",
    "Nota mental: optimizar queries de la base de datos",
    "Aprendizaje del día: los pequeños commits son mejores",
    "Reflexión: el código limpio es código feliz",
    "Investigar: nuevas features de Python 3.12",
    "Recordatorio: refactorizar ese módulo legacy",
    "Concepto interesante: event-driven architecture",
    "Para explorar: microservicios vs monolitos"
]


def nueva_nota():
    """Genera una nota diaria de desarrollo"""

    hoy = datetime.datetime.now()
    archivo = f"notas/nota_{hoy.strftime('%Y%m%d')}.md"

    # Crear directorio si no existe
    os.makedirs("notas", exist_ok=True)

    nota = random.choice(notas)

    with open(archivo, 'w', encoding='utf-8') as f:
        f.write(f"# Nota de Desarrollo\n\n")
        f.write(f"**Fecha:** {hoy.strftime('%d/%m/%Y')}\n\n")
        f.write(f"{nota}\n\n")
        f.write(f"---\n")
        f.write(f"*Generado automáticamente*\n")

    print(f"✓ Nueva nota creada: {archivo}")
    print(f"  {nota}")


if __name__ == "__main__":
    nueva_nota()