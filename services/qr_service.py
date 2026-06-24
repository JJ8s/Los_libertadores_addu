import os
import qrcode


def generar_qr(contenido):

    os.makedirs("qr", exist_ok=True)

    nombre_archivo = "qr/declaracion.png"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4
    )

    qr.add_data(contenido)
    qr.make(fit=True)

    imagen = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    imagen.save(nombre_archivo)

    return nombre_archivo