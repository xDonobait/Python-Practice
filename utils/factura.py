from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from datetime import datetime
import os


class Factura:
    def __init__(self):
        self.numero_factura = ""
        self.fecha = datetime.now().strftime("%d/%m/%Y")
        self.empresa = {
            "nombre": "",
            "direccion": "",
            "telefono": "",
            "email": "",
            "nit": ""
        }
        self.cliente = {
            "nombre": "",
            "direccion": "",
            "telefono": "",
            "identificacion": ""
        }
        self.items = []
        self.subtotal = 0
        self.iva = 0
        self.total = 0

    def agregar_item(self, descripcion, cantidad, precio_unitario):
        total_item = cantidad * precio_unitario
        self.items.append({
            "descripcion": descripcion,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "total": total_item
        })
        self.calcular_totales()

    def calcular_totales(self):
        self.subtotal = sum(item["total"] for item in self.items)
        self.iva = self.subtotal * 0.19  # IVA del 19%
        self.total = self.subtotal + self.iva

    def generar_pdf(self, nombre_archivo="factura.pdf"):
        doc = SimpleDocTemplate(nombre_archivo, pagesize=letter)
        elementos = []
        styles = getSampleStyleSheet()

        style_titulo = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )

        style_derecha = ParagraphStyle(
            'Derecha',
            parent=styles['Normal'],
            alignment=TA_RIGHT
        )

        titulo = Paragraph("FACTURA DE VENTA", style_titulo)
        elementos.append(titulo)
        elementos.append(Spacer(1, 0.2 * inch))

        # Información de la empresa y factura
        info_empresa_factura = [
            [Paragraph(f"<b>{self.empresa['nombre']}</b>", styles['Normal']),
             Paragraph(f"<b>Factura No:</b> {self.numero_factura}", style_derecha)],
            [Paragraph(f"{self.empresa['direccion']}", styles['Normal']),
             Paragraph(f"<b>Fecha:</b> {self.fecha}", style_derecha)],
            [Paragraph(f"Tel: {self.empresa['telefono']}", styles['Normal']), ""],
            [Paragraph(f"Email: {self.empresa['email']}", styles['Normal']), ""],
            [Paragraph(f"NIT: {self.empresa['nit']}", styles['Normal']), ""]
        ]

        tabla_empresa = Table(info_empresa_factura, colWidths=[3.5 * inch, 2.5 * inch])
        tabla_empresa.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elementos.append(tabla_empresa)
        elementos.append(Spacer(1, 0.3 * inch))

        # Información del cliente
        elementos.append(Paragraph("<b>INFORMACIÓN DEL CLIENTE</b>", styles['Heading2']))
        elementos.append(Spacer(1, 0.1 * inch))

        info_cliente = [
            [Paragraph(f"<b>Cliente:</b> {self.cliente['nombre']}", styles['Normal'])],
            [Paragraph(f"<b>Identificación:</b> {self.cliente['identificacion']}", styles['Normal'])],
            [Paragraph(f"<b>Dirección:</b> {self.cliente['direccion']}", styles['Normal'])],
            [Paragraph(f"<b>Teléfono:</b> {self.cliente['telefono']}", styles['Normal'])]
        ]

        tabla_cliente = Table(info_cliente, colWidths=[6 * inch])
        tabla_cliente.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ECF0F1')),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('ROUNDEDCORNERS', [5, 5, 5, 5]),
        ]))
        elementos.append(tabla_cliente)
        elementos.append(Spacer(1, 0.3 * inch))

        # Tabla de items
        elementos.append(Paragraph("<b>DETALLE DE PRODUCTOS/SERVICIOS</b>", styles['Heading2']))
        elementos.append(Spacer(1, 0.1 * inch))

        datos_items = [['Descripción', 'Cantidad', 'Precio Unit.', 'Total']]
        for item in self.items:
            datos_items.append([
                item['descripcion'],
                str(item['cantidad']),
                f"${item['precio_unitario']:,.2f}",
                f"${item['total']:,.2f}"
            ])

        tabla_items = Table(datos_items, colWidths=[3 * inch, 1 * inch, 1 * inch, 1 * inch])
        tabla_items.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')])
        ]))
        elementos.append(tabla_items)
        elementos.append(Spacer(1, 0.3 * inch))

        # Totales
        datos_totales = [
            ['', 'Subtotal:', f"${self.subtotal:,.2f}"],
            ['', f'IVA (19%):', f"${self.iva:,.2f}"],
            ['', 'TOTAL:', f"${self.total:,.2f}"]
        ]

        tabla_totales = Table(datos_totales, colWidths=[3 * inch, 2 * inch, 1 * inch])
        tabla_totales.setStyle(TableStyle([
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (1, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 2), (-1, 2), 14),
            ('TEXTCOLOR', (1, 2), (-1, 2), colors.HexColor('#2C3E50')),
            ('LINEABOVE', (1, 2), (-1, 2), 2, colors.HexColor('#2C3E50')),
            ('TOPPADDING', (1, 2), (-1, 2), 10),
        ]))
        elementos.append(tabla_totales)
        elementos.append(Spacer(1, 0.5 * inch))

        # Pie de página
        elementos.append(Paragraph("<i>Gracias por su compra</i>",
                                   ParagraphStyle('Centro', alignment=TA_CENTER,
                                                  textColor=colors.grey)))

        # Generar PDF
        doc.build(elementos)
        print(f"\n✓ Factura generada exitosamente: {nombre_archivo}")


