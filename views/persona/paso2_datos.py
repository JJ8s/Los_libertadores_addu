from nicegui import ui
from .estado import estado
import re


def render_paso2(on_atras, on_continuar):
    
    # 1. Aseguramos que existan todas las variables en el estado global
    if 'nombre' not in estado: estado['nombre'] = ''
    if 'apellido' not in estado: estado['apellido'] = ''
    if 'nacionalidad' not in estado: estado['nacionalidad'] = ''
    if 'fecha_nacimiento' not in estado: estado['fecha_nacimiento'] = ''
    if 'correo' not in estado: estado['correo'] = ''
    if 'proposito' not in estado: estado['proposito'] = None
    if 'bienes' not in estado:
        estado['bienes'] = {
            'alimentos': False,
            'animales': False,
            'medicamentos': False,
            'dinero': False,
            'agricolas': False,
            'armas': False
        }
    if 'menores' not in estado:
        estado['menores'] = False

    # 2. Helper para los estilos interactivos de las tarjetas de propósito y bienes
    def get_card_style(is_selected):
        base = 'border-radius:12px; border:2px solid; cursor:pointer; transition:all 0.2s ease; box-shadow:none;'
        if is_selected:
            return f"{base} border-color:#06B6D4; background-color:#ECFEFF;" # Cyan activo
        return f"{base} border-color:#F3F4F6; background-color:#FFFFFF;" # Gris inactivo
        
    # --- CONTENEDOR PRINCIPAL ---
    with ui.column().style('width:100%; max-width:520px; margin:0 auto; gap:24px; font-family:sans-serif;'):
        
        ui.label('Paso 2 - Datos Personales y Declaración').style(
            'font-size:22px; font-weight:700; color:#082B57; margin-bottom:-4px;'
        )

        # ─── SECCIÓN A: DATOS PERSONALES Y CONTACTO (Tu segundo bloque de código) ───
        with ui.card().style('width:100%; padding:24px; gap:12px; border-radius:12px; border:1px solid #E5E7EB; box-shadow:none; background:#FFFFFF;'):
            
            ui.label('DATOS DE ORIGEN E IDENTIDAD').style(
                'font-weight:800; font-size:11px; color:#1F2937; letter-spacing:1px; border-bottom:1px solid #F3F4F6; width:100%; padding-bottom:4px;'
            )

            ui.input(
                label='Nombre(s)',
                placeholder='Ej: Juan Carlos',
            ).bind_value(estado, 'nombre').style('width:100%')

            ui.input(
                label='Apellido(s)',
                placeholder='Ej: García López',
            ).bind_value(estado, 'apellido').style('width:100%')

            ui.input(
                label='Nacionalidad de origen',
                placeholder='Ej: Argentina',
            ).bind_value(estado, 'nacionalidad').style('width:100%')

            # COMBINACIÓN: CALENDARIO + TEXTO BRUTO
            fecha_input = ui.input(
                label='Fecha (AAAA-MM-DD) o Año de nacimiento',
                placeholder='Ej: 1995-08-25 o 1995',
            ).bind_value(estado, 'fecha_nacimiento').style('width:100%')
            
            with fecha_input:
                with ui.menu() as menu:
                    ui.date().bind_value(fecha_input).on('change', menu.close)
                with fecha_input.add_slot('append'):
                    ui.icon('calendar_today').on('click', menu.open).classes('cursor-pointer')

            ui.label('INFORMACIÓN DE CONTACTO').style(
                'font-weight:800; font-size:11px; color:#1F2937; letter-spacing:1px; border-bottom:1px solid #F3F4F6; width:100%; padding-bottom:4px; margin-top:10px;'
            )

            correo_input = ui.input(
                label='Correo electrónico',
                placeholder='Ej: juan@mail.com',
            ).bind_value(estado, 'correo').style('width:100%')

            correo_error = ui.label('').style('color:#DC2626; font-size:12px; min-height:16px; margin-top:-6px;')

            def validar_correo(e):
                valor = e.value or ''
                if valor and '@' not in valor:
                    correo_error.set_text('⚠️ El correo debe contener @')
                else:
                    correo_error.set_text('')

            correo_input.on('update:model-value', validar_correo)


        # ─── SECCIÓN B: PROPÓSITO DEL VIAJE ───
        with ui.row().style('width:100%; justify-content:space-between; align-items:center; margin-bottom:-10px;'):
            ui.label('PROPÓSITO DEL VIAJE').style('font-weight:800; font-size:11px; color:#1F2937; letter-spacing:1px;')
            ui.label('OBLIGATORIO').style('background-color:#ECFEFF; color:#06B6D4; font-size:10px; font-weight:700; padding:4px 8px; border-radius:4px;')

        @ui.refreshable
        def render_proposito():
            with ui.row().style('width:100%; gap:8px; flex-wrap:nowrap;'):
                
                def seleccionar_prop(val):
                    estado['proposito'] = val
                    render_proposito.refresh()
                    render_btn_continuar.refresh() # Activa o desactiva visualmente el botón inferior

                def build_p_card(icon, label, val):
                    selected = estado['proposito'] == val
                    text_color = '#1F2937' if selected else '#4B5563'
                    with ui.card().style(get_card_style(selected) + 'flex:1; padding:16px 4px; align-items:center;').on('click', lambda: seleccionar_prop(val)):
                        ui.icon(icon).style('font-size:32px; color:#06B6D4;')
                        ui.label(label).style(f'font-size:10px; font-weight:700; margin-top:8px; color:{text_color};')

                build_p_card('beach_access', 'TURISMO', 'turismo')
                build_p_card('work', 'NEGOCIOS', 'negocios')
                build_p_card('local_shipping', 'CARGA', 'carga')
                build_p_card('home', 'RESIDENCIA', 'residencia')
        render_proposito()

        # Barra decorativa inferior del propósito
        with ui.row().style('width:100%; height:16px; background:#374151; border-radius:4px; align-items:center; justify-content:space-between; padding:0 8px; margin-top:-14px;'):
            ui.icon('arrow_left').style('color:#9CA3AF; font-size:14px;')
            ui.element('div').style('width:50%; height:6px; background:#9CA3AF; border-radius:4px;')
            ui.icon('arrow_right').style('color:#9CA3AF; font-size:14px;')


        # ─── SECCIÓN C: DECLARACIÓN DE BIENES ───
        with ui.row().style('width:100%; justify-content:space-between; align-items:center; margin-bottom:-10px;'):
            ui.label('DECLARACIÓN DE BIENES').style('font-weight:800; font-size:11px; color:#1F2937; letter-spacing:1px;')
            ui.label('SI CORRESPONDE').style('color:#9CA3AF; font-size:10px; font-weight:700;')

        @ui.refreshable
        def render_bienes():
            with ui.grid(columns=2).style('width:100%; gap:12px;'):
                
                def toggle_bien(val):
                    estado['bienes'][val] = not estado['bienes'][val]
                    render_bienes.refresh()

                def build_b_card(icon, label, val):
                    selected = estado['bienes'][val]
                    with ui.card().style(get_card_style(selected) + 'flex-direction:row; align-items:center; padding:12px 16px; gap:12px;').on('click', lambda: toggle_bien(val)):
                        ui.icon(icon).style('font-size:24px; color:#06B6D4;')
                        ui.label(label).style('font-size:11px; font-weight:700; color:#1F2937;')

                build_b_card('eco', 'ALIMENTOS', 'alimentos')
                build_b_card('pets', 'ANIMALES', 'animales')
                build_b_card('medication', 'MEDICAMENTOS', 'medicamentos')
                build_b_card('attach_money', '+$10.000 USD', 'dinero')
                build_b_card('grass', 'PROD. AGRÍCOLAS', 'agricolas')
                build_b_card('shield', 'ARMAS/MUNICIÓN', 'armas')
        render_bienes()


        # ─── SECCIÓN D: MENORES DE EDAD ───
        with ui.card().style('width:100%; flex-direction:row; justify-content:space-between; align-items:center; padding:16px 20px; border-radius:12px; border:1px solid #E5E7EB; box-shadow:none; margin-top:8px; background:#FFFFFF;'):
            with ui.row().style('gap:16px; align-items:center;'):
                ui.icon('group').style('font-size:28px; color:#F59E0B;') 
                with ui.column().style('gap:0;'):
                    ui.label('¿Viajas con menores?').style('font-size:14px; font-weight:700; color:#1F2937;')
                    ui.label('Requiere autorización notarial').style('font-size:11px; color:#9CA3AF;')
            ui.switch().bind_value(estado, 'menores').props('color="cyan"')


        # ─── SECCIÓN E: ADVERTENCIA LEGAL ───
        with ui.row().style('width:100%; background-color:#F1F5F9; padding:16px; border-radius:12px; flex-wrap:nowrap; align-items:center; gap:12px;'):
            ui.icon('info_outline').style('color:#06B6D4; font-size:24px;')
            ui.label('Toda declaración falsa es sancionada por la ley. Al presionar continuar, confirma que la información proporcionada es verídica.').style('font-size:11px; color:#6B7280; line-height:1.4;')


        # ─── CONTROL DE ERRORES Y BOTONES DE NAVEGACIÓN ───
        form_error = ui.label('').style('color:#DC2626; font-size:13px; font-weight:600; margin-top:4px; min-height:20px; text-align:center; width:100%;')

        def validar_y_continuar():
            form_error.set_text('')

            if not estado.get('nombre', '').strip():
                form_error.set_text('⚠️ Ingresá tu nombre.')
                return
            if not estado.get('apellido', '').strip():
                form_error.set_text('⚠️ Ingresá tu apellido.')
                return
            if not estado.get('nacionalidad', '').strip():
                form_error.set_text('⚠️ Ingresá tu nacionalidad de origen.')
                return
            if not estado.get('fecha_nacimiento', '').strip():
                form_error.set_text('⚠️ Ingresá tu fecha o año de nacimiento.')
                return
            
            correo = estado.get('correo', '').strip()
            if not correo:
                form_error.set_text('⚠️ Ingresá tu correo electrónico.')
                return
            if '@' not in correo:
                form_error.set_text('⚠️ El correo debe contener @.')
                return
            if not estado.get('proposito'):
                form_error.set_text('⚠️ Por favor, selecciona un Propósito de Viaje.')
                return

            on_continuar()

        with ui.row().style('width:100%; gap:12px; margin-top:4px; flex-wrap:nowrap;'):
            ui.button('Atrás', on_click=on_atras).style(
                'background:#F3F4F6; color:#4B5563; border-radius:12px; padding:16px; box-shadow:none; font-weight:700;'
            )
            
            @ui.refreshable
            def render_btn_continuar():
                listo = estado.get('proposito') is not None
                bg = '#E2E8F0' if not listo else '#06B6D4'
                txt = '#94A3B8' if not listo else '#FFFFFF'
                cursor = 'not-allowed' if not listo else 'pointer'
                
                ui.button('CONTINUAR CON EL TRÁMITE >', on_click=validar_y_continuar if listo else None).style(
                    f'flex:1; border-radius:12px; padding:16px; font-weight:800; font-size:13px; box-shadow:none; background:{bg}; color:{txt}; cursor:{cursor};'
                )
            render_btn_continuar()