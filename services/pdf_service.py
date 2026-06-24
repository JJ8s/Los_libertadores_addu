from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime
import os


def generar_pdf(datos, qr_path):

    os.makedirs("documentos", exist_ok=True)

    archivo = f"documentos/{datos['dni']}.pdf"

    pdf = SimpleDocTemplate(archivo)

    estilos = getSampleStyleSheet()

    contenido = []

    # =====================
    # ENCABEZADO
    # =====================

    contenido.append(
        Paragraph(
            "DECLARACIÓN JURADA DIGITAL",
            estilos["Title"]
        )
    )

    contenido.append(
        Paragraph(
            "Servicio Nacional de Aduanas / SAG",
            estilos["Heading2"]
        )
    )

    contenido.append(Spacer(1, 20))

    # =====================
    # DATOS GENERALES
    # =====================

    contenido.append(
        Paragraph(
            f"<b>Código:</b> {datos['codigo']}",
            estilos["Normal"]
        )
    )

    contenido.append(
        Paragraph(
            f"<b>Fecha de emisión:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            estilos["Normal"]
        )
    )

    contenido.append(Spacer(1, 15))

    # =====================
    # DATOS DEL VIAJERO
    # =====================

    contenido.append(
        Paragraph(
            "<b>DATOS DEL VIAJERO</b>",
            estilos["Heading3"]
        )
    )

    contenido.append(
        Paragraph(
            f"Nombre completo: {datos['nombre']} {datos['apellido']}",
            estilos["Normal"]
        )
    )

    contenido.append(
        Paragraph(
            f"Documento: {datos['dni']}",
            estilos["Normal"]
        )
    )

    contenido.append(
        Paragraph(
            f"País emisor: {datos['pais']}",
            estilos["Normal"]
        )
    )

    contenido.append(
        Paragraph(
            f"Nacionalidad: {datos['nacionalidad']}",
            estilos["Normal"]
        )
    )

    contenido.append(
        Paragraph(
            f"Fecha nacimiento: {datos['fecha_nacimiento']}",
            estilos["Normal"]
        )
    )

    contenido.append(
        Paragraph(
            f"Correo: {datos['correo']}",
            estilos["Normal"]
        )
    )

    contenido.append(Spacer(1, 15))

    # =====================
    # VIAJE
    # =====================

    contenido.append(
        Paragraph(
            "<b>INFORMACIÓN DEL VIAJE</b>",
            estilos["Heading3"]
        )
    )

    contenido.append(
        Paragraph(
            f"Propósito: {datos['proposito']}",
            estilos["Normal"]
        )
    )

    contenido.append(
        Paragraph(
            f"Viaja con menores: {'SI' if datos['menores'] else 'NO'}",
            estilos["Normal"]
        )
    )

    contenido.append(Spacer(1, 15))

    # =====================
    # BIENES
    # =====================

    contenido.append(
        Paragraph(
            "<b>DECLARACIÓN DE BIENES</b>",
            estilos["Heading3"]
        )
    )

    nombres_bienes = {
        "alimentos": "Alimentos",
        "animales": "Animales",
        "medicamentos": "Medicamentos",
        "dinero": "Más de USD 10.000",
        "agricolas": "Productos agrícolas",
        "armas": "Armas o municiones"
    }

    bienes_seleccionados = []

    for clave, valor in datos["bienes"].items():

        if valor:
            bienes_seleccionados.append(
                nombres_bienes.get(clave, clave)
            )

    if bienes_seleccionados:

        for bien in bienes_seleccionados:

            contenido.append(
                Paragraph(
                    f"• {bien}",
                    estilos["Normal"]
                )
            )

    else:

        contenido.append(
            Paragraph(
                "No se declararon bienes.",
                estilos["Normal"]
            )
        )

    contenido.append(Spacer(1, 20))

    # =====================
    # QR
    # =====================

    contenido.append(
        Paragraph(
            "<b>CÓDIGO QR DE VERIFICACIÓN</b>",
            estilos["Heading3"]
        )
    )

    contenido.append(
        Image(
            qr_path,
            width=150,
            height=150
        )
    )

    contenido.append(
        Spacer(1, 10)
    )

    contenido.append(
        Paragraph(
            "Este código permite verificar la declaración.",
            estilos["Italic"]
        )
    )

    pdf.build(contenido)

    return archivo