def main():
    print("=" * 60)
    print("     SISTEMA DE FACTURACIÓN - GENERADOR DE RECIBOS PDF")
    print("=" * 60)

    factura = Factura()

    # Datos de la empresa
    print("\n--- DATOS DE LA EMPRESA ---")
    factura.empresa["nombre"] = input("Nombre de la empresa: ") or "Mi Empresa S.A.S."
    factura.empresa["direccion"] = input("Dirección: ") or "Calle 123 #45-67"
    factura.empresa["telefono"] = input("Teléfono: ") or "+57 300 123 4567"
    factura.empresa["email"] = input("Email: ") or "info@miempresa.com"
    factura.empresa["nit"] = input("NIT: ") or "900.123.456-7"

    # Número de factura
    factura.numero_factura = input("\nNúmero de factura: ") or f"F-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Datos del cliente
    print("\n--- DATOS DEL CLIENTE ---")
    factura.cliente["nombre"] = input("Nombre del cliente: ") or "Cliente Ejemplo"
    factura.cliente["identificacion"] = input("Identificación/NIT: ") or "12345678-9"
    factura.cliente["direccion"] = input("Dirección: ") or "Calle 456 #78-90"
    factura.cliente["telefono"] = input("Teléfono: ") or "+57 310 987 6543"

    # Items de la factura
    print("\n--- PRODUCTOS/SERVICIOS ---")
    while True:
        print("\nAgregar item:")
        descripcion = input("Descripción (Enter para terminar): ")
        if not descripcion:
            break

        try:
            cantidad = float(input("Cantidad: "))
            precio = float(input("Precio unitario: "))
            factura.agregar_item(descripcion, cantidad, precio)
            print(f"✓ Item agregado - Total: ${cantidad * precio:,.2f}")
        except ValueError:
            print("⚠ Error: Ingrese valores numéricos válidos")

    if not factura.items:
        print("\n⚠ No se agregaron items. Agregando item de ejemplo...")
        factura.agregar_item("Producto de ejemplo", 1, 100000)

    # Resumen
    print("\n" + "=" * 60)
    print(f"Subtotal: ${factura.subtotal:,.2f}")
    print(f"IVA (19%): ${factura.iva:,.2f}")
    print(f"TOTAL: ${factura.total:,.2f}")
    print("=" * 60)

    # Generar PDF
    nombre_archivo = input("\nNombre del archivo PDF (factura.pdf): ") or "factura.pdf"
    if not nombre_archivo.endswith('.pdf'):
        nombre_archivo += '.pdf'

    factura.generar_pdf(nombre_archivo)
    print(f"\n✓ Proceso completado. Revise el archivo: {os.path.abspath(nombre_archivo)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\n✗ Error: {e}")