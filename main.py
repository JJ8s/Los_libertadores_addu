from nicegui import ui

# IMPORTACIONES
from views.home import home_page
from views.login_viajero import login_viajero
from views.login_operador import login_operador
from views.persona_dashboard import persona_page
from views.operador_dashboard import operador_page
from views.analytics import analytics_page


# HOME
@ui.page('/')
def home():
    home_page()


# LOGIN VIAJERO
@ui.page('/login-viajero')
def login_persona():
    login_viajero()


# LOGIN OPERADOR
@ui.page('/login-operador')
def login_op():
    login_operador()


# DASHBOARD VIAJERO
@ui.page('/persona')
def persona():
    persona_page()


# DASHBOARD OPERADOR
@ui.page('/operador')
def operador():
    operador_page()


# DASHBOARD ANALÍTICO
@ui.page('/analytics')
def analytics():
    analytics_page()


# EJECUTAR APP
ui.run(
    title='Los Libertadores Digital',
    reload=True,
    favicon='🌎',
    storage_secret='mi_clave_secreta_123'
)