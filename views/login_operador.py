from nicegui import ui, app
from services.auth import login


def login_operador():

    with ui.card().style("""
        width:420px;
        margin:auto;
        margin-top:100px;
        padding:30px;
    """):

        ui.label(
            'Ingreso Operador'
        ).style(
            'font-size:28px;font-weight:700'
        )

        correo = ui.input(
            'Correo'
        )

        password = ui.input(
            'Contraseña',
            password=True
        )

        def ingresar():

            usuario = login(
                correo.value,
                password.value
            )

            if not usuario:
                ui.notify(
                    'Credenciales incorrectas',
                    color='negative'
                )
                return

            if usuario['rol'] != 'admin':
                ui.notify(
                    'No es un administrador',
                    color='negative'
                )
                return

            app.storage.user['nombre'] = usuario['nombre']
            app.storage.user['rol'] = usuario['rol']

            ui.navigate.to('/operador')

        ui.button(
            'Ingresar',
            on_click=ingresar
        ).classes('w-full')