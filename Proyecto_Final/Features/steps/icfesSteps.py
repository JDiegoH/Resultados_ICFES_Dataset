from behave import *
from Principal import *

@given ('un Principal')
def step_imp(context):
    context.icfes = cargador()


@when ('abrir archivo')
def step_imp(context):
    context.file = context.icfes.abrirArchivo('Proyecto_final/Prueba_Saber_11_2019-2.csv')


@then ('agrupar tablas')
def step_imp(context):
    assert context.file.verificador()
