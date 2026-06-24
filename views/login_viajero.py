from nicegui import ui, app
from services.auth import login


def login_viajero():

    with ui.card().style("""
        width:420px;
        margin:auto;
        margin-top:100px;
        padding:30px;
    """):

        ui.label(
            'Ingreso Viajero'
        ).style(
            'font-size:28px;font-weight:700'
        )

        correo = ui.input('Correo')
        password = ui.input(
            'Contraseña',
            password=True
        )

        def ingresar():

            try:

                usuario = login(
                    correo.value.strip(),
                    password.value.strip()
                )

                print('Usuario encontrado:', usuario)

                if usuario is None:
                    ui.notify(
                        'Credenciales incorrectas',
                        color='negative'
                    )
                    return

                if usuario['rol'] != 'viajero':
                    ui.notify(
                        'No es un usuario viajero',
                        color='negative'
                    )
                    return

                app.storage.user['nombre'] = usuario['nombre']
                app.storage.user['rol'] = usuario['rol']

                ui.notify(
                    f'Bienvenido {usuario["nombre"]}',
                    color='positive'
                )

                print('Navegando a /persona')

                ui.navigate.to('/persona')

            except Exception as e:

                print('ERROR LOGIN:', e)

                ui.notify(
                    f'Error: {str(e)}',
                    color='negative'
                )

        ui.button(
            'Ingresar',
            on_click=ingresar
        ).classes('w-full')