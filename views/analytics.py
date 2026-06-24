from nicegui import ui
import pandas as pd
import plotly.express as px

from services.supabase_service import obtener_declaraciones


def analytics_page():

    declaraciones = obtener_declaraciones()

    total_viajeros = len(declaraciones)

    aprobados = len([
        d for d in declaraciones
        if d.get('estado_revision') == 'aprobado'
    ])

    rechazados = len([
        d for d in declaraciones
        if d.get('estado_revision') == 'rechazado'
    ])

    sospechosos = len([
        d for d in declaraciones
        if d.get('estado_revision') == 'sospechoso'
    ])

    pendientes = len([
        d for d in declaraciones
        if d.get('estado_revision', 'pendiente') == 'pendiente'
    ])

    porcentaje_aprobacion = 0

    if total_viajeros > 0:
        porcentaje_aprobacion = round(
            (aprobados / total_viajeros) * 100,
            1
        )

    # ==========================
    # ESTILOS
    # ==========================

    ui.add_head_html("""
    <style>

    body{
        background:#0B1424;
    }

    .kpi{
        background:#182640;
        border-radius:18px;
        color:white;
        width:220px;
        padding:15px;
    }

    .alert-card{
        background:#182640;
        border-radius:18px;
        color:white;
        padding:20px;
    }

    </style>
    """)

    # ==========================
    # TITULO
    # ==========================

    ui.label(
        'Dashboard Analítico'
    ).style("""
        color:white;
        font-size:34px;
        font-weight:700;
        margin-bottom:20px;
    """)

    # ==========================
    # KPI
    # ==========================

    with ui.row():

        with ui.card().classes('kpi'):
            ui.label('👤')
            ui.label(
                str(total_viajeros)
            ).style(
                'font-size:40px;font-weight:700'
            )
            ui.label(
                'Viajeros Registrados'
            )

        with ui.card().classes('kpi'):
            ui.label('✅')
            ui.label(
                str(aprobados)
            ).style(
                'font-size:40px;font-weight:700'
            )
            ui.label(
                'Aprobados'
            )

        with ui.card().classes('kpi'):
            ui.label('❌')
            ui.label(
                str(rechazados)
            ).style(
                'font-size:40px;font-weight:700'
            )
            ui.label(
                'Rechazados'
            )

        with ui.card().classes('kpi'):
            ui.label('⚠️')
            ui.label(
                str(sospechosos)
            ).style(
                'font-size:40px;font-weight:700'
            )
            ui.label(
                'Sospechosos'
            )

    ui.separator()

    # ==========================
    # GRAFICO 1
    # ESTADO DECLARACIONES
    # ==========================

    estados_df = pd.DataFrame({
        'Estado': [
            'Aprobados',
            'Rechazados',
            'Sospechosos',
            'Pendientes'
        ],
        'Cantidad': [
            aprobados,
            rechazados,
            sospechosos,
            pendientes
        ]
    })

    fig_estado = px.pie(
        estados_df,
        names='Estado',
        values='Cantidad',
        title='Estado de Declaraciones'
    )

    fig_estado.update_layout(
        template='plotly_dark',
        paper_bgcolor='#182640'
    )

    ui.plotly(
        fig_estado
    ).style(
        'height:500px'
    )

    # ==========================
    # GRAFICO 2
    # PAISES
    # ==========================

    paises = {}

    for d in declaraciones:

        pais = d.get(
            'pais',
            'Desconocido'
        )

        paises[pais] = paises.get(
            pais,
            0
        ) + 1

    if paises:

        pais_df = pd.DataFrame({
            'Pais': list(paises.keys()),
            'Cantidad': list(paises.values())
        })

        fig_paises = px.bar(
            pais_df,
            x='Pais',
            y='Cantidad',
            title='Viajeros por País'
        )

        fig_paises.update_layout(
            template='plotly_dark',
            paper_bgcolor='#182640',
            plot_bgcolor='#182640'
        )

        ui.plotly(
            fig_paises
        ).classes(
            'w-full'
        )

    # ==========================
    # GRAFICO 3
    # REVISIONES
    # ==========================

    revision_df = pd.DataFrame({
        'Tipo': [
            'Aprobados',
            'Rechazados',
            'Sospechosos'
        ],
        'Cantidad': [
            aprobados,
            rechazados,
            sospechosos
        ]
    })

    fig_revision = px.bar(
        revision_df,
        x='Tipo',
        y='Cantidad',
        title='Resultados de Revisión'
    )

    fig_revision.update_layout(
        template='plotly_dark',
        paper_bgcolor='#182640',
        plot_bgcolor='#182640'
    )

    ui.plotly(
        fig_revision
    ).classes(
        'w-full'
    )

    # ==========================
    # ALERTAS
    # ==========================

    with ui.card().classes('alert-card'):

        ui.label(
            'Alertas Inteligentes'
        ).style(
            'font-size:24px;font-weight:700'
        )

        if sospechosos > 0:
            ui.label(
                f'⚠ {sospechosos} viajeros marcados como sospechosos'
            )

        if rechazados > aprobados:
            ui.label(
                '⚠ Los rechazos superan a las aprobaciones'
            )

        if pendientes > 0:
            ui.label(
                f'⚠ Existen {pendientes} declaraciones pendientes'
            )

        if total_viajeros == 0:
            ui.label(
                'ℹ No existen declaraciones registradas'
            )

    ui.separator()

    # ==========================
    # PREDICCION SIMPLE
    # ==========================

    with ui.card().classes('alert-card'):

        ui.label(
            'Predicción Operacional'
        ).style(
            'font-size:24px;font-weight:700'
        )

        estimado = total_viajeros + max(
            1,
            round(total_viajeros * 0.1)
        )

        ui.label(
            f'📈 Estimación próxima jornada: {estimado} viajeros'
        )

        ui.label(
            'Estimación basada en registros actuales'
        )

    ui.separator()

    ui.button(
        '⬅ Volver al Dashboard',
        on_click=lambda:
        ui.navigate.to('/operador')
    ).style("""
        background:#29B6F6;
        color:white;
        border-radius:12px;
    """)