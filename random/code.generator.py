import qrcode
from PIL import Image
import os

# Intentar importar módulos avanzados (opcional)
try:
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, SquareModuleDrawer, CircleModuleDrawer

    ESTILOS_DISPONIBLES = True
except ImportError:
    print("Módulos de estilo avanzado no disponibles. Usando estilos básicos.")
    ESTILOS_DISPONIBLES = False


class GeneradorQR:
    def __init__(self):
        self.qr = None

    @staticmethod
    def crear_qr_basico(datos, nombre_archivo="qr_code.png"):
        """
        Crea un código QR básico en blanco y negro
        """
        # Crear objeto QR
        qr = qrcode.QRCode(
            version=1,  # Controla el tamaño del QR (1-40)
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nivel de corrección de errores
            box_size=10,  # Tamaño de cada "caja" en píxeles
            border=4,  # Tamaño del borde
        )

        # Añadir datos
        qr.add_data(datos)
        qr.make(fit=True)

        # Crear imagen
        img = qr.make_image(fill_color="black", back_color="white")

        # Guardar imagen
        img.save(nombre_archivo)
        print(f"QR básico guardado como: {nombre_archivo}")

        return img

    @staticmethod
    def crear_qr_personalizado(datos, nombre_archivo="qr_personalizado.png",
                               color_relleno="black", color_fondo="white",
                               tamano_caja=10, borde=4):
        """
        Crea un código QR con colores personalizados
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=tamano_caja,
            border=borde,
        )

        qr.add_data(datos)
        qr.make(fit=True)

        # Crear imagen con colores personalizados
        img = qr.make_image(fill_color=color_relleno, back_color=color_fondo)

        img.save(nombre_archivo)
        print(f"QR personalizado guardado como: {nombre_archivo}")

        return img

    @staticmethod
    def crear_qr_estilizado(datos, nombre_archivo="qr_estilizado.png",
                            estilo="rounded", color_principal="#000000",
                            color_fondo="#FFFFFF"):
        """
        Crea un código QR con estilos avanzados (requiere módulos opcionales)
        """
        if not ESTILOS_DISPONIBLES:
            print("Estilos avanzados no disponibles. Creando QR básico personalizado...")
            return GeneradorQR.crear_qr_personalizado(datos, nombre_archivo, color_principal, color_fondo)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )

        qr.add_data(datos)
        qr.make(fit=True)

        # Seleccionar estilo de módulo
        if estilo == "rounded":
            module_drawer = RoundedModuleDrawer()
        elif estilo == "circle":
            module_drawer = CircleModuleDrawer()
        else:
            module_drawer = SquareModuleDrawer()

        # Crear imagen estilizada
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            fill_color=color_principal,
            back_color=color_fondo
        )

        img.save(nombre_archivo)
        print(f"QR estilizado guardado como: {nombre_archivo}")

        return img

    @staticmethod
    def crear_qr_con_logo(datos, ruta_logo, nombre_archivo="qr_con_logo.png"):
        """
        Crea un código QR con logo en el centro
        """
        # Crear QR con mayor corrección de errores para soportar el logo
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # Alta corrección
            box_size=10,
            border=4,
        )

        qr.add_data(datos)
        qr.make(fit=True)

        # Crear imagen del QR
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # Abrir y redimensionar logo
        try:
            logo = Image.open(ruta_logo)

            # Calcular tamaño del logo (aproximadamente 1/5 del QR)
            qr_width, qr_height = qr_img.size
            logo_size = min(qr_width, qr_height) // 5

            # Redimensionar logo manteniendo proporción
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

            # Calcular posición central
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

            # Pegar logo en el centro
            qr_img.paste(logo, pos)

            qr_img.save(nombre_archivo)
            print(f"QR con logo guardado como: {nombre_archivo}")

            return qr_img

        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de logo: {ruta_logo}")
            return None

    @staticmethod
    def generar_multiples_tipos(datos):
        """
        Genera varios tipos de QR de una vez
        """
        print(f"Generando códigos QR para: {datos}")
        print("=" * 50)

        # QR básico
        GeneradorQR.crear_qr_basico(datos, "qr_basico.png")

        # QR azul
        GeneradorQR.crear_qr_personalizado(datos, "qr_azul.png",
                                           color_relleno="blue", color_fondo="lightblue")

        # QR verde con módulos redondeados
        GeneradorQR.crear_qr_estilizado(datos, "qr_verde_redondeado.png",
                                        estilo="rounded", color_principal="green",
                                        color_fondo="lightgreen")

        # QR rojo con módulos circulares
        GeneradorQR.crear_qr_estilizado(datos, "qr_rojo_circular.png",
                                        estilo="circle", color_principal="red",
                                        color_fondo="pink")

        print("=" * 50)
        print("¡Todos los códigos QR generados exitosamente!")


def menu_interactivo():
    """
    Menú interactivo para generar diferentes tipos de QR
    """
    generador = GeneradorQR()

    while True:
        print("\n" + "=" * 50)
        print("🔲 GENERADOR DE CÓDIGOS QR 🔲")
        print("=" * 50)
        print("1. QR Básico (blanco y negro)")
        print("2. QR Personalizado (colores)")
        print("3. QR Estilizado (módulos especiales)")
        print("4. QR con Logo")
        print("5. Generar múltiples tipos")
        print("6. Salir")
        print("=" * 50)

        opcion = input("Selecciona una opción (1-6): ").strip()

        if opcion == "1":
            datos = input("Ingresa el texto/URL para el QR: ")
            nombre = input("Nombre del archivo (presiona Enter para 'qr_basico.png'): ").strip()
            if not nombre:
                nombre = "qr_basico.png"
            generador.crear_qr_basico(datos, nombre)

        elif opcion == "2":
            datos = input("Ingresa el texto/URL para el QR: ")
            nombre = input("Nombre del archivo (presiona Enter para 'qr_personalizado.png'): ").strip()
            if not nombre:
                nombre = "qr_personalizado.png"

            color_relleno = input("Color de relleno (presiona Enter para 'black'): ").strip()
            if not color_relleno:
                color_relleno = "black"

            color_fondo = input("Color de fondo (presiona Enter para 'white'): ").strip()
            if not color_fondo:
                color_fondo = "white"

            GeneradorQR.crear_qr_personalizado(datos, nombre, color_relleno, color_fondo)

        elif opcion == "3":
            datos = input("Ingresa el texto/URL para el QR: ")
            nombre = input("Nombre del archivo (presiona Enter para 'qr_estilizado.png'): ").strip()
            if not nombre:
                nombre = "qr_estilizado.png"

            print("Estilos disponibles: rounded, circle, square")
            estilo = input("Selecciona el estilo (presiona Enter para 'rounded'): ").strip()
            if not estilo:
                estilo = "rounded"

            color_principal = input("Color principal (presiona Enter para '#000000'): ").strip()
            if not color_principal:
                color_principal = "#000000"

            color_fondo = input("Color de fondo (presiona Enter para '#FFFFFF'): ").strip()
            if not color_fondo:
                color_fondo = "#FFFFFF"

            GeneradorQR.crear_qr_estilizado(datos, nombre, estilo, color_principal, color_fondo)

        elif opcion == "4":
            datos = input("Ingresa el texto/URL para el QR: ")
            ruta_logo = input("Ruta del archivo de logo: ").strip()
            nombre = input("Nombre del archivo (presiona Enter para 'qr_con_logo.png'): ").strip()
            if not nombre:
                nombre = "qr_con_logo.png"

            GeneradorQR.crear_qr_con_logo(datos, ruta_logo, nombre)

        elif opcion == "5":
            datos = input("Ingresa el texto/URL para el QR: ")
            GeneradorQR.generar_multiples_tipos(datos)

        elif opcion == "6":
            print("¡Gracias por usar el Generador de QR!")
            break

        else:
            print("Opción no válida. Por favor, selecciona del 1 al 6.")


# Ejemplo de uso directo
def ejemplo_uso():
    """
    Ejemplos de cómo usar el generador
    """
    # Datos de ejemplo
    url = "https://www.python.org"
    texto = "¡Hola desde Python!"
    wifi = "WIFI:T:WPA;S:MiRed;P:mipassword123;;"

    print("Generando ejemplos de códigos QR...")

    # Generar diferentes tipos
    GeneradorQR.crear_qr_basico(url, "ejemplo_url.png")
    GeneradorQR.crear_qr_personalizado(texto, "ejemplo_texto.png", "blue", "lightblue")
    GeneradorQR.crear_qr_estilizado(wifi, "ejemplo_wifi.png", "circle", "green", "white")

    print("\nEjemplos generados:")
    print("- ejemplo_url.png: URL de Python")
    print("- ejemplo_texto.png: Texto personalizado")
    print("- ejemplo_wifi.png: Configuración WiFi")


if __name__ == "__main__":
    print("Instalación requerida:")
    print("pip install qrcode[pil]")
    print("\nOpciones de ejecución:")
    print("1. Ejecutar menú interactivo")
    print("2. Generar ejemplos")

    opcion = input("\nSelecciona (1 o 2): ").strip()

    if opcion == "1":
        menu_interactivo()
    elif opcion == "2":
        ejemplo_uso()
    else:
        print("Ejecutando menú interactivo por defecto...")
        menu_interactivo()