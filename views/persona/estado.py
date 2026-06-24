estado = {

    # navegación
    'pantalla': 'dashboard',
    'paso': 1,

    # identificación
    'dni': '',
    'pais': '',

    # datos personales
    'nombre': '',
    'apellido': '',
    'nacionalidad': '',
    'fecha_nacimiento': '',
    'correo': '',

    # declaración
    'mercancias': False,
    'dinero': False,
    'alimentos': False,
    'mascotas': False,
    'observaciones': ''
}


def resetear():
    estado['pantalla'] = 'formulario'
    estado['paso'] = 1
    estado['dni'] = ''
    estado['pais'] = ''
    estado['nombre'] = ''
    estado['apellido'] = ''
    estado['nacionalidad'] = ''
    estado['fecha_nacimiento'] = ''
    estado['correo'] = ''
    estado['mercancias'] = False
    estado['dinero'] = False
    estado['alimentos'] = False
    estado['mascotas'] = False
    estado['observaciones'] = ''