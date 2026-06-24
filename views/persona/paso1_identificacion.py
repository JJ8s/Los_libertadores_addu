from nicegui import ui
from .estado import estado

PAIS_DEFAULT = {
    'label': 'Documento de Identidad',
    'placeholder': 'Ingrese número de documento',
    'hint': 'Debe contener entre 7 y 9 caracteres.'
}


def render_paso1(on_continuar):

    pais_actual = estado.get('pais', '')

    # --- FILA SUPERIOR ---
    with ui.row().classes(
        'w-full justify-between items-center'
    ).style(
        'margin-bottom: 20px; max-width: 810px; margin: 0 auto 20px auto;'
    ):

        ui.label(
            'Paso 1 - Identificación'
        ).style(
            'font-size:22px;font-weight:700;color:#082B57;'
        )

        ui.button(
            'Ir al Paso 2 →',
            on_click=on_continuar
        ).style(
            'background: #06B6D4; color: white; padding: 8px 20px; font-weight: bold; border-radius: 8px; box-shadow: none;'
        )

    with ui.row().classes(
        'w-full justify-center'
    ).style(
        'gap:30px; align-items:flex-start; padding-bottom: 50px;'
    ):

        # ======================================
        # TARJETA IZQUIERDA
        # ======================================

        with ui.card().style(
            'width:420px;padding:28px;'
        ):

            ui.label(
                'Ingrese el país emisor del documento'
            ).style(
                'font-size:13px;color:#374151;margin-bottom:8px;'
            )

            pais_input = ui.input(
                label='País Emisor',
                placeholder='Ej: Chile, Argentina, Perú',
                value=pais_actual
            ).style(
                'width:100%'
            )

            ui.label(
                'Número de documento'
            ).style(
                'font-size:13px;font-weight:600;color:#374151;margin-top:20px;margin-bottom:4px;'
            )

            config = PAIS_DEFAULT

            doc_input = ui.input(
                label=config['label'],
                placeholder=config['placeholder'],
                value=estado.get('dni', '')
            ).style(
                'width:100%;'
            )

            hint_label = ui.label(
                f'ℹ️ {config["hint"]}'
            ).style(
                'font-size:11px;color:#6B7280;margin-top:4px;'
            )

            error_label = ui.label('').style(
                '''
                color:#DC2626;
                font-size:13px;
                font-weight:bold;
                min-height:16px;
                margin-top:10px;
                '''
            )

            def validar_y_continuar():

                pais = pais_input.value.strip()
                documento = doc_input.value.strip()

                if not pais:
                    error_label.set_text(
                        'Debe ingresar un país.'
                    )
                    return

                if len(documento) < 7 or len(documento) > 9:
                    error_label.set_text(
                        'El documento debe tener entre 7 y 9 caracteres.'
                    )
                    return

                estado['pais'] = pais
                estado['dni'] = documento

                error_label.set_text('')

                on_continuar()

            ui.button(
                'Continuar →',
                on_click=validar_y_continuar
            ).style(
                '''
                width:100%;
                margin-top:25px;
                background:#12B5D9;
                color:white;
                padding:12px;
                font-weight:bold;
                font-size:16px;
                border-radius:8px;
                '''
            )

            def on_pais_change(e):
                estado['pais'] = e.value or ''

            def on_dni_change(e):
                estado['dni'] = e.value or ''

            pais_input.on_change(on_pais_change)
            doc_input.on_change(on_dni_change)

        # ======================================
        # TARJETA DERECHA
        # ======================================

        with ui.card().style(
            'width:360px;padding:24px;'
        ):

            ui.upload(
                label='Subir DNI'
            ).style(
                'width:100%'
            )