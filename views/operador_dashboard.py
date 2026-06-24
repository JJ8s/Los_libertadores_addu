from nicegui import ui
from services.supabase_service import (
    obtener_declaraciones,
    actualizar_estado
)


def operador_page():

    declaraciones = obtener_declaraciones()
    total_declaraciones = len(declaraciones)

    def aprobar(declaracion):

        actualizar_estado(
            declaracion['codigo'],
            'aprobado'
        )

        ui.notify(
            'Declaración aprobada',
            color='positive'
        )

        ui.navigate.to('/operador')

    def rechazar(declaracion):

        actualizar_estado(
            declaracion['codigo'],
            'rechazado'
        )

        ui.notify(
            'Declaración rechazada',
            color='negative'
        )

        ui.navigate.to('/operador')

    def sospechoso(declaracion):

        actualizar_estado(
            declaracion['codigo'],
            'sospechoso'
        )

        ui.notify(
            'Viajero marcado como sospechoso',
            color='warning'
        )

        ui.navigate.to('/operador')

    ui.add_head_html("""
    <style>

    body{
        background:#0B1424;
        margin:0;
    }

    .sidebar{
        background:#111C33;
        width:260px;
        height:100vh;
        padding:20px;
    }

    .menu-btn{
        width:100%;
        margin-top:8px;
        color:white;
    }

    .content{
        flex:1;
        padding:25px;
    }

    .card{
        background:#182640;
        color:white;
        border-radius:18px;
        padding:15px;
    }

    </style>
    """)

    with ui.row().classes('w-full').style(
        'height:100vh; gap:0'
    ):

        # ==========================
        # SIDEBAR
        # ==========================

        with ui.column().classes('sidebar'):

            ui.label(
                'LOS LIBERTADORES'
            ).style(
                'color:white;font-size:24px;font-weight:700'
            )

            ui.label(
                'Panel Operador'
            ).style(
                'color:#9FB3C8'
            )

            ui.separator()

            ui.button(
                '📊 Dashboard'
            ).props(
                'flat'
            ).classes(
                'menu-btn'
            )

            ui.button(
                '📋 Cola Atención'
            ).props(
                'flat'
            ).classes(
                'menu-btn'
            )

            ui.button(
                '👤 Consulta Viajero'
            ).props(
                'flat'
            ).classes(
                'menu-btn'
            )

            ui.button(
                '⚠ Alertas'
            ).props(
                'flat'
            ).classes(
                'menu-btn'
            )

            ui.separator()

            ui.button(
                '📈 Dashboard Analítico',
                on_click=lambda:
                ui.navigate.to('/analytics')
            ).style("""
                background:#29B6F6;
                color:white;
                width:100%;
            """)

            ui.space()

            ui.button(
                'Cerrar Sesión',
                on_click=lambda:
                ui.navigate.to('/')
            ).style("""
                background:#F44336;
                color:white;
                width:100%;
            """)

        # ==========================
        # CONTENIDO
        # ==========================

        with ui.column().classes('content'):

            ui.label(
                'Dashboard Operador'
            ).style("""
                color:white;
                font-size:34px;
                font-weight:700;
            """)

            # ==========================
            # KPI
            # ==========================

            paises = len(
                set(
                    d.get('pais', '')
                    for d in declaraciones
                )
            )

            with ui.row():

                with ui.card().classes('card').style(
                    'width:220px'
                ):

                    ui.label('📄')

                    ui.label(
                        str(total_declaraciones)
                    ).style(
                        'font-size:42px;font-weight:700'
                    )

                    ui.label(
                        'Declaraciones'
                    )

                with ui.card().classes('card').style(
                    'width:220px'
                ):

                    ui.label('✅')

                    ui.label(
                        str(
                            len(
                                [
                                    d for d in declaraciones
                                    if d.get(
                                        'estado_revision'
                                    ) == 'aprobado'
                                ]
                            )
                        )
                    ).style(
                        'font-size:42px;font-weight:700'
                    )

                    ui.label(
                        'Aprobadas'
                    )

                with ui.card().classes('card').style(
                    'width:220px'
                ):

                    ui.label('🌎')

                    ui.label(
                        str(paises)
                    ).style(
                        'font-size:42px;font-weight:700'
                    )

                    ui.label(
                        'Países'
                    )

            ui.separator()

            # ==========================
            # TABLA
            # ==========================

            with ui.card().classes('card'):

                ui.label(
                    'Declaraciones Registradas'
                ).style(
                    'font-size:20px;font-weight:bold'
                )

                columnas = [
                    {
                        'name': 'codigo',
                        'label': 'Código',
                        'field': 'codigo'
                    },
                    {
                        'name': 'nombre',
                        'label': 'Nombre',
                        'field': 'nombre'
                    },
                    {
                        'name': 'dni',
                        'label': 'DNI',
                        'field': 'dni'
                    },
                    {
                        'name': 'pais',
                        'label': 'País',
                        'field': 'pais'
                    },
                    {
                        'name': 'estado',
                        'label': 'Estado',
                        'field': 'estado'
                    }
                ]

                filas = []

                for declaracion in declaraciones:

                    filas.append({

                        'codigo':
                        str(
                            declaracion.get(
                                'codigo',
                                ''
                            )
                        )[:8],

                        'nombre':
                        f"{declaracion.get('nombre','')} {declaracion.get('apellido','')}",

                        'dni':
                        declaracion.get(
                            'dni',
                            ''
                        ),

                        'pais':
                        declaracion.get(
                            'pais',
                            ''
                        ),

                        'estado':
                        declaracion.get(
                            'estado_revision',
                            'pendiente'
                        )
                    })

                ui.table(
                    columns=columnas,
                    rows=filas
                ).classes('w-full')

            ui.separator()

            # ==========================
            # REVISIÓN
            # ==========================

            ui.label(
                'Revisión de Declaraciones'
            ).style(
                'font-size:22px;font-weight:bold;color:white'
            )

            for declaracion in declaraciones:

                with ui.card().classes('card').style(
                    'margin-top:10px'
                ):

                    ui.label(
                        f"{declaracion.get('nombre','')} {declaracion.get('apellido','')}"
                    ).style(
                        'font-size:18px;font-weight:bold'
                    )

                    ui.label(
                        f"DNI: {declaracion.get('dni','')}"
                    )

                    ui.label(
                        f"País: {declaracion.get('pais','')}"
                    )

                    ui.label(
                        f"Estado actual: {declaracion.get('estado_revision','pendiente')}"
                    )

                    with ui.row():

                        ui.button(
                            '🟢 PASA',
                            on_click=lambda d=declaracion:
                            aprobar(d)
                        ).style(
                            'background:green;color:white'
                        )

                        ui.button(
                            '🔴 NEGADO',
                            on_click=lambda d=declaracion:
                            rechazar(d)
                        ).style(
                            'background:red;color:white'
                        )

                        ui.button(
                            '🟡 SOSPECHOSO',
                            on_click=lambda d=declaracion:
                            sospechoso(d)
                        ).style(
                            'background:orange;color:black'
                        )