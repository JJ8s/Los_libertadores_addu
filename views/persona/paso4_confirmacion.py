from nicegui import ui
from .estado import estado
import uuid
from datetime import datetime

from services.qr_service import generar_qr
from services.pdf_service import generar_pdf
from services.supabase_service import guardar_declaracion

def render_paso4(on_atras, on_finalizar):

    # ==========================
    # DATOS PARA QR Y PDF
    # ==========================

    if 'codigo_declaracion' not in estado:
        estado['codigo_declaracion'] = str(uuid.uuid4())

    codigo_declaracion = estado['codigo_declaracion']   

    qr_payload = (
        f"CODIGO:{codigo_declaracion}\n"
        f"NOMBRE:{estado.get('nombre','')}\n"
        f"APELLIDO:{estado.get('apellido','')}\n"
        f"DNI:{estado.get('dni','')}\n"
        f"PAIS:{estado.get('pais','')}\n"
        f"CORREO:{estado.get('correo','')}"
    )

    ruta_qr = generar_qr(qr_payload)

    datos_pdf = {
    "codigo": codigo_declaracion,
    "nombre": estado.get("nombre", ""),
    "apellido": estado.get("apellido", ""),
    "dni": estado.get("dni", ""),
    "pais": estado.get("pais", ""),
    "nacionalidad": estado.get("nacionalidad", ""),
    "fecha_nacimiento": estado.get("fecha_nacimiento", ""),
    "correo": estado.get("correo", ""),
    "proposito": estado.get("proposito", ""),
    "menores": estado.get("menores", False),
    "bienes": estado.get("bienes", {})
    }

    ruta_pdf = generar_pdf(
        datos_pdf,
        ruta_qr
    )

    # ==========================
    # INTERFAZ
    # ==========================

    with ui.column().classes('w-full items-center').style(
        'gap: 20px; padding: 20px;'
    ):

        with ui.row().classes(
            'items-center justify-center'
        ).style(
            'gap: 10px; margin-bottom: 5px;'
        ):

            ui.label('🎉').style(
                'font-size: 28px;'
            )

            ui.label(
                '¡Declaración Generada Exitosamente!'
            ).style(
                'font-size: 24px; font-weight: 800; color: #10B981;'
            )

        # ==================================
        # COMPROBANTE
        # ==================================

        with ui.card().style(
            '''
            width: 460px;
            padding: 0px;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
            border: 1px solid #E5E7EB;
            '''
        ):

            # Encabezado

            with ui.row().classes(
                'w-full justify-between items-center'
            ).style(
                'background: #082B57; padding: 18px 24px;'
            ):

                ui.label(
                    'DECLARACIÓN JURADA DIGITAL'
                ).style(
                    '''
                    color: white;
                    font-weight: 700;
                    font-size: 13px;
                    letter-spacing: 0.5px;
                    '''
                )

                ui.label(
                    'ADUANA / SAG'
                ).style(
                    '''
                    color: #12B5D9;
                    font-weight: 900;
                    font-size: 14px;
                    '''
                )

            # Cuerpo

            with ui.column().classes(
                'w-full items-center'
            ).style(
                'padding: 28px; gap: 16px; background: #ffffff;'
            ):

                ui.label(
                    '✓ TRÁMITE APROBADO'
                ).style(
                    '''
                    background: #D1FAE5;
                    color: #065F46;
                    padding: 6px 18px;
                    font-weight: 800;
                    border-radius: 9999px;
                    font-size: 12px;
                    letter-spacing: 0.5px;
                    '''
                )

                # QR REAL

                ui.image(ruta_qr).style(
                    '''
                    width: 180px;
                    height: 180px;
                    margin: 10px 0;
                    border: 4px solid #F3F4F6;
                    padding: 6px;
                    border-radius: 8px;
                    '''
                )

                ui.label(
                    'Presente este código QR al inspector en el punto de control fronterizo.'
                ).style(
                    '''
                    font-size: 11px;
                    color: #6B7280;
                    text-align: center;
                    max-width: 320px;
                    line-height: 1.4;
                    '''
                )

                ui.element('div').style(
                    '''
                    width: 100%;
                    height: 1px;
                    border-top: 2px dashed #E5E7EB;
                    margin: 12px 0;
                    '''
                )

                with ui.grid(columns=2).style(
                    '''
                    width: 100%;
                    row-gap: 12px;
                    col-gap: 10px;
                    font-size: 13px;
                    '''
                ):

                    ui.label(
                        'Pasajero:'
                    ).style(
                        'color: #6B7280; font-weight: 500;'
                    )

                    ui.label(
                        f"{estado.get('nombre', '')} {estado.get('apellido', '')}"
                    ).style(
                        'color: #111827; font-weight: 700; text-align: right;'
                    )

                    ui.label(
                        'Documento / ID:'
                    ).style(
                        'color: #6B7280; font-weight: 500;'
                    )

                    ui.label(
                        estado.get('dni', '')
                    ).style(
                        'color: #111827; font-weight: 700; text-align: right;'
                    )

                    ui.label(
                        'País Emisor:'
                    ).style(
                        'color: #6B7280; font-weight: 500;'
                    )

                    ui.label(
                        estado.get('pais', 'Argentina')
                    ).style(
                        'color: #111827; font-weight: 600; text-align: right;'
                    )

                    ui.label(
                        'Nacionalidad:'
                    ).style(
                        'color: #6B7280; font-weight: 500;'
                    )

                    ui.label(
                        estado.get(
                            'nacionalidad',
                            'No especificada'
                        )
                    ).style(
                        'color: #111827; font-weight: 600; text-align: right;'
                    )

                    # NUEVO

                    ui.label(
                        'Propósito:'
                    ).style(
                        'color: #6B7280; font-weight: 500;'
                    )

                    ui.label(
                        str(
                            estado.get(
                                'proposito',
                                ''
                            )
                        ).upper()
                    ).style(
                        'color: #111827; font-weight: 600; text-align: right;'
                    )

                    ui.label(
                        'Viaja con menores:'
                    ).style(
                        'color: #6B7280; font-weight: 500;'
                    )

                    ui.label(
                        'SI' if estado.get('menores') else 'NO'
                    ).style(
                        'color: #111827; font-weight: 600; text-align: right;'
                    )

                    ui.label(
                        'Contacto:'
                    ).style(
                        'color: #6B7280; font-weight: 500;'
                    )

                    ui.label(
                        estado.get('correo', '')
                    ).style(
                        '''
                        color: #111827;
                        font-weight: 600;
                        text-align: right;
                        word-break: break-all;
                        '''
                    )

                    ui.label(
                        'Contacto:'
                    ).style(
                        'color: #6B7280; font-weight: 500;'
                    )

                    ui.label(
                        estado.get('correo', '')
                    ).style(
                        '''
                        color: #111827;
                        font-weight: 600;
                        text-align: right;
                        word-break: break-all;
                        '''
                    )

                    ui.label(
                        'Fecha de Emisión:'
                    ).style(
                        'color: #6B7280; font-weight: 500;'
                    )

                    ui.label(
                        datetime.now().strftime('%d/%m/%Y')
                    ).style(
                        'color: #111827; font-weight: 600; text-align: right;'
                    )

        # ==================================
        # BOTONES
        # ==================================

        with ui.row().classes(
            'justify-center'
        ).style(
            'gap: 16px; margin-top: 15px;'
        ):

            ui.button(
                '← Volver',
                on_click=on_atras
            ).style(
                '''
                background: #E5E7EB;
                color: #374151;
                padding: 10px 24px;
                font-weight: bold;
                border-radius: 8px;
                box-shadow: none;
                '''
            )

            ui.button(
                'Descargar PDF 📄',
                on_click=lambda: ui.download(ruta_pdf)
            ).style(
                '''
                background: #082B57;
                color: white;
                padding: 10px 24px;
                font-weight: bold;
                border-radius: 8px;
                '''
            )

    def finalizar_tramite():

        try:

            print("GUARDANDO:")
            print(datos_pdf)

            resultado = guardar_declaracion(datos_pdf)

            print("RESULTADO:")
            print(resultado)

            ui.notify(
                'Declaración guardada correctamente',
                color='positive'
            )

            on_finalizar()

        except Exception as e:

            print("ERROR:")
            print(str(e))

            ui.notify(
                f'Error al guardar: {str(e)}',
                color='negative'
            )

    ui.button(
        'Finalizar',
        on_click=finalizar_tramite
    ).style(
        '''
        background: #12B5D9;
        color: white;
        padding: 10px 24px;
        font-weight: bold;
        border-radius: 8px;
        '''
    )