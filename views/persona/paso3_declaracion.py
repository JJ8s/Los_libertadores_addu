from nicegui import ui

def render_paso3(on_atras, on_continuar):
    # Contenedor completamente centrado para la pantalla de carga
    with ui.column().classes('w-full items-center justify-center').style('min-height: 400px; gap: 20px; margin-top: 40px;'):
        
        # Spinner de carga circular con el color celeste de tu diseño
        ui.spinner(size='xl', color='#12B5D9', thickness=6)
        
        # Mensajes de espera para el usuario
        ui.label('Procesando Declaración...').style(
            'font-size: 22px; font-weight: 700; color: #082B57; margin-top: 10px;'
        )
        
        ui.label('Estamos validando tu información con los sistemas de control de Aduanas, PDI y SAG. Por favor, no cierres esta ventana.').style(
            'font-size: 14px; color: #6B7280; text-align: center; max-width: 450px; line-height: 1.5;'
        )

    # ── TEMPORIZADOR AUTOMÁTICO ─────────────────────────────────────────────
    # Ejecuta 'on_continuar' automáticamente después de 3.0 segundos (una sola vez)
    ui.timer(3.0, on_continuar, once=True)