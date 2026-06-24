from nicegui import ui

def home_page():

    ui.add_head_html("""
    <style>
        body {
            margin: 0;
            background: linear-gradient(
                135deg,
                #082B57 0%,
                #16457A 100%
            );
        }
    </style>
    """)

    with ui.element('div').style('''
        position:fixed;
        top:0;
        left:0;
        width:100%;
        height:100vh;
        display:flex;
        justify-content:center;
        align-items:center;
    '''):

        with ui.column().classes(
            'items-center'
        ).style(
            'gap:20px;'
        ):

            ui.icon(
                'travel_explore',
                size='80px'
            ).style(
                '''
                color:#12B5D9;
                padding:25px;
                border-radius:20px;
                background:rgba(255,255,255,0.1);
                '''
            )

            ui.label(
                'LOS LIBERTADORES'
            ).style(
                '''
                color:white;
                font-size:48px;
                font-weight:800;
                '''
            )

            ui.label(
                'DIGITAL'
            ).style(
                '''
                color:#12B5D9;
                font-size:48px;
                font-weight:800;
                margin-top:-15px;
                '''
            )

            ui.label(
                'SISTEMA DE MODERNIZACIÓN DIGITAL'
            ).style(
                '''
                color:#BFC9D8;
                letter-spacing:2px;
                '''
            )

            ui.button(
                'INICIAR TRÁMITE',
                on_click=lambda: ui.navigate.to('/login-viajero')
            ).style(
                '''
                width:350px;
                height:60px;
                background:#12B5D9;
                color:white;
                border-radius:16px;
                font-size:18px;
                font-weight:700;
                margin-top:20px;
                '''
            )

            ui.link(
                '🛡 Panel Operador',
                '/login-operador'
            ).style(
                '''
                color:#8FB6D9;
                margin-top:10px;
                text-decoration:none;
                '''
            )