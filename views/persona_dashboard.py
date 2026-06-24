from nicegui import ui
from .persona.estado import estado, resetear
from .persona.dashboard_home import render_dashboard_home
from .persona.paso1_identificacion import render_paso1
from .persona.paso2_datos import render_paso2
from .persona.paso3_declaracion import render_paso3
from .persona.paso4_confirmacion import render_paso4


def persona_page():

    with ui.element('div').style('''
        width:100%;
        min-height:100vh;
        display:flex;
        justify-content:center;
        background:#f4f7fb;
    '''):

        contenedor = ui.column().style('''
            width:100%;
            max-width:1200px;
            padding:40px;
        ''')

        def cambiar_paso(nuevo):
            estado['paso'] = nuevo
            render()

        def volver_dashboard():
            estado['pantalla'] = 'dashboard'
            render()

        def nuevo_tramite():
            resetear()
            render()

        def render():
            contenedor.clear()

            with contenedor:

                if estado['pantalla'] == 'dashboard':
                    render_dashboard_home(on_nuevo_tramite=nuevo_tramite)

                elif estado['pantalla'] == 'formulario':
                    _render_barra_pasos()

                    if estado['paso'] == 1:
                        render_paso1(
                            on_continuar=lambda: cambiar_paso(2)
                        )
                    elif estado['paso'] == 2:
                        render_paso2(
                            on_atras=lambda: cambiar_paso(1),
                            on_continuar=lambda: cambiar_paso(3)
                        )
                    elif estado['paso'] == 3:
                        render_paso3(
                            on_atras=lambda: cambiar_paso(2),
                            on_continuar=lambda: cambiar_paso(4)
                        )
                    elif estado['paso'] == 4:
                        render_paso4(
                            on_atras=lambda: cambiar_paso(3),
                            on_finalizar=volver_dashboard
                        )

        def _render_barra_pasos():
            nombres = ['Identificación', 'Datos', 'Declaración', 'Confirmación']

            with ui.row().classes('justify-center items-center').style(
                'gap:25px;margin-bottom:30px;'
            ):
                for i, nombre in enumerate(nombres, start=1):
                    color = '#12B5D9' if i <= estado['paso'] else '#D1D5DB'

                    with ui.column().classes('items-center'):
                        ui.label(str(i)).style(f'''
                            width:50px;
                            height:50px;
                            border-radius:50%;
                            background:{color};
                            color:white;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            font-weight:bold;
                        ''')
                        ui.label(nombre)

        render()