from nicegui import ui
from .estado import estado


# 💡 Hacemos que on_ver_tramites=None sea opcional para evitar el TypeError
def render_dashboard_home(on_nuevo_tramite, on_ver_tramites=None):

    ui.label('Portal del Viajero').style('''
        font-size:34px;
        font-weight:700;
        color:#082B57;
    ''')

    ui.label('Seleccione una opción')

    with ui.row().classes('justify-center').style(
        'width:100%; gap:30px; margin-top:30px;'
    ):

        # 📝 TARJETA: NUEVO TRÁMITE
        with ui.card().style('width:300px; height:220px; padding:20px; border-radius:12px; box-shadow:0 4px 15px rgba(0,0,0,0.05);'):
            ui.label('📝').style('font-size:50px')
            ui.label('Nuevo Trámite').style('font-weight:700; font-size:16px; color:#1F2937;')
            ui.button('Comenzar', on_click=on_nuevo_tramite).style(
                'background:#12B5D9; color:white; width:100%; margin-top:12px; font-weight:bold; border-radius:8px;'
            )

        # 📂 TARJETA: MIS TRÁMITES
        with ui.card().style('width:300px; height:220px; padding:20px; border-radius:12px; box-shadow:0 4px 15px rgba(0,0,0,0.05);'):
            ui.label('📂').style('font-size:50px')
            ui.label('Mis Trámites').style('font-weight:700; font-size:16px; color:#1F2937;')
            
            def acceder_al_comprobante():
                # Rellenamos con datos demo si está vacío para pruebas
                if not estado.get('nombre', '').strip():
                    estado['nombre'] = 'Diego'
                    estado['apellido'] = 'Pérez'
                    estado['dni'] = '20444888'
                    estado['pais'] = 'Argentina'
                    estado['nacionalidad'] = 'Argentina'
                    estado['correo'] = 'diego.perez@mail.com'
                    estado['proposito'] = 'turismo'
                    ui.notify('ℹ️ Cargando demostración del último trámite generado.', type='info')
                
                # Ejecuta la navegación si fue configurada, de lo contrario avisa amigablemente
                if on_ver_tramites:
                    on_ver_tramites()
                else:
                    ui.notify('⚠️ No se ha enrutado la función para visualizar el historial aún.', type='warning')

            ui.button('Ver', on_click=acceder_al_comprobante).style(
                'background:#082B57; color:white; width:100%; margin-top:12px; font-weight:bold; border-radius:8px;'
            )